import argparse
import json
from my_loginUser import authenticate

def main():
    parser = argparse.ArgumentParser(description="Login CLI tool")
    parser.add_argument("--email", type=str, required=True, help="User email")
    parser.add_argument("--password", type=str, required=True, help="User password")

    args = parser.parse_args()

    try:
        result = authenticate(args.email, args.password)
        print(json.dumps(result))  # JSON output for other languages
    except Exception as e:
        print(json.dumps({"success": False, "message": f"Error: {str(e)}"}))
