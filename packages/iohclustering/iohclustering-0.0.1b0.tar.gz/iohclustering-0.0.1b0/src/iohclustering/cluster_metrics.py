
import numpy as np
import typing
from .utils_metrics import euclidean_distance, mse_error

def compute_labels(
        X: np.ndarray, 
        centroids: np.ndarray, 
        distance_function: typing.Callable = euclidean_distance
    ):
    """
    Compute the labels for each data point based on the closest centroid.

    Parameters:
    - X: numpy array of shape (m, n), where m is the number of data points and n is the dimensionality of the data.
    - centroids: numpy array of shape (k, n), where k is the number of clusters and n is the dimensionality of the centroids.

    Returns:
    - labels: numpy array of shape (m,), where each element is the index of the closest centroid for each data point.
    """
    # Initialize an array to store the labels (cluster assignments)
    labels = np.zeros(len(X), dtype=int)

    # Calculate labels (assign closest centroid to each data point)
    for i in range(len(X)):
        # Compute the distance between the point and each centroid
        distances = distance_function(X[i], centroids)
        # Assign the label as the index of the closest centroid
        labels[i] = np.argmin(distances)

    return labels


def general_cluster_metric(
    distance_function: typing.Callable[[np.ndarray, np.ndarray], np.ndarray] = euclidean_distance, 
    error_function: typing.Callable[[np.ndarray, np.ndarray, np.ndarray[np.int_]], float] = mse_error
    ) -> typing.Callable[[np.ndarray, np.ndarray], float]:
    """
    Creates a general clustering metric function based on the provided distance and error functions.

    Parameters:
    --------
        distance_function (Callable, optional): A function to compute the distance between 
            data points and centroids. Defaults to `euclidean_distance`.
        error_function (Callable, optional): A function to compute the clustering error 
            based on the dataset, centroids, and labels. Defaults to `mse_error`.

    Returns:
    --------
        Callable[[np.ndarray, np.ndarray], float]: A function that computes the clustering metric.
    """
    def metric(X: np.ndarray, centroids: np.ndarray) -> float:
        labels = compute_labels(X, centroids, distance_function)
        return error_function(X, centroids, labels)
    
    return metric



CLUSTER_METRICS = {
    "mse_euclidean": general_cluster_metric(euclidean_distance, mse_error),
}
