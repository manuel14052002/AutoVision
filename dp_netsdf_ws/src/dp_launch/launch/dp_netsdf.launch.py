from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def include(pkg: str, relative: str) -> IncludeLaunchDescription:
    path = get_package_share_directory(pkg) + relative
    return IncludeLaunchDescription(PythonLaunchDescriptionSource(path))


def generate_launch_description():
    return LaunchDescription([
        include('dp_realsense', '/launch/realsense.launch.py'),
        include('dp_depth_preproc', '/launch/depth_preproc.launch.py'),
        include('dp_panoptic_detector', '/launch/panoptic_detector.launch.py'),
        include('dp_tsdf_fuser', '/launch/tsdf_fuser.launch.py'),
        include('dp_dynamic_manager', '/launch/dynamic_manager.launch.py'),
        include('dp_neural_refiner', '/launch/neural_refiner.launch.py'),
        include('dp_visualizer', '/launch/visualizer.launch.py'),
    ])
