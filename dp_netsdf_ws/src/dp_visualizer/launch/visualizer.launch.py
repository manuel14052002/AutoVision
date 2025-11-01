from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    config_path = get_package_share_directory('dp_visualizer') + '/rviz/dp_visualizer.rviz'
    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='dp_visualizer',
            arguments=['-d', config_path],
        ),
    ])
