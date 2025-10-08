#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from decimal import Decimal
from datetime import datetime, timedelta
from app.services import InvoiceService, CustomerService, PaymentService
from app.core.auth import get_password_hash, verify_password, create_access_token, verify_token

def test_invoice_service():
    """Test InvoiceService methods"""
    # Test invoice number generation
    invoice_num = InvoiceService.generate_invoice_number()
    assert invoice_num.startswith("INV-")
    assert len(invoice_num) == 12
    
    # Test calculations
    assert InvoiceService.calculate_item_total(Decimal("2"), Decimal("50")) == Decimal("100")
    assert InvoiceService.calculate_tax(Decimal("100")) == Decimal("10")
    assert InvoiceService.calculate_total(Decimal("100"), Decimal("10")) == Decimal("110")
    
    print("✅ InvoiceService tests passed")

def test_customer_service():
    """Test CustomerService methods"""
    # Test validation
    errors = CustomerService.validate_customer_data("", "invalid")
    assert len(errors) == 2
    
    errors = CustomerService.validate_customer_data("John Doe", "john@example.com")
    assert len(errors) == 0
    
    print("✅ CustomerService tests passed")

def test_auth_functions():
    """Test authentication functions"""
    # Test password hashing
    password = "testpass123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    
    # Test JWT
    token = create_access_token({"sub": "test@example.com"})
    email = verify_token(token)
    assert email == "test@example.com"
    
    print("✅ Auth functions tests passed")

if __name__ == "__main__":
    print("Running unit tests...")
    test_invoice_service()
    test_customer_service()
    test_auth_functions()
    print("✅ All unit tests passed!")
