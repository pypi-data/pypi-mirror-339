import unittest
import numpy as np
from iohclustering import mse_error

# filepath: src/IOHClustering/test_utils_metrics.py

class TestUtilsMetrics(unittest.TestCase):

    def test_mse_error_valid_input(self):
        # Test with a valid dataset, centroids, and labels
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        centroids = np.array([[1, 2], [5, 6]])
        labels = np.array([0, 0, 1, 1])  # Assign first two points to cluster 0, last point to cluster 1
        mse = mse_error(X, centroids, labels)
        self.assertAlmostEqual(mse, 4.0, places=5)

    def test_mse_error_single_cluster(self):
        # Test with all points assigned to a single cluster
        X = np.array([[1, 2], [5, 6]])
        centroids = np.array([[3, 4]])
        labels = np.array([0, 0, 0])  # All points assigned to the single cluster
        mse = mse_error(X, centroids, labels)
        self.assertAlmostEqual(mse, 8.0, places=5)


if __name__ == "__main__":
    unittest.main()