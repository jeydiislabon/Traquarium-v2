"""User authentication and management"""

import os
import json


class UserManager:
    def __init__(self, user_file="users.json"):
        self.user_file = user_file
        if not os.path.exists(self.user_file):
            with open(self.user_file, "w") as f:
                json.dump({}, f)

    def load_users(self):
        with open(self.user_file, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.user_file, "w") as f:
            json.dump(users, f, indent=4)

    def register_user(self, username, password):
        users = self.load_users()
        if username in users:
            return False, "Username already exists."
        users[username] = {"password": password}
        self.save_users(users)
        os.makedirs(os.path.join("users", username), exist_ok=True)
        return True, "✅ Registration successful!"

    def validate_user(self, username, password):
        users = self.load_users()
        if username not in users:
            return False, "❌ User not found."
        if users[username]["password"] != password:
            return False, "❌ Incorrect password."
        return True, "✅ Login successful!"
