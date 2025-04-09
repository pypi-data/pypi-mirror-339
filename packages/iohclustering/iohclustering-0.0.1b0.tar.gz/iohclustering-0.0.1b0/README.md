# IOHClustering

**IOHClustering** provides an interface for clustering problems, allowing users to map a dataset and a specified number of clusters to the IOHprofiler problem format. This enables seamless integration with the IOHprofiler framework for further analysis and performance evaluation.

As part of the IOHprofiler framework, IOHClustering is under active development. Some features may still be evolving, with potential updates to functionality and interfaces.

## Features

- Transform datasets into clustering problems compatible with the IOHprofiler framework.
- Real-world datasets for clustering, such as:
    - Iris dataset
    - Wine dataset
    - KC1 dataset
    - Glass dataset

## Installation

The minimum supported Python version is 3.10. Install IOHClustering via pip and git:

```bash
pip install iohclustering
```

## Basic Usage
### Examples and Tutorials

Below are several examples demonstrating how to use **IOHClustering** for various clustering tasks. These examples cover basic usage, working with benchmark problems, solving custom datasets, and defining custom evaluation functions.

#### Example: Clustering a Dataset

The following example shows how to get a benchmark clustering problem (by name or ID) the **IOHClustering** framework:

```python
from iohclustering import get_problem, download_benchmark_datasets

# Download benchmark datasets
download_benchmark_datasets()

# Get benchmark problem by name (e.g., "iris_pca") with k=2 clusters
clustering_problem, retransform = get_problem(fid="iris_pca", k=2)

# Alternatively, get benchmark problem by its ID (e.g., ID=5) with k=2 clusters
clustering_problem, retransform = get_problem(fid=5, k=2)

# Print metadata of the clustering problem
print(clustering_problem.meta_data)

# Set up a logger to store results in the specified directory
logger = ioh.logger.Analyzer(
    root=os.getcwd(),  # Current working directory
    folder_name="AttachedLogger",  # Folder to store logs
    algorithm_name="None",  # Name of the algorithm (can be customized)
)

# Attach the logger to the created clustering problem
clustering_problem.attach_logger(logger)

```

#### Example: Listing Available Benchmark Problems

You can retrieve a list of all benchmark problems available in **IOHClustering**:

```python
from iohclustering import load_problems

problems = load_problems()

for problem in problems.keys():
    print(problem)
```



## Tutorials

Explore the following Jupyter notebooks for step-by-step tutorials on using **IOHClustering**:
1. [Custom Dataset and Random Search Tutorial](https://github.com/IOHprofiler/IOHClustering/blob/main/tutorials/custom_dataset_random_search.ipynb): Learn how to define clustering problems with your own datasets and explore solutions using random search.
2. [Custom Metric and Random Search Tutorial](https://github.com/IOHprofiler/IOHClustering/blob/main/tutorials/custom_clustering_metric.ipynb): Understand how to define custom clustering metrics and solve clustering problems with random search.

## License

This project is licensed under a standard BSD-3 clause License. See the LICENSE file for details.


## Acknowledgments



## Cite Us

Citation information coming soon!