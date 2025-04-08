import numpy as np

def mse_error(X: np.ndarray, centroids: np.ndarray, labels: np.ndarray) -> float:
    """
    Compute the Mean Squared Error (MSE) for a clustering problem.
    The MSE is calculated as the average of the squared Euclidean distances 
    between each data point and the centroid of its assigned cluster.
    Parameters:
    ----------
        X : np.ndarray
            A 2D array of shape (n_samples, n_features) representing the dataset.
        centroids : np.ndarray
            A 2D array of shape (n_clusters, n_features) representing the cluster centroids.
        labels : np.ndarray
            A 1D array of shape (n_samples,) where each element is the index of the 
            cluster assigned to the corresponding data point in X.
    Returns:
    -------
        float
            The mean squared error of the clustering.
    """
    
    
    mse = 0
    for i in range(len(X)):
        # Get the centroid of the assigned cluster
        centroid = centroids[labels[i]]
        # Compute the squared error manually (Euclidean distance squared)
        squared_error = np.sum((X[i] - centroid) ** 2)
        mse += squared_error

    # Average the MSE by the number of data points
    mse /= len(X)

    return mse

def euclidean_distance(x: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    """
    Compute the Euclidean distance between a point and a set of centroids.

    Parameters:
    ---------
        x (numpy.ndarray): A 1D array representing the point.
        centroids (numpy.ndarray): A 2D array where each row represents a centroid.

    Returns:
    --------
        numpy.ndarray: A 1D array containing the Euclidean distances from the point
                   to each centroid.
    """
    return np.linalg.norm(x - centroids, axis=1)