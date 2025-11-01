from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    realsense_pkg = get_package_share_directory('realsense2_camera')
    launch_file = realsense_pkg + '/launch/rs_launch.py'
    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(launch_file)),
    ])
