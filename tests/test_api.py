from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_calculate_endpoint():
    payload = {
        "length_m": 10,
        "diameter_m": 0.05,
        "flow_rate_m3s": 0.002,
        "density_kgm3": 997,
        "viscosity_pas": 0.001,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pressure_drop_pa"] > 0
    assert data["reynolds_number"] > 0
