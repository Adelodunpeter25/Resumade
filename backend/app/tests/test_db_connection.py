#!/usr/bin/env python3

import sys
import os
# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal, engine
from app.models import User, Customer, Invoice, InvoiceItem
from sqlalchemy import text

def test_connection():
    try:
        # Test basic connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
        # Test session and table queries
        db = SessionLocal()
        try:
            # Check if tables exist
            users_count = db.query(User).count()
            customers_count = db.query(Customer).count()
            invoices_count = db.query(Invoice).count()
            items_count = db.query(InvoiceItem).count()
            
            print(f"✅ Tables accessible:")
            print(f"   - Users: {users_count} records")
            print(f"   - Customers: {customers_count} records")
            print(f"   - Invoices: {invoices_count} records")
            print(f"   - Invoice Items: {items_count} records")
            
        finally:
            db.close()
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
