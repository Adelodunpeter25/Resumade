#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.auth import create_access_token, verify_token

def test_jwt_only():
    try:
        # Test JWT token creation
        token = create_access_token(data={"sub": "test@example.com"})
        print("✅ JWT token creation works")
        
        # Test JWT token verification
        email = verify_token(token)
        if email == "test@example.com":
            print("✅ JWT token verification works")
        else:
            print("❌ JWT token verification failed")
            return False
        
        print("✅ JWT authentication working!")
        return True
        
    except Exception as e:
        print(f"❌ JWT test failed: {e}")
        return False

if __name__ == "__main__":
    test_jwt_only()
