import numpy as npdef cluster_indices(cluster_assignments):    n = cluster_assignments.max()    indices = []    for cluster_number in range(1, n + 1):        indices.append(np.where(cluster_assignments == cluster_number)[0])    return indicesif __name__ == "__main__":    from scipy.cluster.hierarchy import fclusterdata    # Make some test data.    data = np.random.rand(15,2)    # Compute the clusters.    cutoff = 1.0    cluster_assignments = fclusterdata(data, cutoff)    print cluster_assignments    # Print the indices of the data points in each cluster.    num_clusters = cluster_assignments.max()    print "%d clusters" % num_clusters    indices = cluster_indices(cluster_assignments)    #print indices    for k, ind in enumerate(indices):        print "cluster", k + 1, "is", ind