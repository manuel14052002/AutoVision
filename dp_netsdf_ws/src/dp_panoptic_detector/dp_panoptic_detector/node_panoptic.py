#!/usr/bin/env python3
"""Panoptic segmentation node stub using the Ultralytics YOLO segmentation model."""

from __future__ import annotations

from typing import Optional

import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image

try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover - ultralytics might not be installed in CI
    YOLO = None

from dp_msgs.msg import PanopticMask


class PanopticDetector(Node):
    """Perform lightweight panoptic segmentation and publish mask metadata."""

    def __init__(self) -> None:
        super().__init__('panoptic_detector')
        self.declare_parameter('input_topic', '/camera/color/image_raw')
        self.declare_parameter('output_topic', '/panoptic_mask')
        self.declare_parameter('model_path', 'yolov8n-seg.pt')
        self.declare_parameter('confidence', 0.25)
        self.declare_parameter('imgsz', 640)

        self._bridge = CvBridge()
        input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        self._output_topic = self.get_parameter('output_topic').get_parameter_value().string_value
        self._confidence = float(self.get_parameter('confidence').value)
        self._imgsz = int(self.get_parameter('imgsz').value)

        model_path = self.get_parameter('model_path').get_parameter_value().string_value
        if YOLO is None:
            self.get_logger().warning('Ultralytics is not installed. Panoptic detector will not run predictions.')
            self._model = None
        else:
            self.get_logger().info(f'Loading YOLO model from {model_path}')
            self._model = YOLO(model_path)

        self.create_subscription(Image, input_topic, self._image_callback, 5)
        self._publisher = self.create_publisher(PanopticMask, self._output_topic, 5)

    def _image_callback(self, msg: Image) -> None:
        image = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        if self._model is None:
            mask_msg = self._empty_mask(msg)
            self._publisher.publish(mask_msg)
            return

        results = self._model.predict(source=image, imgsz=self._imgsz, conf=self._confidence, verbose=False)
        result = results[0]

        mask = np.zeros(image.shape[:2], dtype=np.uint16)
        class_names: list[str] = []
        instance_ids: list[int] = []
        semantic_ids: list[int] = []

        if result.masks is not None:
            for index, (segmentation, box) in enumerate(zip(result.masks.data.cpu().numpy(), result.boxes)):
                instance_id = index + 1
                mask[segmentation > 0.5] = instance_id
                class_index = int(box.cls.item()) if box.cls is not None else -1
                class_name = result.names.get(class_index, 'unknown') if class_index >= 0 else 'unknown'
                class_names.append(class_name)
                instance_ids.append(instance_id)
                semantic_ids.append(class_index)

        panoptic_msg = PanopticMask()
        panoptic_msg.header = msg.header
        panoptic_msg.mask = self._bridge.cv2_to_imgmsg(mask, encoding='16UC1')
        panoptic_msg.class_names = class_names
        panoptic_msg.instance_ids = instance_ids
        panoptic_msg.semantic_ids = semantic_ids
        self._publisher.publish(panoptic_msg)

    def _empty_mask(self, msg: Image) -> PanopticMask:
        mask_msg = PanopticMask()
        mask_msg.header = msg.header
        zeros = np.zeros((msg.height, msg.width), dtype=np.uint16)
        mask_msg.mask = self._bridge.cv2_to_imgmsg(zeros, encoding='16UC1')
        mask_msg.class_names = []
        mask_msg.instance_ids = []
        mask_msg.semantic_ids = []
        return mask_msg


def main(args: Optional[list[str]] = None) -> None:
    rclpy.init(args=args)
    node = PanopticDetector()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
