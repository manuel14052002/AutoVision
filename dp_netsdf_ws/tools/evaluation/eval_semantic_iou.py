#!/usr/bin/env python3
"""Compute semantic IoU between predicted and ground-truth voxel grids."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def load_labels(path: Path) -> np.ndarray:
    data = np.load(str(path))
    if 'labels' in data:
        return data['labels']
    return data


def semantic_iou(pred: np.ndarray, gt: np.ndarray) -> float:
    if pred.shape != gt.shape:
        raise ValueError('Predicted and ground-truth label volumes must match shape.')
    matches = pred == gt
    intersection = np.count_nonzero(matches & (gt != 0))
    union = np.count_nonzero((pred != 0) | (gt != 0))
    if union == 0:
        return 1.0
    return intersection / union


def main() -> None:
    parser = argparse.ArgumentParser(description='Compute semantic IoU for voxel grids stored in NumPy arrays.')
    parser.add_argument('--prediction', type=Path, required=True, help='Path to predicted labels .npy/.npz')
    parser.add_argument('--ground-truth', type=Path, required=True, help='Path to ground-truth labels .npy/.npz')
    args = parser.parse_args()

    pred = load_labels(args.prediction)
    gt = load_labels(args.ground_truth)
    iou = semantic_iou(pred, gt)
    print(f'Semantic IoU: {iou:.6f}')


if __name__ == '__main__':
    main()
