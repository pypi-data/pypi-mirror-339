
# 🧠 ParallelBrain

A biologically-inspired artificial neural network with adaptive inhibition, sparse connectivity, and sustained activity dynamics.

## Install

```bash
pip install parallel-brain
```

## Usage

```python
from parallel_brain import ParallelBrainWithAdaptiveInhibition

brain = ParallelBrainWithAdaptiveInhibition(num_neurons=10000)
brain.stimulate_neurons([0, 1, 2])
brain.propagate_signals(steps=100)
```
