import hashlib
import os

def create_password_hash(password: str, salt: str = None) -> str:
    if not salt:
        salt = os.urandom(8).hex()
    salted_password = (salt + password).encode('utf-8')
    hashed = hashlib.sha256(salted_password).hexdigest()
    return f"{salt}${hashed}"

if __name__ == "__main__":
    import sys
    print(create_password_hash(sys.argv[1]))
