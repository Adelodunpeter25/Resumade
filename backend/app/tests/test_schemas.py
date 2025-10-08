#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.schemas import UserCreate, CustomerCreate, InvoiceCreate, InvoiceItemCreate
from decimal import Decimal
from datetime import datetime

def test_schemas():
    try:
        # Test UserCreate schema
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "password123"
        }
        user = UserCreate(**user_data)
        print("✅ UserCreate schema validation passed")
        
        # Test CustomerCreate schema
        customer_data = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "address": "123 Test St",
            "phone": "+1234567890"
        }
        customer = CustomerCreate(**customer_data)
        print("✅ CustomerCreate schema validation passed")
        
        # Test InvoiceItemCreate schema
        item_data = {
            "description": "Test Item",
            "quantity": Decimal("2.00"),
            "unit_price": Decimal("50.00")
        }
        item = InvoiceItemCreate(**item_data)
        print("✅ InvoiceItemCreate schema validation passed")
        
        # Test InvoiceCreate schema
        invoice_data = {
            "customer_id": 1,
            "due_date": datetime.now(),
            "items": [item_data]
        }
        invoice = InvoiceCreate(**invoice_data)
        print("✅ InvoiceCreate schema validation passed")
        
        print("✅ All schema validations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False

if __name__ == "__main__":
    test_schemas()
