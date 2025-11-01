# DP-NeTSDF Research Plan

This document summarizes the objectives, hypotheses, evaluation metrics, and staged implementation plan for the DP-NeTSDF pipeline. It mirrors the system description provided in the project brief and links each research goal to the packages and scripts in this workspace skeleton.

## Objectives

- Develop a depth-uncertainty weighted TSDF backbone that fuses RealSense D435 depth frames.
- Integrate panoptic segmentation to guide dynamic masking and region prioritization.
- Train local neural implicit refiners on-demand for semantically important regions.
- Evaluate improvements in geometric accuracy, semantic consistency, and computational efficiency.

## Hypotheses

1. Depth-uncertainty weighting reduces fused noise relative to a baseline TSDF.
2. Panoptic-guided neural refinement improves detail on thin or high-value objects while maintaining near real-time throughput.
3. Instance-level dynamic masking prevents transient objects from corrupting the static map.

## Evaluation Metrics

- Chamfer distance and point-to-surface RMSE (see `tools/evaluation/eval_chamfer.py`).
- Semantic Intersection over Union (IoU) (see `tools/evaluation/eval_semantic_iou.py`).
- Instance association precision/recall (extend the dynamic manager package).
- Runtime metrics: per-frame latency, GPU utilization, and memory footprint.

## Implementation Milestones

1. **Workspace bring-up** – build custom messages (`dp_msgs`) and run preprocessing (`dp_depth_preproc`).
2. **Panoptic integration** – connect `dp_panoptic_detector` to the RealSense image stream and verify mask publication.
3. **TSDF fusion** – expand `dp_tsdf_fuser` to perform weighted updates and expose refinement queues.
4. **Dynamic filtering** – enhance `dp_dynamic_manager` to maintain static/dynamic voxel layers.
5. **Neural refinement** – implement data buffering, training scheduling, and mesh export in `dp_neural_refiner`.
6. **Visualization & logging** – configure RViz (`dp_visualizer`) and aggregate launch flows (`dp_launch`).

## Experiment Roadmap

- Perform baseline runs without uncertainty weighting for reference metrics.
- Enable uncertainty weighting and compare results across benchmark datasets (e.g., ScanNet, Replica).
- Activate panoptic-guided region selection and measure improvements on dynamic scenes.
- Introduce neural refinement, varying region sizes and iteration counts to study the quality/performance trade-off.

Use the provided Dockerfile to reproduce the environment and extend each package with production-grade functionality.
