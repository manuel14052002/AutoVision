# DP-NeTSDF Tools

The `evaluation` folder contains standalone Python utilities for computing the primary metrics described in the research plan:

- `eval_chamfer.py` – computes Chamfer distance between reconstructed and ground-truth meshes using Open3D.
- `eval_semantic_iou.py` – evaluates semantic IoU between predicted and ground-truth voxel label volumes stored as NumPy arrays.

Extend this directory with additional logging, plotting, and benchmarking scripts as experiments mature.
