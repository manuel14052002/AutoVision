"""Minimal neural implicit model definitions for DP-NeTSDF."""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn as nn


def _make_mlp(in_channels: int, hidden_dim: int, num_layers: int) -> nn.Sequential:
    layers = []
    for i in range(num_layers):
        in_dim = in_channels if i == 0 else hidden_dim
        layers.append(nn.Linear(in_dim, hidden_dim))
        layers.append(nn.ReLU(inplace=True))
    return nn.Sequential(*layers)


class TinyLocalNeRF(nn.Module):
    """A lightweight implicit model for local neural refinement."""

    def __init__(self, hidden_dim: int = 128, num_layers: int = 4) -> None:
        super().__init__()
        self.backbone = _make_mlp(3, hidden_dim, num_layers)
        self.density_head = nn.Linear(hidden_dim, 1)
        self.color_head = nn.Linear(hidden_dim, 3)

    def forward(self, points: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        features = self.backbone(points)
        sigma = torch.relu(self.density_head(features))
        color = torch.sigmoid(self.color_head(features))
        return sigma, color


@dataclass
class RefinementConfig:
    iterations: int = 200
    samples_per_iteration: int = 2048
    learning_rate: float = 5e-4


class LocalRefiner:
    """Training loop skeleton for local neural refinement."""

    def __init__(self, config: RefinementConfig | None = None) -> None:
        self.config = config or RefinementConfig()
        self.model = TinyLocalNeRF()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config.learning_rate)

    def train_on_batch(self, samples: torch.Tensor, targets: torch.Tensor) -> float:
        self.model.train()
        sigma, _ = self.model(samples)
        loss = torch.nn.functional.l1_loss(sigma.squeeze(-1), targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return float(loss.item())
