import torch

class ParallelBrainWithAdaptiveInhibition:
    def __init__(self, num_neurons, avg_connections=500, decay=0.995, base_threshold=50.0):
        self.num_neurons = num_neurons
        self.decay = decay
        self.base_threshold = base_threshold

        self.potentials = torch.zeros(num_neurons, device='cuda')
        self.thresholds = torch.ones(num_neurons, device='cuda') * base_threshold
        self.refractory = torch.zeros(num_neurons, dtype=torch.int, device='cuda')
        self.firing_activity = torch.zeros(num_neurons, device='cuda')

        row_indices = torch.randint(0, num_neurons, (avg_connections * num_neurons,), device='cuda')
        col_indices = torch.arange(num_neurons, device='cuda').repeat_interleave(avg_connections)
        weights = torch.rand(avg_connections * num_neurons, device='cuda') * 0.7 + 0.7

        indices = torch.stack([row_indices, col_indices])
        self.connection_weights = torch.sparse_coo_tensor(
            indices, weights, size=(num_neurons, num_neurons), device='cuda'
        ).coalesce()

    def stimulate_neurons(self, neuron_ids, signal_strength=12.0):
        self.potentials[neuron_ids] += signal_strength

    def propagate_signals(self, steps=50):
        for step in range(steps):
            active_neurons = self.refractory == 0

            potentials_column = self.potentials.unsqueeze(1)
            if potentials_column.dim() == 1:
                potentials_column = potentials_column.unsqueeze(1)

            signals = torch.sparse.mm(self.connection_weights, potentials_column).squeeze()
            signals = signals * active_neurons
            signals = torch.clamp(signals, min=0, max=400)

            noise = torch.randn(self.potentials.size(), device='cuda') * 0.05
            self.potentials += noise

            fired_neurons = signals >= self.thresholds
            self.firing_activity = self.firing_activity * 0.9 + fired_neurons.float() * 0.1

            overactive_neurons = self.firing_activity > 0.30
            self.potentials[overactive_neurons] *= 0.92
            self.thresholds[overactive_neurons] *= 1.015

            self.refractory = torch.where(
                fired_neurons,
                torch.randint(2, 5, (self.num_neurons,), device='cuda'),
                torch.clamp(self.refractory - 1, min=0)
            )

            firing_rate = torch.mean(fired_neurons.float()).item()
            if firing_rate < 0.1:
                self.thresholds *= 0.995
            else:
                self.thresholds = torch.where(
                    self.firing_activity > 0.2,
                    self.thresholds * 1.001,
                    self.thresholds * 0.999
                )

            self.thresholds = torch.clamp(self.thresholds, min=40.0, max=68.0)
            decay_factor = 0.995 if firing_rate > 0.12 else 0.998
            self.connection_weights = self.connection_weights * decay_factor

            inactive_neurons = self.potentials < 4.0
            self.potentials[inactive_neurons] += 3.2
            self.potentials = self.potentials * self.decay + 0.4
            self.potentials = torch.clamp(self.potentials, min=0.0, max=45.0)

            max_signal = torch.max(signals).item()
            mean_signal = torch.mean(signals).item()
            max_threshold = torch.max(self.thresholds).item()
            print(f"Step {step + 1}/{steps} | Mean Signal: {mean_signal:.2f}, "
                  f"Max Signal: {max_signal:.2f}, Max Threshold: {max_threshold:.2f}, Neurons Fired: {fired_neurons.sum().item()}")

            if torch.max(self.potentials) == 0:
                print("⚠️ All neurons have zero potential! Adjust stimulation or decay rates.")
                break
