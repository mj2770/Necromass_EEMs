from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass
class RegionWindow:
    name: str
    ex_min: float
    ex_max: float
    em_min: float
    em_max: float


DEFAULT_WINDOWS = [
    RegionWindow("protein_humic_overlap_seed", 250, 300, 380, 450),
    RegionWindow("bacteria_like_seed", 250, 350, 310, 370),
]


def _nearest_index(axis: list[float], target: float) -> int:
    return min(range(len(axis)), key=lambda idx: abs(axis[idx] - target))


def nearest_signal(eem: list[list[float]], ex: list[float], em: list[float], ex_target: float, em_target: float) -> float:
    ex_idx = _nearest_index(ex, ex_target)
    em_idx = _nearest_index(em, em_target)
    return float(eem[ex_idx][em_idx])


def regional_sum(eem: list[list[float]], ex: list[float], em: list[float], window: RegionWindow) -> float:
    ex_indices = [idx for idx, value in enumerate(ex) if window.ex_min <= value <= window.ex_max]
    em_indices = [idx for idx, value in enumerate(em) if window.em_min <= value <= window.em_max]
    total = 0.0
    for ex_idx in ex_indices:
        for em_idx in em_indices:
            total += eem[ex_idx][em_idx]
    return total


def build_feature_row(sample_name: str, eem: list[list[float]], ex: list[float], em: list[float]) -> dict:
    feature_row = {
        "sample_name": sample_name,
        "peak_350_450": nearest_signal(eem, ex, em, 350, 450),
    }
    for window in DEFAULT_WINDOWS:
        feature_row[f"sum_{window.name}"] = regional_sum(eem, ex, em, window)
    return feature_row


def _feature_columns(feature_rows: list[dict]) -> list[str]:
    return [key for key in feature_rows[0] if key != "sample_name"]


def _distance(row_a: dict, row_b: dict, columns: list[str]) -> float:
    return sqrt(sum((float(row_a[col]) - float(row_b[col])) ** 2 for col in columns))


def cluster_feature_table(feature_rows: list[dict], n_clusters: int = 3, max_iter: int = 20) -> list[dict]:
    if not feature_rows:
        return []

    n_clusters = max(1, min(n_clusters, len(feature_rows)))
    columns = _feature_columns(feature_rows)
    centroids = [dict(feature_rows[idx]) for idx in range(n_clusters)]

    for _ in range(max_iter):
        assignments: list[int] = []
        for row in feature_rows:
            distances = [_distance(row, centroid, columns) for centroid in centroids]
            assignments.append(distances.index(min(distances)))

        new_centroids: list[dict] = []
        for cluster_idx in range(n_clusters):
            members = [row for row, assigned in zip(feature_rows, assignments) if assigned == cluster_idx]
            if not members:
                new_centroids.append(dict(centroids[cluster_idx]))
                continue
            centroid = {"sample_name": f"cluster_{cluster_idx}"}
            for column in columns:
                centroid[column] = sum(float(member[column]) for member in members) / len(members)
            new_centroids.append(centroid)

        if all(_distance(old, new, columns) < 1e-9 for old, new in zip(centroids, new_centroids)):
            centroids = new_centroids
            break
        centroids = new_centroids

    clustered_rows = []
    for row in feature_rows:
        distances = [_distance(row, centroid, columns) for centroid in centroids]
        clustered_rows.append({**row, "cluster_label": distances.index(min(distances))})
    return clustered_rows
