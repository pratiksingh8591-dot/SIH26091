"""Machine-learning services for location segmentation and business prediction.

The current project ships a small Census baseline dataset and no historical
business outcome column. Clustering can therefore run today, while the
Random Forest service deliberately stays unavailable until labelled outcomes
are supplied.
"""

from __future__ import annotations

import math
import pickle
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from app.services.population_service import SAMPLE_POPULATION_DATA

MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
CLUSTER_MODEL_PATH = MODEL_DIR / "location_kmeans.pkl"
SUCCESS_MODEL_PATH = MODEL_DIR / "business_random_forest.pkl"
RANDOM_STATE = 42


def _clean_location_records(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove invalid and duplicate location records without inventing values."""
    cleaned: List[Dict[str, Any]] = []
    seen = set()
    for record in records:
        try:
            name = str(record["location_name"]).strip()
            latitude = float(record["latitude"])
            longitude = float(record["longitude"])
            population = float(record["population"])
        except (KeyError, TypeError, ValueError):
            continue
        if not name or not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            continue
        if not math.isfinite(population) or population < 0:
            continue
        key = (name.casefold(), round(latitude, 6), round(longitude, 6))
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({**record, "population": population})
    return cleaned


def _require_sklearn():
    try:
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        from sklearn.preprocessing import StandardScaler
    except ImportError as exc:
        raise RuntimeError(
            "scikit-learn is required for analytics. Install backend requirements first."
        ) from exc
    return KMeans, silhouette_score, StandardScaler


def _cluster_label(centroid_population: float, populations: Sequence[float], rank: int, count: int) -> str:
    """Create a label from the fitted centroid, never from its cluster ID."""
    ordered = sorted(populations)
    low_cut = ordered[max(0, math.ceil(len(ordered) / 3) - 1)]
    high_cut = ordered[min(len(ordered) - 1, math.floor(len(ordered) * 2 / 3))]
    if count >= 3 and centroid_population <= low_cut:
        return "Low Population"
    if count >= 3 and centroid_population >= high_cut:
        return "High Population"
    if count >= 3:
        return "Medium Population"
    return "Lower Population" if rank == 0 else "Higher Population"


def fit_location_clusters(
    records: Optional[Iterable[Dict[str, Any]]] = None,
    n_clusters: int = 3,
) -> Dict[str, Any]:
    """Fit scaled K-Means using population from the project location dataset."""
    cleaned = _clean_location_records(records or SAMPLE_POPULATION_DATA)
    if len(cleaned) < 2:
        raise ValueError("At least two valid location records are required for clustering.")
    if not 2 <= n_clusters <= min(8, len(cleaned)):
        raise ValueError(f"n_clusters must be between 2 and {min(8, len(cleaned))}.")

    KMeans, silhouette_score, StandardScaler = _require_sklearn()
    features = [[record["population"]] for record in cleaned]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    model = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
    assignments = model.fit_predict(scaled)

    centroids = scaler.inverse_transform(model.cluster_centers_).ravel().tolist()
    rank_by_cluster = {
        cluster_id: rank
        for rank, cluster_id in enumerate(sorted(range(n_clusters), key=lambda i: centroids[i]))
    }
    labels = {
        cluster_id: _cluster_label(centroids[cluster_id], [r["population"] for r in cleaned],
                                   rank_by_cluster[cluster_id], n_clusters)
        for cluster_id in range(n_clusters)
    }

    locations = []
    for record, cluster_id in zip(cleaned, assignments):
        locations.append({
            "location_name": record["location_name"],
            "latitude": record["latitude"],
            "longitude": record["longitude"],
            "population": int(record["population"]),
            "cluster_id": int(cluster_id),
            "cluster_label": labels[int(cluster_id)],
            "explanation": (
                f"Population is {int(record['population']):,}; this location is closest "
                f"to the {labels[int(cluster_id)].lower()} centroid."
            ),
        })

    summaries = []
    for cluster_id in range(n_clusters):
        members = [location for location in locations if location["cluster_id"] == cluster_id]
        summaries.append({
            "cluster_id": cluster_id,
            "cluster_label": labels[cluster_id],
            "location_count": len(members),
            "average_population": round(sum(m["population"] for m in members) / len(members), 2)
            if members else 0,
        })

    scores: Dict[str, Optional[float]] = {"silhouette_score": None}
    if len(set(assignments)) > 1 and len(cleaned) > n_clusters:
        scores["silhouette_score"] = round(float(silhouette_score(scaled, assignments)), 4)

    elbow = []
    for candidate in range(2, min(8, len(cleaned)) + 1):
        candidate_model = KMeans(n_clusters=candidate, random_state=RANDOM_STATE, n_init=10)
        candidate_model.fit(scaled)
        elbow.append({"k": candidate, "inertia": round(float(candidate_model.inertia_), 4)})

    result = {
        "feature_columns": ["population"],
        "n_clusters": n_clusters,
        "locations": locations,
        "summaries": summaries,
        "evaluation": scores,
        "elbow": elbow,
        "limitations": [
            "The current dataset contains population and coordinates only; business potential features are not available."
        ],
    }
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with CLUSTER_MODEL_PATH.open("wb") as file:
        pickle.dump({"model": model, "scaler": scaler, "labels": labels}, file)
    return result


def load_or_fit_location_clusters(n_clusters: int = 3) -> Dict[str, Any]:
    """Return current assignments, fitting a model when no persisted model exists."""
    return fit_location_clusters(n_clusters=n_clusters)


def train_business_success_model(
    records: Iterable[Dict[str, Any]],
    target_column: Optional[str] = None,
) -> Dict[str, Any]:
    """Train a Random Forest only when a valid historical target is present."""
    rows = [row for row in records if isinstance(row, dict)]
    if not rows:
        return {"status": "unavailable", "reason": "No business records were supplied."}
    candidates = [target_column] if target_column else [
        "business_success", "success", "profitability", "survival", "business_performance"
    ]
    target = next((column for column in candidates if column and any(column in row for row in rows)), None)
    if not target:
        return {
            "status": "unavailable",
            "reason": "No historical success, profitability, survival, or performance target exists.",
            "required_data": "Labelled business outcomes linked to location features.",
        }
    raise NotImplementedError(
        "Random Forest training requires a target schema and feature dataset; "
        "the discovered target is not yet supported by this MVP."
    )


def business_model_metrics() -> Dict[str, Any]:
    """Describe model readiness without reporting fabricated evaluation metrics."""
    return {
        "status": "unavailable",
        "model_type": "Random Forest classification or regression",
        "metrics": None,
        "feature_columns": [],
        "reason": "No valid historical business outcome column is present in the project dataset.",
        "required_data": [
            "location features available before opening",
            "business category",
            "historical success/profitability/survival outcome",
            "multiple labelled businesses for train/test evaluation",
        ],
    }


def predict_business_success(features: Dict[str, Any]) -> Dict[str, Any]:
    """Return an explicit unavailable response until a validated model exists."""
    if not features:
        raise ValueError("At least one prediction feature is required.")
    return {
        **business_model_metrics(),
        "prediction": None,
        "limitations": [
            "A probability is not returned because training labels are unavailable.",
            "Do not interpret the deterministic feasibility score as a trained success probability.",
        ],
    }
