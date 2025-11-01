from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dp_neural_refiner',
            executable='neural_refiner_node',
            name='neural_refiner',
            output='screen',
        ),
    ])
