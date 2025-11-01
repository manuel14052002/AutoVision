#!/usr/bin/env python3
"""Depth preprocessing node for DP-NeTSDF.

This node filters incoming depth frames and publishes per-pixel uncertainty
estimates to guide TSDF fusion weighting. The implementation mirrors the
prototype described in the research plan and is ready to be extended with more
sophisticated noise models.
"""

from __future__ import annotations

from typing import Optional

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class DepthPreproc(Node):
    """Apply bilateral filtering and compute simple uncertainty estimates."""

    def __init__(self) -> None:
        super().__init__('depth_preproc')
        self.declare_parameter('input_topic', '/camera/depth/image_rect_raw')
        self.declare_parameter('filtered_topic', '/camera/depth/filtered')
        self.declare_parameter('uncertainty_topic', '/camera/depth/uncertainty')
        self.declare_parameter('bilateral_diameter', 5)
        self.declare_parameter('bilateral_sigma_color', 75.0)
        self.declare_parameter('bilateral_sigma_space', 75.0)
        self.declare_parameter('uncertainty_a', 0.01)
        self.declare_parameter('uncertainty_b', 0.0003)

        self._bridge = CvBridge()
        depth_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        self._filtered_topic = self.get_parameter('filtered_topic').get_parameter_value().string_value
        self._uncertainty_topic = self.get_parameter('uncertainty_topic').get_parameter_value().string_value

        self.create_subscription(Image, depth_topic, self._depth_callback, 10)
        self._pub_filtered = self.create_publisher(Image, self._filtered_topic, 10)
        self._pub_uncertainty = self.create_publisher(Image, self._uncertainty_topic, 10)

        self.get_logger().info(f'DepthPreproc node initialized. Subscribing to {depth_topic}')

    def _depth_callback(self, msg: Image) -> None:
        depth = self._bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        depth_f32 = depth.astype(np.float32)

        diameter = int(self.get_parameter('bilateral_diameter').value)
        sigma_color = float(self.get_parameter('bilateral_sigma_color').value)
        sigma_space = float(self.get_parameter('bilateral_sigma_space').value)

        filtered = cv2.bilateralFilter(depth_f32, diameter, sigma_color, sigma_space)

        a = float(self.get_parameter('uncertainty_a').value)
        b = float(self.get_parameter('uncertainty_b').value)
        uncertainty = a + b * np.square(filtered)

        filtered_msg = self._bridge.cv2_to_imgmsg(filtered.astype(np.float32), encoding='32FC1')
        filtered_msg.header = msg.header
        uncert_msg = self._bridge.cv2_to_imgmsg(uncertainty.astype(np.float32), encoding='32FC1')
        uncert_msg.header = msg.header

        self._pub_filtered.publish(filtered_msg)
        self._pub_uncertainty.publish(uncert_msg)


def main(args: Optional[list[str]] = None) -> None:
    rclpy.init(args=args)
    node = DepthPreproc()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
