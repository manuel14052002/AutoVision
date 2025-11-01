#!/usr/bin/env python3
"""Chamfer distance evaluation utility for DP-NeTSDF outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import open3d as o3d


def load_mesh(path: Path) -> o3d.geometry.TriangleMesh:
    mesh = o3d.io.read_triangle_mesh(str(path))
    if not mesh.has_vertices():
        raise ValueError(f'Mesh {path} has no vertices')
    return mesh


def chamfer_distance(mesh_a: o3d.geometry.TriangleMesh, mesh_b: o3d.geometry.TriangleMesh, samples: int = 100000) -> float:
    pts_a = mesh_a.sample_points_uniformly(number_of_points=samples)
    pts_b = mesh_b.sample_points_uniformly(number_of_points=samples)
    dist_a_to_b = np.asarray(pts_a.compute_point_cloud_distance(pts_b)).mean()
    dist_b_to_a = np.asarray(pts_b.compute_point_cloud_distance(pts_a)).mean()
    return float(dist_a_to_b + dist_b_to_a)


def main() -> None:
    parser = argparse.ArgumentParser(description='Compute Chamfer distance between meshes.')
    parser.add_argument('--prediction', type=Path, required=True, help='Path to predicted mesh (PLY/OBJ).')
    parser.add_argument('--ground-truth', type=Path, required=True, help='Path to ground-truth mesh.')
    parser.add_argument('--samples', type=int, default=100000, help='Number of samples per mesh.')
    args = parser.parse_args()

    mesh_pred = load_mesh(args.prediction)
    mesh_gt = load_mesh(args.ground_truth)
    distance = chamfer_distance(mesh_pred, mesh_gt, args.samples)
    print(f'Chamfer distance: {distance:.6f}')


if __name__ == '__main__':
    main()
