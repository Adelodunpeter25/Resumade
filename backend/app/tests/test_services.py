#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from decimal import Decimal
from datetime import datetime, timedelta
from app.services import InvoiceService, CustomerService, PaymentService

def test_services():
    try:
        # Test invoice number generation
        invoice_num = InvoiceService.generate_invoice_number()
        assert invoice_num.startswith("INV-")
        assert len(invoice_num) == 12  # INV- + 8 chars
        print("✅ Invoice number generation works")
        
        # Test item total calculation
        total = InvoiceService.calculate_item_total(Decimal("2.5"), Decimal("100.00"))
        assert total == Decimal("250.00")
        print("✅ Item total calculation works")
        
        # Test tax calculation
        tax = InvoiceService.calculate_tax(Decimal("100.00"))
        assert tax == Decimal("10.00")  # 10% default
        print("✅ Tax calculation works")
        
        # Test custom tax rate
        tax_custom = InvoiceService.calculate_tax(Decimal("100.00"), Decimal("0.15"))
        assert tax_custom == Decimal("15.00")  # 15% custom
        print("✅ Custom tax rate works")
        
        # Test due date calculation
        due_date = InvoiceService.set_due_date(None, 30)
        expected = datetime.now() + timedelta(days=30)
        assert abs((due_date - expected).total_seconds()) < 60  # Within 1 minute
        print("✅ Due date calculation works")
        
        # Test customer validation
        errors = CustomerService.validate_customer_data("", "invalid-email")
        assert len(errors) == 2
        print("✅ Customer validation works")
        
        # Test valid customer data
        errors = CustomerService.validate_customer_data("John Doe", "john@example.com")
        assert len(errors) == 0
        print("✅ Valid customer data passes validation")
        
        print("✅ All service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Service test failed: {e}")
        return False

if __name__ == "__main__":
    test_services()
