def authenticate(email: str, password: str) -> dict:
    # Example: Replace this with your database or secure storage
    users = {
        "admin@example.com": "secure123",
        "user@example.com": "password456"
    }

    if not email or not password:
        return {"success": False, "message": "Email and password are required."}

    if email not in users:
        return {"success": False, "message": "User not found."}

    if users[email] != password:
        return {"success": False, "message": "Invalid password."}

    return {"success": True, "message": "Login successful."}
