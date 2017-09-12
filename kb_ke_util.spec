/*
A KBase module: kb_ke_util
*/

module kb_ke_util {

  /* A boolean - 0 for false, 1 for true.
    @range (0, 1)
  */
  typedef int boolean;

  /* An X/Y/Z style reference*/
  typedef string obj_ref;

  /***************
  math layer
  ***************/

  /* Input of the run_pdist function
    data_matrix - raw data matrix with row_ids, col_ids and values
                  e.g.{'row_ids': ['gene_1', 'gene_2'], 
                       'col_ids': ['condition_1', 'condition_2'],
                       'values': [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]}

    Optional arguments:
    metric - The distance metric to use. Default set to 'euclidean'.
             The distance function can be 
             ["braycurtis", "canberra", "chebyshev", "cityblock", "correlation", "cosine", 
              "dice", "euclidean", "hamming", "jaccard", "kulsinski", "matching", 
              "rogerstanimoto", "russellrao", "sokalmichener", "sokalsneath", "sqeuclidean", 
              "yule"]
              Details refer to: 
              https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html

    Note: Advanced metric functions 'minkowski', 'seuclidean' and 'mahalanobis' included in 
          scipy.spatial.distance.pdist library are not implemented
  */
  typedef structure {
    mapping<string, list<string>> data_matrix;
    string metric;
  } PdistParams;

  /* Ouput of the run_pdist function
    dist_matrix - 1D distance matrix
    labels - item name corresponding to each dist_matrix element
  */
  typedef structure {
    list<float> dist_matrix;
    list<string> labels;
  } PdistOutput;

  /* run_pdist: a wrapper method for scipy.spatial.distance.pdist
     reference: 
     https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html*/
  funcdef run_pdist(PdistParams params) returns(PdistOutput returnVal) authentication required;

  /* Input of the run_linkage function
    dist_matrix - 1D distance matrix (refer to run_pdist return)

    Optional arguments:
    method - The linkage algorithm to use. Default set to 'ward'.
             The method can be 
             ["single", "complete", "average", "weighted", "centroid", "median", "ward"]
             Details refer to: 
             https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
  */
  typedef structure {
    list<float> dist_matrix;
    string method;
  } LinkageParams;

  /* Ouput of the run_linkage function
    linkage_matrix - The hierarchical clustering encoded as a linkage matrix
  */
  typedef structure {
    list<list<float>> linkage_matrix;
  } LinkageOutput;

  /* run_linkage: a wrapper method for scipy.cluster.hierarchy.linkage
     reference: 
     https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html*/
  funcdef run_linkage(LinkageParams params) returns(LinkageOutput returnVal) authentication required;


  /* Input of the run_fcluster function
    linkage_matrix - hierarchical clustering linkage matrix (refer to run_linkage return)
    dist_threshold - the threshold to apply when forming flat clusters

    Optional arguments:
    labels - items corresponding to each linkage_matrix element 
             (If labels are given, result flat_cluster will be mapped to element in labels.)
    criterion - The criterion to use in forming flat clusters. Default set to 'distance'.
                The criterion can be 
                ["inconsistent", "distance", "maxclust"]
                Note: Advanced criterion 'monocrit', 'maxclust_monocrit' in 
                scipy.cluster.hierarchy.fcluster library are not implemented
                Details refer to: 
                https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html
  */
  typedef structure {
    list<list<float>> linkage_matrix;
    float dist_threshold;
    list<string> labels;
    string criterion;
  } FclusterParams;

  /* Ouput of the run_fcluster function
     flat_cluster - A dictionary of flat clusters.
                    Each element of flat_cluster representing a cluster contains a label array. 
                    (If labels is none, element position array is returned to each cluster group)
  */
  typedef structure {
    mapping<string, list<string>> flat_cluster;
  } FclusterOutput;

  /* run_fcluster: a wrapper method for scipy.cluster.hierarchy.fcluster
     reference: 
     https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html*/
  funcdef run_fcluster(FclusterParams params) returns(FclusterOutput returnVal) authentication required;

  /* Input of the run_dendrogram function
    linkage_matrix - hierarchical clustering linkage matrix (refer to run_linkage return)

    Optional arguments:
    dist_threshold - the threshold to apply when forming flat clusters (draw a horizontal line to dendrogram)
    labels - items corresponding to each linkage_matrix element 
             (If labels are given, result dendrogram x-axis will be mapped to element in labels.)
    last_merges - show only last given value merged clusters
  */
  typedef structure {
    list<list<string>> linkage_matrix;
    float dist_threshold;
    list<string> labels;
    int last_merges;
  } DendrogramParams;

  /* Ouput of the run_dendrogram function
     result_plots - List of result plot path(s)
  */
  typedef structure {
    list<string> result_plots;
  } DendrogramOutput;

  /* run_dendrogram: a wrapper method for scipy.cluster.hierarchy.dendrogram
     reference: 
     https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.dendrogram.html*/
  funcdef run_dendrogram(DendrogramParams params) returns(DendrogramOutput returnVal) authentication required;

  /***************
  persistence layer
  ***************/

  /* Input of the build_biclusters function
    ndarray_ref: NDArray object reference
    dist_threshold: the threshold to apply when forming flat clusters

    Optional arguments:
    dist_metric: The distance metric to use. Default set to 'euclidean'.
                 The distance function can be
                 ["braycurtis", "canberra", "chebyshev", "cityblock", "correlation", "cosine", 
                  "dice", "euclidean", "hamming", "jaccard", "kulsinski", "matching", 
                  "rogerstanimoto", "russellrao", "sokalmichener", "sokalsneath", "sqeuclidean", 
                  "yule"]
                 Details refer to:
                 https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html

    linkage_method: The linkage algorithm to use. Default set to 'ward'.
                    The method can be
                    ["single", "complete", "average", "weighted", "centroid", "median", "ward"]
                    Details refer to:
                    https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html

    fcluster_criterion: The criterion to use in forming flat clusters. Default set to 'distance'.
                        The criterion can be
                        ["inconsistent", "distance", "maxclust"]
                        Details refer to:
                        https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html
  */
  typedef structure{
      obj_ref ndarray_ref;
      float dist_threshold;

      string dist_metric;
      string linkage_method;
      string fcluster_criterion;
  } BuildBiclustersParams;

  /* Ouput of the build_biclusters function
    shock_id_list: list of the id of the shock node where the zipped JSON biclustering info output is stored

    JSON format:
    ["gene_id_1", "gene_id_2", "gene_id_3"]
  */
  typedef structure {
    list<string> shock_id_list;
  } BuildBiclustersOutput;

  /*
  build_biclusters: build biclusters and store result feature sets as JSON into shock
  */
  funcdef build_biclusters(BuildBiclustersParams params) returns (BuildBiclustersOutput returnVal) authentication required;

};
