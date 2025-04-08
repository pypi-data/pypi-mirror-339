import causally.scm.scm as scm
import causally.graph.random_graph as rg
import causally.scm.noise as noise
import causally.scm.causal_mechanism as cm
from causally.scm.context import SCMContext
from causally.utils.graph import topological_order
import numpy as np
import random

SEED = 42
np.random.seed(SEED)
random.seed(42)

# Erdos-Renyi graph generator
graph_generator = rg.ErdosRenyi(num_nodes=10, expected_degree=2)

# Generator of the noise terms
noise_generator = noise.MLPNoise()

# Nonlinear causal mechanisms (parametrized with a random neural network)
causal_mechanism = cm.NeuralNetMechanism()

# Context for the assumptions
context = SCMContext()

# Make assumption: confounded model
context.confounded_model(p_confounder=0.1)

# Make assumption: unfaithful model
context.unfaithful_model(p_unfaithful=1)

# Generate the data
model = scm.AdditiveNoiseModel(
        num_samples=1000,
        graph_generator=graph_generator,
        noise_generator=noise_generator,
        causal_mechanism=causal_mechanism,
        scm_context=context,
        seed=42
)

# Sample from the model
dataset, groundtruth = model.sample()
print([int(i) for i in topological_order(model.adjacency)])
