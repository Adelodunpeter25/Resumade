#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.auth import get_password_hash, verify_password, create_access_token, verify_token

def test_complete_auth():
    try:
        # Test with normal password
        password = "testpass123"
        hashed = get_password_hash(password)
        print("✅ Normal password hashing works")
        
        if verify_password(password, hashed):
            print("✅ Normal password verification works")
        else:
            print("❌ Normal password verification failed")
            return False
        
        # Test with long password (over 72 bytes)
        long_password = "a" * 100  # 100 character password
        hashed_long = get_password_hash(long_password)
        print("✅ Long password hashing works")
        
        # Should verify with truncated version
        if verify_password(long_password, hashed_long):
            print("✅ Long password verification works")
        else:
            print("❌ Long password verification failed")
            return False
        
        # Test JWT
        token = create_access_token(data={"sub": "test@example.com"})
        email = verify_token(token)
        if email == "test@example.com":
            print("✅ JWT token works")
        else:
            print("❌ JWT token failed")
            return False
        
        print("✅ All authentication tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

if __name__ == "__main__":
    test_complete_auth()
