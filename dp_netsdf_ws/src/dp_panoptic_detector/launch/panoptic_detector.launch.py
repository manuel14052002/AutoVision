from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dp_panoptic_detector',
            executable='panoptic_node',
            name='panoptic_detector',
            output='screen',
            parameters=[{
                'input_topic': '/camera/color/image_raw',
                'output_topic': '/panoptic_mask',
            }],
        ),
    ])
