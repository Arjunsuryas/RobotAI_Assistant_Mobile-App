import sys
import getpass
import threading
import time
from typing import Dict

# Optional: Supabase client
try:
    from supabase import create_client, Client
    SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
    SUPABASE_KEY = "YOUR_SUPABASE_KEY"
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    USE_SUPABASE = True
except Exception:
    USE_SUPABASE = False
    print("Supabase not configured. Running in local mode.")

# Simple in-memory "database"
users: Dict[str, str] = {}  # email -> password


def alert(title: str, message: str):
    print(f"\n[{title}] {message}\n")


def sign_up(email: str, password: str):
    if USE_SUPABASE:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            return True
        else:
            raise Exception(res.error.message if res.error else "Sign up failed")
    else:
        if email in users:
            raise Exception("Email already registered")
        users[email] = password
        return True


def sign_in(email: str, password: str):
    if USE_SUPABASE:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            return True
        else:
            raise Exception(res.error.message if res.error else "Sign in failed")
    else:
        if email not in users or users[email] != password:
            raise Exception("Invalid email or password")
        return True


def auth_screen():
    is_sign_up = False
    while True:
        print("=== AI Assistant Authentication ===")
        print("Mode:", "Sign Up" if is_sign_up else "Sign In")

        email = input("Email: ").strip()
        password = getpass.getpass("Password: ").strip()

        if not email or not password:
            alert("Error", "Please fill in all fields")
            continue

        print("Processing...\n")
        time.sleep(0.5)

        try:
            if is_sign_up:
                sign_up(email, password)
                alert("Success", "Account created! Please sign in.")
                is_sign_up = False
            else:
                sign_in(email, password)
                alert("Success", f"Signed in as {email}")
                print("Redirecting to chat screen...\n")
                break
        except Exception as e:
            alert("Error", str(e))

        # Toggle mode
        toggle = input("Switch mode? (y/n): ").strip().lower()
        if toggle == "y":
            is_sign_up = not is_sign_up


if __name__ == "__main__":
    auth_screen()
