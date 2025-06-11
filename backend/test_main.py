#import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Item Management API" in response.json()["message"]

def test_get_all_items():
    """Test GET /items"""
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item():
    """Test POST /items"""
    item_data = {
        "name": "Test Item",
        "quantity": 10
    }
    response = client.post("/items", json=item_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
    assert response.json()["quantity"] == 10
    assert "id" in response.json()

def test_get_item_by_id():
    """Test GET /items/{id}"""
    # First create an item
    item_data = {"name": "Test Item 2", "quantity": 5}
    create_response = client.post("/items", json=item_data)
    item_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_get_nonexistent_item():
    """Test GET /items/{id} for non-existent item"""
    response = client.get("/items/99999")
    assert response.status_code == 404

def test_update_item():
    """Test PUT /items/{id}"""
    # Create item
    item_data = {"name": "Test Item 3", "quantity": 15}
    create_response = client.post("/items", json=item_data)
    item_id = create_response.json()["id"]
    
    # Update it
    update_data = {"name": "Updated Item", "quantity": 20}
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"
    assert response.json()["quantity"] == 20

def test_partial_update_item():
    """Test partial update (only name)"""
    # Create item
    item_data = {"name": "Test Item 4", "quantity": 25}
    create_response = client.post("/items", json=item_data)
    item_id = create_response.json()["id"]
    
    # Partial update (only name)
    update_data = {"name": "Partially Updated"}
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Partially Updated"
    assert response.json()["quantity"] == 25  # Should remain unchanged

def test_delete_item():
    """Test DELETE /items/{id}"""
    # Create item
    item_data = {"name": "Test Item 5", "quantity": 30}
    create_response = client.post("/items", json=item_data)
    item_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_item():
    """Test DELETE /items/{id} for non-existent item"""
    response = client.delete("/items/99999")
    assert response.status_code == 404

def test_invalid_item_data():
    """Test validation with invalid data"""
    # Empty name
    response = client.post("/items", json={"name": "", "quantity": 10})
    assert response.status_code == 422
    
    # Negative quantity
    response = client.post("/items", json={"name": "Test", "quantity": -1})
    assert response.status_code == 422
