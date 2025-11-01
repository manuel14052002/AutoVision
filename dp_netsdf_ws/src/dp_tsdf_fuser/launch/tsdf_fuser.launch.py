from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dp_tsdf_fuser',
            executable='tsdf_fuser_node',
            name='tsdf_fuser',
            output='screen',
        ),
    ])
