# jaxsne

[![build](https://github.com/erikbrinkman/jaxsne/actions/workflows/python-package.yml/badge.svg)](https://github.com/erikbrinkman/jaxsne/actions/workflows/python-package.yml)
[![pypi](https://img.shields.io/pypi/v/jaxsne)](https://pypi.org/project/jaxsne/)
[![docs](https://img.shields.io/badge/api-docs-blue)](https://erikbrinkman.github.io/jaxsne)

A library for doing dimensionality reduction in different metric spaces, or
using different distributions.

In addition to regular t-SNE for MNIST

![tsne](resources/tsne.png)

this can also be used to embed points on the sphere

![ssne](resources/ssne.gif)

or even into hierarchical hyperbolic space

![psne](resources/psne.png)

The downside is that this is generally less performant than the
[t-SNE](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html)
provided by scikit-learn, so should only be used if you want to tweak the
metrics or measures.

## Installation

```sh
pip install jaxsne
```

## Basic Usage

```py
import jaxsne

data = ... # n x d
reduced = jaxsne.sne(data)
# or
reduced = jaxsne.scaling(data)
```

## Advanced Usage

```py
import jaxsne
import jax
from jax import Array
from jax import numpy as jnp

@jax.jit
def manhattan(left: Array, right: Array) -> Array:
    return jnp.abs(left - right).sum(-1)


data = ... # n x d
reduced = jaxsne.sne(data, in_metric=manhattan, out_metric=manhattan)
```

## Development

```sh
uv run ruff format --check
uv run ruff check
uv run pyright
uv run pytest
```

## Publishing

```sh
rm -rf dist
uv build
uv publish --username __token__
```

## Tasks

- [ ] Extend to [Barnes-Hut-SNE](https://arxiv.org/abs/1301.3342)
