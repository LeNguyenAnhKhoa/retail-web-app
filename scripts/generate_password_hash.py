import bcrypt

def generate_hash(password: str) -> str:
    """Generate bcrypt hash for a password"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

if __name__ == "__main__":
    passwords = {
        "Admin123": "admin@example.com",
        "Staff123": "staff1@example.com", 
        "Stock123": "stock1@example.com"
    }
    
    print("-- UPDATE password hashes for user accounts")
    print("-- Run these SQL commands in MySQL Workbench:\n")
    
    for password, email in passwords.items():
        hash_value = generate_hash(password)
        print(f"UPDATE users SET password_hash = '{hash_value}' WHERE email = '{email}';")
        print(f"-- Password: {password}\n")
