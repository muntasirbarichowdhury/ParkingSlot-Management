from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# 1. GET all parking slots - successful
def test_get_all_parking_slots():
    response = client.get("/parking-slots")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 2. GET single parking slot - successful
def test_get_single_parking_slot():
    slot_data = {
        "id": 101,
        "title": "Parking Slot B-01",
        "description": "First floor near elevator",
        "status": "available",
        "priority": "low",
    }
    client.post("/parking-slots", json=slot_data)

    response = client.get("/parking-slots/101")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 101
    assert data["title"] == "Parking Slot B-01"


# 3. POST/create parking slot - successful
def test_create_parking_slot():
    slot_data = {
        "id": 102,
        "title": "Parking Slot C-05",
        "description": "Second floor VIP section",
        "status": "occupied",
        "priority": "high",
    }
    response = client.post("/parking-slots", json=slot_data)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["id"] == 102
    assert data["status"] == "occupied"


# 4. PUT/update parking slot - successful
def test_update_parking_slot():
    slot_data = {
        "id": 103,
        "title": "Parking Slot D-10",
        "description": "Basement level 1",
        "status": "available",
        "priority": "medium",
    }
    client.post("/parking-slots", json=slot_data)

    update_data = {
        "id": 103,
        "title": "Parking Slot D-10 Updated",
        "description": "Basement level 1 near exit",
        "status": "occupied",
        "priority": "high",
    }
    response = client.put("/parking-slots/103", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Parking Slot D-10 Updated"
    assert data["status"] == "occupied"


# 5. DELETE parking slot - successful
def test_delete_parking_slot():
    slot_data = {
        "id": 104,
        "title": "Parking Slot E-01",
        "description": "Outdoor lot",
        "status": "available",
        "priority": "low",
    }
    client.post("/parking-slots", json=slot_data)

    response = client.delete("/parking-slots/104")
    assert response.status_code in (200, 204)

    # Verify deletion
    get_resp = client.get("/parking-slots/104")
    assert get_resp.status_code == 404


# 6. GET non-existing slot - invalid scenario, expect 404
def test_get_non_existing_slot():
    response = client.get("/parking-slots/999999")
    assert response.status_code == 404


# 7. POST duplicate ID - invalid scenario, expect 400
def test_create_duplicate_id():
    slot_data = {
        "id": 201,
        "title": "Parking Slot F-01",
        "description": "Ground floor",
        "status": "available",
        "priority": "medium",
    }
    client.post("/parking-slots", json=slot_data)

    # Attempt duplicate POST with same ID
    response = client.post("/parking-slots", json=slot_data)
    assert response.status_code == 400


# 8. Invalid status or priority - invalid scenario, expect 422
def test_invalid_status():
    invalid_data = {
        "id": 301,
        "title": "Parking Slot G-01",
        "description": "Test Slot",
        "status": "reserved",  # Invalid (only 'available' or 'occupied' allowed)
        "priority": "high",
    }
    response = client.post("/parking-slots", json=invalid_data)
    assert response.status_code == 422


def test_invalid_priority():
    invalid_data = {
        "id": 302,
        "title": "Parking Slot G-02",
        "description": "Test Slot",
        "status": "available",
        "priority": "super_high",  # Invalid (only 'low', 'medium', 'high' allowed)
    }
    response = client.post("/parking-slots", json=invalid_data)
    assert response.status_code == 422
