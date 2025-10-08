#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.models import User, Customer, Invoice

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_auth_flow():
    """Test complete authentication flow"""
    # Test signup
    signup_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    
    response = client.post("/api/auth/signup", json=signup_data)
    assert response.status_code == 201
    assert "access_token" in response.json()
    
    token = response.json()["access_token"]
    
    # Test login
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    # Test protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    
    return token

def test_customer_crud():
    """Test customer CRUD operations"""
    token = test_auth_flow()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create customer
    customer_data = {
        "name": "Test Customer",
        "email": "customer@example.com",
        "address": "123 Test St",
        "phone": "+1234567890"
    }
    
    response = client.post("/api/customers/", json=customer_data, headers=headers)
    assert response.status_code == 200
    customer_id = response.json()["id"]
    
    # Get customer
    response = client.get(f"/api/customers/{customer_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Customer"
    
    # Update customer
    update_data = {"name": "Updated Customer"}
    response = client.put(f"/api/customers/{customer_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Customer"
    
    return customer_id, headers

def test_invoice_crud():
    """Test invoice CRUD operations"""
    customer_id, headers = test_customer_crud()
    
    # Create invoice
    invoice_data = {
        "customer_id": customer_id,
        "status": "draft",
        "items": [
            {
                "description": "Test Item",
                "quantity": 2.0,
                "unit_price": 50.0
            }
        ]
    }
    
    response = client.post("/api/invoices/", json=invoice_data, headers=headers)
    assert response.status_code == 200
    invoice = response.json()
    assert invoice["subtotal"] == 100.0
    assert invoice["tax_amount"] == 10.0
    assert invoice["total_amount"] == 110.0
    
    invoice_id = invoice["id"]
    
    # Mark as paid
    response = client.put(f"/api/invoices/{invoice_id}/mark-paid", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "paid"

def test_analytics():
    """Test analytics endpoints"""
    _, headers = test_customer_crud()
    
    # Revenue summary
    response = client.get("/api/analytics/revenue-summary", headers=headers)
    assert response.status_code == 200
    assert "total_invoiced" in response.json()
    
    # Aging report
    response = client.get("/api/analytics/aging-report", headers=headers)
    assert response.status_code == 200
    assert "current" in response.json()

def test_error_handling():
    """Test error handling"""
    # Test 404
    response = client.get("/api/customers/999999")
    assert response.status_code == 401  # Unauthorized (no token)
    
    # Test invalid login
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

if __name__ == "__main__":
    print("Running integration tests...")
    test_auth_flow()
    print("✅ Auth flow test passed")
    
    test_customer_crud()
    print("✅ Customer CRUD test passed")
    
    test_invoice_crud()
    print("✅ Invoice CRUD test passed")
    
    test_analytics()
    print("✅ Analytics test passed")
    
    test_error_handling()
    print("✅ Error handling test passed")
    
    print("✅ All integration tests passed!")
    
    # Cleanup
    os.remove("test.db")
