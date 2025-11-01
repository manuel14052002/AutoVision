# DP-NeTSDF Workspace Skeleton

This directory contains a ROS 2 Jazzy workspace layout for the DP-NeTSDF research prototype described in the accompanying plan. It provides package stubs, launch files, and evaluation utilities required to begin implementing the hybrid TSDF and neural refinement system.

## Workspace Contents

- `src/dp_msgs`: Custom ROS message definitions.
- `src/dp_depth_preproc`: Depth preprocessing node (Python).
- `src/dp_panoptic_detector`: Panoptic segmentation node (Python).
- `src/dp_realsense`: Launch wrappers for Intel RealSense cameras.
- `src/dp_tsdf_fuser`: TSDF fusion node stub (Python/Open3D).
- `src/dp_dynamic_manager`: Dynamic instance masking node stub (Python).
- `src/dp_neural_refiner`: Local neural implicit refiner skeleton (Python/PyTorch).
- `src/dp_visualizer`: RViz configuration and visualization helpers.
- `src/dp_launch`: Aggregate launch files for orchestrating the stack.
- `tools`: Evaluation scripts and experiment utilities.

Follow the README files inside each package for build and usage instructions.
