from backend.auth import get_password_hash, verify_password
import sys

try:
    print("Testing password hashing...")
    pwd = "testpassword"
    hashed = get_password_hash(pwd)
    print(f"Hash created: {hashed}")
    
    print("Testing password verification...")
    is_valid = verify_password(pwd, hashed)
    print(f"Verification result: {is_valid}")
    
    if is_valid:
        print("Auth module works correctly.")
    else:
        print("Auth module failed verification.")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
