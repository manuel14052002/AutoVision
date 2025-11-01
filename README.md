# AutoVision

This repository now hosts the DP-NeTSDF research workspace skeleton for autonomous perception experiments. The `dp_netsdf_ws` directory contains a ROS 2 Jazzy workspace with package stubs, launch files, and evaluation utilities corresponding to the hybrid depth-weighted TSDF and neural refinement pipeline described in the research plan.

## Layout

- `dp_netsdf_ws/README.md` – workspace overview and package list.
- `dp_netsdf_ws/src` – ROS 2 packages providing message definitions, processing nodes, and launch configurations.
- `dp_netsdf_ws/tools` – evaluation scripts for geometry and semantic accuracy.
- `dp_netsdf_ws/Dockerfile` – reproducible environment setup for ROS 2 Jazzy with required Python libraries.

Refer to the individual package manifests and source files for implementation details and extend them to realize the full DP-NeTSDF system.
