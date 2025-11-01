#!/usr/bin/env python3
"""Prototype TSDF fusion node for DP-NeTSDF."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import open3d as o3d
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

from dp_msgs.msg import PanopticMask, RefineRequest, TSDFMeta


@dataclass
class CameraIntrinsics:
    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int

    def to_o3d(self) -> o3d.camera.PinholeCameraIntrinsic:
        intrinsic = o3d.camera.PinholeCameraIntrinsic()
        intrinsic.set_intrinsics(self.width, self.height, self.fx, self.fy, self.cx, self.cy)
        return intrinsic


class SimpleTSDFFuser(Node):
    """Fuse filtered depth frames into a scalable TSDF volume."""

    def __init__(self) -> None:
        super().__init__('simple_tsdf_fuser')
        self.declare_parameter('depth_topic', '/camera/depth/filtered')
        self.declare_parameter('uncertainty_topic', '/camera/depth/uncertainty')
        self.declare_parameter('mask_topic', '/panoptic_mask')
        self.declare_parameter('voxel_length', 0.03)
        self.declare_parameter('sdf_trunc', 0.06)
        self.declare_parameter('camera_frame', 'camera_color_optical_frame')
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('publish_interval', 2.0)

        self._bridge = CvBridge()
        depth_topic = self.get_parameter('depth_topic').value
        mask_topic = self.get_parameter('mask_topic').value
        uncertainty_topic = self.get_parameter('uncertainty_topic').value

        self._tsdf = o3d.pipelines.integration.ScalableTSDFVolume(
            voxel_length=float(self.get_parameter('voxel_length').value),
            sdf_trunc=float(self.get_parameter('sdf_trunc').value),
            color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8,
        )

        self._latest_mask: Optional[np.ndarray] = None
        self._latest_uncertainty: Optional[np.ndarray] = None
        self._camera_intrinsics = CameraIntrinsics(525.0, 525.0, 319.5, 239.5, 640, 480)

        self.create_subscription(Image, depth_topic, self._depth_callback, 5)
        self.create_subscription(Image, uncertainty_topic, self._uncertainty_callback, 5)
        self.create_subscription(PanopticMask, mask_topic, self._mask_callback, 5)

        self._meta_pub = self.create_publisher(TSDFMeta, '/map/tsdf_meta', 1)
        self._refine_pub = self.create_publisher(RefineRequest, '/map/refine_requests', 10)

        timer_period = float(self.get_parameter('publish_interval').value)
        self.create_timer(timer_period, self._publish_meta)

    def _uncertainty_callback(self, msg: Image) -> None:
        self._latest_uncertainty = self._bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')

    def _mask_callback(self, msg: PanopticMask) -> None:
        self._latest_mask = self._bridge.imgmsg_to_cv2(msg.mask, desired_encoding='16UC1')

    def _depth_callback(self, msg: Image) -> None:
        depth = self._bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')
        rgb_image = np.zeros((depth.shape[0], depth.shape[1], 3), dtype=np.uint8)
        depth_mm = (depth * 1000.0).astype(np.uint16)
        depth_o3d = o3d.geometry.Image(depth_mm)
        rgb_o3d = o3d.geometry.Image(rgb_image)
        intrinsic = self._camera_intrinsics.to_o3d()
        extrinsic = np.eye(4)

        self._tsdf.integrate(rgb_o3d, depth_o3d, intrinsic, extrinsic)
        self._maybe_enqueue_refinement(depth)

    def _publish_meta(self) -> None:
        msg = TSDFMeta()
        msg.header.frame_id = self.get_parameter('map_frame').value
        msg.voxel_size = float(self.get_parameter('voxel_length').value)
        msg.truncation_distance = float(self.get_parameter('sdf_trunc').value)
        msg.resolution_x = 0.0
        msg.resolution_y = 0.0
        msg.resolution_z = 0.0
        self._meta_pub.publish(msg)

    def _maybe_enqueue_refinement(self, depth: np.ndarray) -> None:
        if self._latest_mask is None or self._latest_uncertainty is None:
            return

        uncertainty = self._latest_uncertainty
        if uncertainty.size == 0:
            return

        score = float(np.mean(uncertainty))
        if score < 0.05:
            return

        request = RefineRequest()
        request.header.frame_id = self.get_parameter('map_frame').value
        request.region_center.x = 0.0
        request.region_center.y = 0.0
        request.region_center.z = 0.0
        request.region_size = 0.5
        request.region_id = 0
        request.priority = score
        request.semantic_hint = 'general'
        self._refine_pub.publish(request)


def main(args: Optional[list[str]] = None) -> None:
    rclpy.init(args=args)
    node = SimpleTSDFFuser()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
