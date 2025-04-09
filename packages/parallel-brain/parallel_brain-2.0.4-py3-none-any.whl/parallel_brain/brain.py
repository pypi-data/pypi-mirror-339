import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class ParallelBrainWithAdaptiveInhibition(nn.Module):
    def __init__(
    self,
    num_neurons=10000,
    avg_connections=500,
    inhibitory_ratio=0.2,
    firing_threshold=50.0,
    decay=0.95,
    noise_std=0.01,
    device='cpu'     # ✅ THIS LINE
):

        super().__init__()
        self.num_neurons = num_neurons
        self.device = device
        self.firing_threshold = firing_threshold
        self.decay = decay
        self.noise_std = noise_std

        # Create sparse connectivity
        self.connections = torch.zeros(num_neurons, avg_connections, dtype=torch.long)
        self.weights = torch.randn(num_neurons, avg_connections) * 0.1

        for i in range(num_neurons):
            self.connections[i] = torch.from_numpy(
                np.random.choice(num_neurons, avg_connections, replace=False)
            )

        # Inhibitory neurons
        self.inhibitory_mask = torch.rand(num_neurons) < inhibitory_ratio
        self.inhibitory_mask = self.inhibitory_mask.float().to(device)

        # Dynamic variables
        self.potentials = torch.zeros(num_neurons, device=device)
        self.fired = torch.zeros(num_neurons, device=device)

        # Adaptive thresholds
        self.adaptive_thresholds = torch.ones(num_neurons, device=device) * firing_threshold

    def forward(self, external_input, steps=10, verbose=False):
        for step in range(steps):
            # Apply decay
            self.potentials *= self.decay

            # Inject noise
            noise = torch.randn_like(self.potentials) * self.noise_std
            self.potentials += noise

            # Inject external input only in step 0
            if step == 0:
                self.potentials += external_input.to(self.device)

            # Neurons that fire
            self.fired = (self.potentials >= self.adaptive_thresholds).float()

            # Adjust thresholds based on firing
            self.adaptive_thresholds += self.fired * 0.5
            self.adaptive_thresholds -= 0.1
            self.adaptive_thresholds = torch.clamp(self.adaptive_thresholds, min=1.0, max=100.0)

            # Signal propagation
            postsynaptic_input = torch.zeros(self.num_neurons, device=self.device)
            for i in range(self.num_neurons):
                targets = self.connections[i].to(self.device)
                weights = self.weights[i].to(self.device)
                signal = self.fired[i] * weights
                postsynaptic_input[targets] += signal

            # Apply inhibition
            inhibition = self.inhibitory_mask * postsynaptic_input
            excitation = (1 - self.inhibitory_mask) * postsynaptic_input
            net_input = excitation - inhibition

            self.potentials += net_input

            if verbose:
                print(f"Step {step+1}/{steps} | Mean Signal: {net_input.mean():.2f}, "
                      f"Max Signal: {net_input.max():.2f}, Max Threshold: {self.adaptive_thresholds.max():.2f}, "
                      f"Neurons Fired: {int(self.fired.sum().item())}")

        return self.potentials.detach()

    def reset_state(self):
        self.potentials.zero_()
        self.fired.zero_()
