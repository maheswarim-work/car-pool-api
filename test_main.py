from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CarPool API"}

def test_create_carpool():
    carpool_data = {
        "driver_name": "John Doe",
        "car_model": "Toyota Camry",
        "available_seats": 3,
        "departure_time": "2024-03-20T08:00:00",
        "departure_location": "New York",
        "destination": "Boston",
        "price_per_seat": 25.50
    }
    response = client.post("/carpools", json=carpool_data)
    assert response.status_code == 200
    data = response.json()
    assert data["driver_name"] == carpool_data["driver_name"]
    assert data["car_model"] == carpool_data["car_model"]
    assert data["available_seats"] == carpool_data["available_seats"]
    assert data["departure_location"] == carpool_data["departure_location"]
    assert data["destination"] == carpool_data["destination"]
    assert data["price_per_seat"] == carpool_data["price_per_seat"]
    assert data["is_active"] == True
    assert "id" in data

def test_get_all_carpools():
    response = client.get("/carpools")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # If there are carpools
        assert all("id" in carpool for carpool in data)
        assert all("driver_name" in carpool for carpool in data)
        assert all("car_model" in carpool for carpool in data)

def test_get_specific_carpool():
    # First create a carpool
    carpool_data = {
        "driver_name": "Test Driver",
        "car_model": "Test Car",
        "available_seats": 2,
        "departure_time": "2024-03-20T09:00:00",
        "departure_location": "Test Start",
        "destination": "Test End",
        "price_per_seat": 20.00
    }
    create_response = client.post("/carpools", json=carpool_data)
    carpool_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/carpools/{carpool_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == carpool_id
    assert data["driver_name"] == carpool_data["driver_name"]

def test_get_nonexistent_carpool():
    response = client.get("/carpools/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "CarPool not found"

def test_update_carpool():
    # First create a carpool
    carpool_data = {
        "driver_name": "Original Driver",
        "car_model": "Original Car",
        "available_seats": 2,
        "departure_time": "2024-03-20T10:00:00",
        "departure_location": "Original Start",
        "destination": "Original End",
        "price_per_seat": 15.00
    }
    create_response = client.post("/carpools", json=carpool_data)
    carpool_id = create_response.json()["id"]

    # Then update it
    update_data = {
        "driver_name": "Updated Driver",
        "car_model": "Updated Car",
        "available_seats": 3,
        "departure_time": "2024-03-20T11:00:00",
        "departure_location": "Updated Start",
        "destination": "Updated End",
        "price_per_seat": 20.00
    }
    response = client.put(f"/carpools/{carpool_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == carpool_id
    assert data["driver_name"] == update_data["driver_name"]
    assert data["car_model"] == update_data["car_model"]

def test_update_nonexistent_carpool():
    update_data = {
        "driver_name": "Test Driver",
        "car_model": "Test Car",
        "available_seats": 2,
        "departure_time": "2024-03-20T12:00:00",
        "departure_location": "Test Start",
        "destination": "Test End",
        "price_per_seat": 20.00
    }
    response = client.put("/carpools/999999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "CarPool not found"

def test_delete_carpool():
    # First create a carpool
    carpool_data = {
        "driver_name": "Delete Test",
        "car_model": "Delete Car",
        "available_seats": 2,
        "departure_time": "2024-03-20T13:00:00",
        "departure_location": "Delete Start",
        "destination": "Delete End",
        "price_per_seat": 10.00
    }
    create_response = client.post("/carpools", json=carpool_data)
    carpool_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/carpools/{carpool_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "CarPool deleted successfully"

    # Verify it's deleted
    get_response = client.get(f"/carpools/{carpool_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_carpool():
    response = client.delete("/carpools/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "CarPool not found"

def test_invalid_carpool_data():
    invalid_data = {
        "driver_name": "Test",
        "car_model": "Test Car",
        "available_seats": -1,  # Invalid: negative seats
        "departure_time": "2024-03-20T14:00:00",
        "departure_location": "Test Start",
        "destination": "Test End",
        "price_per_seat": -10.00  # Invalid: negative price
    }
    response = client.post("/carpools", json=invalid_data)
    assert response.status_code == 422  # Validation error 