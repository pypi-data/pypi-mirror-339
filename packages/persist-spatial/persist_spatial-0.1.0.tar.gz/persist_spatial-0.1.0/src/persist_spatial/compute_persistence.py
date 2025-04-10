import numpy as np
import pandas as pd
import dionysus as d
import pickle
from scipy.sparse import csc_array
from sklearn.preprocessing import normalize
from typing import List

from persist_spatial.network_functions import get_distances
from persist_spatial.smoothed_expression import distance_to_measure_weighted
from persist_spatial.topology_utils import p_norm, diagram_to_array, function_filtration
from persist_spatial.post_ph_functions import find_knee

def run_persistence(data: pd.DataFrame, p: int =2, m: float =0.1, mesh_type: str ="hexagonal", sensitivity: float =1, 
                    metrics_storage_location: str =None, diagrams_storage_location: str =None, log_storage_location: str =None, 
                    notes: str =None, return_metrics: bool =True, return_diagrams: bool =False):
    
    """ Computes spatial structure scores for all variables in a spatial 'omics dataset.
    
        Takes in expression and co-ordinate data for a set of wells from a single tissue sample and computes the Coefficient
        of spatial structure (CoSS) for each gene. Optionally stores spatial metrics (norms, ratios, ranks, and SVG calls) and 
        persistence diagrams in user-specified locations.

        Parameters
        ----------        
        data : pd.DataFrame
            pandas DataFrame of the form
                   x , y , gene1 , gene2, ... , geneN
                   .   .     .       .            .    
                   .   .     .       .            .    
            where (x, y) are the co-ordinates of each well, and genei is the expression of gene i in each well.                           
        p : float, default=2 
            Specifies which norm of the 0D persistence diagram to use as the CoSS. Should lie in [0,infinity).
        m : float, default=0.1
            Specifies the probability mass threshold to use in distance to measure computation. Should lie in (0,1).
        mesh_type : str, default='hexagonal' 
            Type of mesh that the well co-ordinates lie on. Allowed values are "hexagonal" or "square".
        sensitivity : float, default=1 
            Controls the behaviour of the automatic CoSS threshold selection for declaring a gene as spatially variable.
        metrics_storage_location : str, default=None 
            Filepath specifiying where to store metrics csv file.
        diagrams_storage_location : str, default=None
            Filepath specifiying where to store the dictionary of persistence diagrams for each gene. Stored as a pickle file.
        log_storage_location : str, default=None
            Filepath specifying where to record details of persistence computation. Stored as a text file. 
        notes : str, default=None
            Extra text to be appended on to the log. 
        return_metrics : bool, default=True
            Whether to return the metrics data frame. If return_metrics=True and return_diagrams=True, both objects will be reutrned in the order (metrics, diagrams). 
        return_diagrams : bool, default=True 
            Whether to return persistence diagrams what objects to return. If return_metrics=True and return_diagrams=True, both objects will be reutrned in the order (metrics, diagrams).

        Returns
        ----------
        pd.DataFrame
            Data frame contaning CoSS and other metrics for each gene.
        List[d.Diagram]
            Lost of persistence diagrams for each gene, indexed by gene name (taken from the column names of the input data frame).       
        
        """
    
    # == Treat missing entries as zero expression ==
    
    data = data.fillna(0)
    
    # == Setup expression and co-ordinate data ==
    
    expression_array = normalize(np.array(data.iloc[:,2:]), axis=0, norm="l1") 
    expression_sparse = csc_array(expression_array)
    
    co_ordinates = np.array(data.iloc[:,:2])
    
    
    # == Network structure setup ==
    
    # Compute well-well distance matrix, so dmat[i,j] = d(well_i, well_j)
    # Also compute an upper triangular version for use in creating the filtration
    num_wells = data.shape[0]
    dmat_ut = np.zeros((num_wells,num_wells))
    dmat = np.zeros((num_wells,num_wells))
    for i in range(num_wells):
        dmat[i,:] = np.sqrt( ((co_ordinates[i,0] - co_ordinates[:,0])**2 + (co_ordinates[i,1] - co_ordinates[:,1])**2) )
        dmat_ut[i,i:] = np.sqrt( ((co_ordinates[i,0] - co_ordinates[i:,0])**2 + (co_ordinates[i,1] - co_ordinates[i:,1])**2) )
        
    # Compute the distance between adjacent wells as the smallest non-zero entry in dmat
    dunique = np.unique(dmat)
    well_sep = dunique[dunique>0].min()
    
    # Set distance threshold for treating wells as adjacent
    if mesh_type=="hexagonal":
        dthresh = (0.5*(1+np.sqrt(3))) * well_sep
    elif mesh_type=="square":
        dthresh = (0.5*(1+np.sqrt(2))) * well_sep
        
    # Compute an ordered list of the num_wells smallest squared distances from the central vertex that appear in a radial grid 
    grid_distances = get_distances(num_wells, well_sep, mesh_type)
    
    # Create a version of dmat with the actual distances replaced by the network distances 
    dmat_comp = np.zeros((num_wells,num_wells))
    for i in range(dmat.shape[0]):
        dmat_comp[i,dmat[i,:].argsort()] = grid_distances
    
    # Determine which pairs of wells are adjacent (i.e. which edges to include in the simplicial complex),
    # edge [i,j] is in the SC if it appears as a row in edges
    edges_to_add = np.where((dmat_ut>0) & (dmat_ut <= dthresh)) # Using upper triangular distance matrix ensures no duplication of edges (i.e. including both [i,j] and [j,i])
    edges = np.zeros((edges_to_add[0].size, 2))
    edges[:,0] = np.array(edges_to_add[0])
    edges[:,1] = np.array(edges_to_add[1])
    edges = edges.astype(int)  
    
    
    
    # == Compute persistent homology ==
    
    # Create objects for storing results 
    gene_list = data.columns[2:]
    num_genes = expression_array.shape[1]
    svg_calls = np.array(["No"]*(num_genes), dtype="<U3")# dtype="<U3" to allow "Yes" to be written later
    artefact_calls = np.array(["No"]*(num_genes), dtype="<U3")
    norms = np.zeros(num_genes)
    ratios = np.zeros(num_genes)
    
    record_diagrams = not diagrams_storage_location==None
    compute_diagrams = record_diagrams | return_diagrams
    if compute_diagrams:
        diagrams = {}

    # Determine which genes to compute persistence on
    compute_ph = np.where(expression_sparse.sum(axis=0)>0)[0]
    
    # Compute 0dPH for each gene with expression
    for i in compute_ph:
        expressed_wells = expression_array[:,i]>0
        
        # Determine which wells have expression (we will be skipping over the zero wells in the smoothing)
        weights = expression_sparse[expressed_wells,[i]].flatten()
        # Determine which indices sort the wells in descending order (- sign is as .argsort() by default sorts in ascending order)
        indices = (-weights).argsort()
        # Sort the weights by this
        weights = weights[indices]
        # Filter down dmat_comp columns to those wells with expression
        # Order columns by expression, to ensure that when we sort wells by distance to the well we are computing dtm for later on,
        # ties are broken by expression (by default .argsort() breaks ties by the order elements appear in the array pre-sorting)
        dists = dmat_comp[:,expressed_wells][:,indices]
        
        # Compute distance to measure
        dtm = distance_to_measure_weighted(weights=weights, dmat=dists, m=m)
        
        # Create filtration
        f = function_filtration(values=dtm, edges=edges)

        # Compute the 0 dimensional persistent homology
        ph = d.homology_persistence(f)
        dgm = d.init_diagrams(ph, f)
        dgm_array = diagram_to_array(dgm, 0)
        
        # Record the specified norm of persistence diagram, the persistence diagram itself, 
        # and the L_infinity / L_1 norm ratio for artifact detection
        norms[i] = p_norm(dgm_array, p=2)
        try: # try except clause is to handle the case where there are no features and so ||diagram||_1 = 0
            ratios[i] = p_norm(dgm_array, p=np.inf) / p_norm(dgm_array, p=1)
        except ZeroDivisionError:
            ratios[i] = 0
        if compute_diagrams:
            diagrams[gene_list[i]] = dgm
    
    # Call SVGs, using maximum curvature (via the kneed.KneeLocator() function) to determine the cutoff for SVG calling
    cutoff = find_knee(pd.Series(norms))
    ranks = np.zeros(norms.size)
    ranks[norms.argsort()] = np.linspace(norms.size, 1, norms.size) # think about it...
    if not cutoff==None:
        cutoff *= sensitivity
        svg_calls[ranks <= cutoff] = "Yes"
        
    artefact_calls[ratios > 0.9] = "Yes"
    
    # Create data frame of norm, ratio, rank and SVG call
    metrics = pd.DataFrame({"gene":pd.Series(gene_list), "CoSS":norms, "ratio":ratios, "gene_rank":ranks, "possible_artefact":artefact_calls, "svg":svg_calls}) 
    
    
    # == Store results if requested ==
    
    # Save persistence diagrams and norms
    if record_diagrams:
        with open(diagrams_storage_location, "wb") as f:
            pickle.dump(diagrams, f)
    
    if not metrics_storage_location==None:
        print("saving metrics")
        metrics.to_csv(metrics_storage_location, index=False)
        
    # Create log of details
    if not log_storage_location==None:
        with open(log_storage_location, "w") as f:
            f.write("p: " + str(p) + "\n")
            f.write("m: " + str(m) + "\n")  
            if not notes==None:
                f.write(notes + "\n")
    
    
    # == Return desired objects ==
    
    if return_metrics:
        if return_diagrams:
            return metrics, diagrams
        else:
            return metrics
    elif return_diagrams:
        return diagrams