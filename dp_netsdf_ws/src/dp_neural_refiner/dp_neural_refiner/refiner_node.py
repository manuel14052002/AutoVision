#!/usr/bin/env python3
"""ROS node wrapper for the local neural refiner."""

from __future__ import annotations

from typing import Optional

import rclpy
from rclpy.node import Node
import torch

from dp_msgs.msg import RefineRequest
from .refiner import LocalRefiner


class NeuralRefinerNode(Node):
    """Consume refinement requests and train local implicit models."""

    def __init__(self) -> None:
        super().__init__('neural_refiner')
        self.declare_parameter('request_topic', '/map/refine_requests')
        self.declare_parameter('device', 'cuda' if torch.cuda.is_available() else 'cpu')

        self._device = torch.device(self.get_parameter('device').value)
        self._refiner = LocalRefiner()
        self._refiner.model.to(self._device)

        request_topic = self.get_parameter('request_topic').value
        self.create_subscription(RefineRequest, request_topic, self._request_callback, 10)

    def _request_callback(self, msg: RefineRequest) -> None:
        self.get_logger().info(
            f'Received refine request id={msg.region_id} priority={msg.priority:.3f} semantic={msg.semantic_hint}'
        )
        samples = self._generate_dummy_samples(self._refiner.config.samples_per_iteration)
        targets = torch.ones(samples.shape[0], device=self._device)
        loss = self._refiner.train_on_batch(samples, targets)
        self.get_logger().info(f'Completed refinement iteration with loss {loss:.6f}')

    def _generate_dummy_samples(self, count: int) -> torch.Tensor:
        rng = torch.rand((count, 3), device=self._device) - 0.5
        return rng


def main(args: Optional[list[str]] = None) -> None:
    rclpy.init(args=args)
    node = NeuralRefinerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
