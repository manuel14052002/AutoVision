from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dp_dynamic_manager',
            executable='dynamic_manager_node',
            name='dynamic_manager',
            output='screen',
        ),
    ])
