"""Tests for the business intelligence services."""

import pytest

from app.services import ml_service


def test_location_clusters_use_real_population_records():
    result = ml_service.fit_location_clusters(n_clusters=3)

    assert result["feature_columns"] == ["population"]
    assert len(result["locations"]) == len(ml_service.SAMPLE_POPULATION_DATA)
    assert all(location["cluster_label"] for location in result["locations"])
    assert result["elbow"]


def test_invalid_cluster_size_is_rejected():
    with pytest.raises(ValueError):
        ml_service.fit_location_clusters(n_clusters=1)


def test_random_forest_does_not_fabricate_target():
    result = ml_service.train_business_success_model(
        [{"location_name": "Pune", "population": 1000}]
    )

    assert result["status"] == "unavailable"
    assert "historical" in result["reason"]


def test_prediction_requires_features():
    with pytest.raises(ValueError):
        ml_service.predict_business_success({})
