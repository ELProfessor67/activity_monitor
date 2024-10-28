import os
import secrets

def generate_random_key(length=32):
    """Generate a random key of specified length."""
    return secrets.token_hex(length)

def check_or_create_key(file_path='server.key'):
    """Check for the server.key file. Create a new key if it does not exist."""
    if os.path.exists(file_path):
        # If the file exists, read the key from it
        with open(file_path, 'r') as key_file:
            key = key_file.read().strip()
            return key
    else:
        # If the file does not exist, generate a new key
        new_key = generate_random_key()
        with open(file_path, 'w') as key_file:
            key_file.write(new_key)
        return new_key

if __name__ == "__main__":
    key = check_or_create_key()
    print(f"Using key: {key}")
