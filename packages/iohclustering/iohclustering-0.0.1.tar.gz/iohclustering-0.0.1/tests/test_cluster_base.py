import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from iohclustering import (
    create_cluster_problem,
    get_problem_id,
    get_problem,
    load_problems,
)

class TestClusterBase(unittest.TestCase):

    @patch("numpy.loadtxt")
    @patch("ioh.wrap_problem")
    def test_create_cluster_problem_with_string_dataset(self, mock_wrap_problem, mock_loadtxt):
        mock_loadtxt.return_value = np.array([[1, 2], [3, 4]])
        mock_wrap_problem.return_value = MagicMock()

        f, retransform = create_cluster_problem("iris_pca", k=2, error_metric="mse_euclidean")

        mock_loadtxt.assert_called_once_with('banchmark_datasets/iris_pca.txt', delimiter=',')
        self.assertTrue(callable(retransform))
        self.assertIsNotNone(f)

    @patch("ioh.wrap_problem")
    def test_create_cluster_problem_with_array_dataset(self, mock_wrap_problem):
        dataset = np.array([[1, 2], [3, 4]])
        mock_wrap_problem.return_value = MagicMock()

        f, retransform = create_cluster_problem(dataset, k=2, error_metric="mse_euclidean")

        self.assertTrue(callable(retransform))
        self.assertIsNotNone(f)

    def test_create_cluster_problem_invalid_error_metric(self):
        dataset = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            create_cluster_problem(dataset, k=2, error_metric="invalid_metric")

    def test_get_problem_id_valid(self):
        with patch.dict("iohclustering.cluster_base.CLUSTER_BASELINE_DATASETS", {1: "test_dataset"}):
            self.assertEqual(get_problem_id("test_dataset"), 1)

    def test_get_problem_id_invalid(self):
        with patch.dict("iohclustering.cluster_base.CLUSTER_BASELINE_DATASETS", {1: "test_dataset"}):
            with self.assertRaises(ValueError):
                get_problem_id("unknown_dataset")

    @patch("iohclustering.cluster_base.create_cluster_problem")
    def test_get_problem_valid(self, mock_create_cluster_problem):
        mock_create_cluster_problem.return_value = (MagicMock(), MagicMock())
        with patch.dict("iohclustering.cluster_base.CLUSTER_BASELINE_DATASETS", {1: "test_dataset"}):
            f, retransform = get_problem(1, instance=1, k=2)
            self.assertTrue(callable(retransform))
            self.assertIsNotNone(f)

    def test_get_problem_invalid(self):
        with self.assertRaises(ValueError):
            get_problem(0, instance=1, k=2)


    def test_retransform_function(self):
        dataset = np.array([[1, 2], [3, 4]])
        f, retransform = create_cluster_problem(dataset, k=2, error_metric="mse_euclidean")
        transformed = retransform(np.array([0.5, 0.5, 0.5, 0.5]))
        self.assertEqual(transformed.shape, (2, 2))

if __name__ == "__main__":
    unittest.main()