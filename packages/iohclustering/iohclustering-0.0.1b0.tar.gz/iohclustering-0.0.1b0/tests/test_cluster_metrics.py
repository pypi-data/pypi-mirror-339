import unittest
import numpy as np
from unittest.mock import patch, MagicMock

# filepath: src/IOHClustering/test_cluster_metrics.py
from iohclustering import (
    euclidean_distance, 
    mse_error,
    compute_labels,
    general_cluster_metric,
    CLUSTER_METRICS,
)


class TestClusterMetrics(unittest.TestCase):

    def test_compute_labels(self):
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        centroids = np.array([[1, 2], [5, 6]])
        labels = compute_labels(X, centroids, euclidean_distance)
        self.assertTrue(np.array_equal(labels, [0, 0, 1, 1]))

    def test_general_cluster_metric(self):
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        centroids = np.array([[1, 2], [5, 6]])

        metric_function = general_cluster_metric(euclidean_distance, mse_error)
        result = metric_function(X, centroids)

        self.assertEqual(result, 4.0)

    def test_general_cluster_metric_default(self):
        metric_function = general_cluster_metric()
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        centroids = np.array([[1, 2], [5, 6]])
        result = metric_function(X, centroids)
        self.assertGreaterEqual(result, 0)
        self.assertAlmostEqual(result, 4.0)

    def test_cluster_metrics_dict(self):
        self.assertIn("mse_euclidean", CLUSTER_METRICS)
        metric_function = CLUSTER_METRICS["mse_euclidean"]
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        centroids = np.array([[1, 2], [5, 6]])
        result = metric_function(X, centroids)
        self.assertGreaterEqual(result, 0)
        self.assertAlmostEqual(result, 4.0)


if __name__ == "__main__":
    unittest.main()