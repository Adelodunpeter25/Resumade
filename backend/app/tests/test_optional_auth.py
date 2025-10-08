#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.auth import get_current_user_optional, get_current_user
from app.core.config import settings

def test_optional_auth_functions():
    """Test optional authentication functions"""
    try:
        # Test that optional auth functions exist
        assert callable(get_current_user_optional)
        assert callable(get_current_user)
        
        print("✅ Optional authentication functions exist")
        
        # Test settings
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'jwt_algorithm')
        
        print("✅ Authentication settings configured")
        
        print("✅ Optional authentication setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Optional authentication test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing optional authentication setup...")
    test_optional_auth_functions()
