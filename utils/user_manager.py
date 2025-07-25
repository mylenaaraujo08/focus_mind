# utils/user_manager.py
import json
import os
import hashlib

class UserManager:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"❌ Erro ao carregar usuários: {e}")
            return {}

    def save_users(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar usuários: {e}")
            return False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def user_exists(self, username):
        return username in self.users

    def register_user(self, name, username, password):
        try:
            if self.user_exists(username):
                return False
            
            hashed_password = self.hash_password(password)
            
            self.users[username] = {
                'name': name,
                'password': hashed_password,
                'created_date': self.get_current_date()
            }
            
            return self.save_users()
        except Exception as e:
            print(f"❌ Erro ao registrar usuário: {e}")
            return False

    def authenticate_user(self, username, password):
        try:
            if not self.user_exists(username):
                return False
            
            hashed_password = self.hash_password(password)
            return self.users[username]['password'] == hashed_password
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return False

    def get_user_info(self, username):
        if self.user_exists(username):
            return self.users[username]
        return None

    def get_current_date(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
