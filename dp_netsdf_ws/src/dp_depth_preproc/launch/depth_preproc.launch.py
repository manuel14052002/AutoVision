from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dp_depth_preproc',
            executable='depth_preproc_node',
            name='depth_preproc',
            output='screen',
            parameters=[{
                'input_topic': '/camera/depth/image_rect_raw',
                'filtered_topic': '/camera/depth/filtered',
                'uncertainty_topic': '/camera/depth/uncertainty',
            }],
        ),
    ])
