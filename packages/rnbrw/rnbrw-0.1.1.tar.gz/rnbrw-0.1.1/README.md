# RNBRW

[![PyPI version](https://badge.fury.io/py/rnbrw.svg)](https://pypi.org/project/rnbrw/)

**RNBRW** (Renewal Non-Backtracking Random Walks) is a Python package for estimating edge-level importance in networks using random walks that restart upon cycle closure. These weights can be used to improve community detection algorithms like Louvain.

Based on:

> **Moradi, B.**, **Shakeri, H.**, **Poggi-Corradini, P.**, & **Higgins, M.**  
> *New methods for incorporating network cyclic structures to improve community detection*  
> [arXiv:1805.07484](https://arxiv.org/abs/1805.07484)

---

##  Installation

```bash
pip install rnbrw


## Features
- Parallel RNBRW edge weight estimation
- Seamless integration with Louvain
- Based on [Moradi-Jamei et al., 2019](https://arxiv.org/abs/1805.07484)

## Installation
```bash
pip install rnbrw
```

## Usage
```python
import networkx as nx
from rnbrw.weights import compute_weights
from rnbrw.community import detect_communities_louvain

# Create or load a graph
G = nx.karate_club_graph()

# Compute RNBRW weights
G = compute_weights(G, nsim=1000, n_jobs=4)

# Detect communities
partition = detect_communities_louvain(G)

## API Reference
- compute_weights(G, nsim=1000, n_jobs=1, weight_attr='rnbrw_weight', seed_base=0)
- Simulates RNBRW on graph G to assign edge importance scores as weights.

# Parameter	Type	Description
| Parameter     | Type            | Description                                       |
|-------------- |---------------- |--------------------------------------------------|
| G             | networkx.Graph  | Input undirected graph                           |
| nsim          | int             | Number of simulations (default = 1000)           |
| n_jobs        | int             | Number of parallel jobs (default = 1; -1 = all)  |
| weight_attr   | str             | Name of the edge attribute to store weights      |
| seed_base     | int             | Base random seed for reproducibility             |


detect_communities_louvain(G, weight_attr='rnbrw_weight')
Runs Louvain on G using edge weights.

Parameter	Type	Description
| Parameter     | Type            | Description                                  |
|-------------- |---------------- |---------------------------------------------|
| G             | networkx.Graph  | Weighted graph with edge weights            |
| weight_attr   | str             | Edge attribute name (default = 'rnbrw_weight') |

normalize_edge_weights(G, weight='rnbrw_weight')
Normalizes the weights to sum to 1 across all edges.

Parameter	Type	Description
| Parameter     | Type            | Description                                 |
|-------------- |---------------- |--------------------------------------------|
| G             | networkx.Graph  | Graph whose weights are to be normalized   |
| weight        | str             | Edge attribute to normalize (default='rnbrw_weight') |


 Citation
If you use this package in your research, please cite:


@article{moradi2018new,
  title={New methods for incorporating network cyclic structures to improve community detection},
  author={Moradi, Behnaz and Shakeri, Heman and Poggi-Corradini, Pietro and Higgins, Michael},
  journal={arXiv preprint arXiv:1805.07484},
  year={2018}
}
Or use the “Cite this repository” button above.

📄 License
This project is licensed under the MIT License © 2025 Behnaz Moradi-Jamei.
## Documentation
Full documentation is available at [Read the Docs](https://rnbrw.readthedocs.io).

