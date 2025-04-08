import hashlib
import hmac

def check_password(password: str, password_hash: str) -> bool:
    """
    Verifies a password against a SHA-256 hash with salt.
    Expected format: <salt>$<sha256 hash>

    Args:
        password (str): The plain password to verify.
        password_hash (str): The stored salt and hash in the format 'salt$hash'.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    try:
        salt, stored_hash = password_hash.split('$')
        salted_password = (salt + password).encode('utf-8')
        computed_hash = hashlib.sha256(salted_password).hexdigest()
        return hmac.compare_digest(computed_hash, stored_hash)
    except Exception:
        return False
