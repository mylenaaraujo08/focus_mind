# utils/user_manager.py
import json
import os
import hashlib

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
    
    def hash_password(self, password):
        """Cria hash da senha para segurança"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Carrega usuários do arquivo JSON"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
        return {}
    
    def save_users(self, users):
        """Salva usuários no arquivo JSON"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")
    
    def register_user(self, username, password, name, email):
        """Registra um novo usuário"""
        users = self.load_users()
        
        if username in users:
            return False, "Usuário já existe"
        
        # Verifica se email já existe
        for user_data in users.values():
            if user_data.get('email', '').lower() == email.lower():
                return False, "Email já cadastrado"
        
        users[username] = {
            'name': name,
            'email': email.lower(),
            'password': self.hash_password(password)
        }
        
        self.save_users(users)
        return True, "Usuário registrado com sucesso"
    
    def authenticate_user(self, username, password):
        """Autentica um usuário"""
        users = self.load_users()
        hashed_password = self.hash_password(password)
        
        if username in users and users[username]['password'] == hashed_password:
            return True, users[username]
        
        return False, None
