#!/usr/bin/env python3
"""Dynamic instance management for DP-NeTSDF."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node

from dp_msgs.msg import PanopticMask


@dataclass
class InstanceTrack:
    instance_id: int
    semantic_id: int
    last_mask: np.ndarray


class DynamicManager(Node):
    """Track instance masks and flag moving objects."""

    def __init__(self) -> None:
        super().__init__('dynamic_manager')
        self.declare_parameter('mask_topic', '/panoptic_mask')
        self.declare_parameter('motion_threshold', 0.1)

        self._tracks: Dict[int, InstanceTrack] = {}
        self._bridge = CvBridge()

        mask_topic = self.get_parameter('mask_topic').value
        self.create_subscription(PanopticMask, mask_topic, self._mask_callback, 5)

    def _mask_callback(self, msg: PanopticMask) -> None:
        cv_mask = self._bridge.imgmsg_to_cv2(msg.mask, desired_encoding='16UC1')
        new_dynamic: list[int] = []
        for instance_id, semantic_id in zip(msg.instance_ids, msg.semantic_ids):
            binary_mask = (cv_mask == instance_id).astype(np.uint8)
            track = self._tracks.get(instance_id)
            if track is None:
                self._tracks[instance_id] = InstanceTrack(instance_id, semantic_id, binary_mask)
                continue
            displacement = self._compute_mask_displacement(track.last_mask, binary_mask)
            if displacement > float(self.get_parameter('motion_threshold').value):
                new_dynamic.append(instance_id)
            track.last_mask = binary_mask

        if new_dynamic:
            self.get_logger().info(f'Dynamic instances detected: {new_dynamic}')

    @staticmethod
    def _compute_mask_displacement(prev: np.ndarray, current: np.ndarray) -> float:
        intersection = np.logical_and(prev, current).sum()
        union = np.logical_or(prev, current).sum()
        if union == 0:
            return 0.0
        iou = intersection / union
        return 1.0 - iou


def main(args: Optional[list[str]] = None) -> None:
    rclpy.init(args=args)
    node = DynamicManager()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
