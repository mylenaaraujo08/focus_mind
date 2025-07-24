# frames/login_frame.py
import tkinter as tk
from tkinter import messagebox, font
import json
import os
import hashlib

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors.get("beige", "#F5F3F0"))
        self.controller = controller
        self.colors = colors
        self.users_file = "users.json"
        
        print("LoginFrame criado!")  # Debug
        
        # Atualiza cores para consistência
        self.colors.update({
            "soft_cream": "#F5F3F0",
            "light_cream": "#FAF8F5",
            "dark_text": "#2C3E50",
            "beige": "#F5F3F0",
            "white": "#FFFFFF",
            "dark_blue": "#2C3E50",
            "purple": "#8E44AD",
            "green": "#27AE60",
            "orange": "#E67E22",
            "blue": "#3498DB",
            "red": "#E74C3C"
        })
        
        self.create_ui()

    def create_ui(self):
        print("Criando UI do LoginFrame...")  # Debug
        
        # Header com logo
        header_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Logo e título centralizado
        logo_container = tk.Frame(header_frame, bg=self.colors["dark_blue"])
        logo_container.pack(expand=True, pady=30)
        
        tk.Label(logo_container, text="🧠", font=("Arial", 48), 
                bg=self.colors["dark_blue"], fg="#FFD700").pack()
        
        tk.Label(logo_container, text="FocusMind", 
                font=("Segoe UI", 32, "bold"), 
                bg=self.colors["dark_blue"], 
                fg=self.colors["white"]).pack(pady=(5, 0))

        # Container principal centralizado
        main_container = tk.Frame(self, bg=self.colors["beige"])
        main_container.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Card de login centralizado - AUMENTANDO A ALTURA
        login_card = tk.Frame(main_container, bg=self.colors["white"], 
                             bd=2, relief="solid", width=400, height=650)  # Aumentei a altura
        login_card.pack(expand=True)
        login_card.pack_propagate(False)
        
        # Sombra do card
        shadow_frame = tk.Frame(main_container, bg="#D5D8DC", width=405, height=655)
        shadow_frame.place(in_=login_card, x=5, y=5)
        shadow_frame.lower()

        # Header do card
        card_header = tk.Frame(login_card, bg=self.colors["blue"], height=80)
        card_header.pack(fill="x", padx=3, pady=3)
        card_header.pack_propagate(False)
        
        tk.Label(card_header, text="🔐 Fazer Login", 
                font=("Segoe UI", 20, "bold"), 
                bg=self.colors["blue"], 
                fg=self.colors["white"]).pack(expand=True, pady=25)

        # Corpo do formulário
        form_frame = tk.Frame(login_card, bg=self.colors["white"])
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Campo de usuário
        tk.Label(form_frame, text="👤 Usuário:", 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(form_frame, font=("Segoe UI", 14), 
                                      relief="solid", bd=2, 
                                      bg=self.colors["light_cream"])
        self.username_entry.pack(fill="x", pady=(0, 20), ipady=8)
        self.username_entry.focus()

        # Campo de senha
        tk.Label(form_frame, text="🔒 Senha:", 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = tk.Entry(form_frame, font=("Segoe UI", 14), 
                                      show="*", relief="solid", bd=2,
                                      bg=self.colors["light_cream"])
        self.password_entry.pack(fill="x", pady=(0, 30), ipady=8)

        # Botão de login
        login_button = tk.Button(form_frame, text="🚀 Entrar", 
                               command=self.login,
                               bg=self.colors["green"], fg=self.colors["white"], 
                               font=("Segoe UI", 14, "bold"), relief="flat", 
                               pady=12, cursor="hand2")
        login_button.pack(fill="x", pady=(0, 15))

        # Separador
        separator = tk.Frame(form_frame, bg="#ECF0F1", height=2)
        separator.pack(fill="x", pady=15)

        # Texto "Não possui conta?"
        no_account_label = tk.Label(form_frame, text="Não possui conta?", 
                                   font=("Segoe UI", 11), 
                                   bg=self.colors["white"], 
                                   fg=self.colors["dark_text"])
        no_account_label.pack(pady=(0, 10))
        print("Label 'Não possui conta?' criado!")  # Debug

        # BOTÃO CRIAR CONTA - Versão destacada
        register_button = tk.Button(form_frame, 
                                   text="📝 Criar Conta", 
                                   command=self.go_to_register,
                                   bg=self.colors["purple"], 
                                   fg=self.colors["white"], 
                                   font=("Segoe UI", 13, "bold"), 
                                   relief="flat", 
                                   pady=10, 
                                   cursor="hand2",
                                   activebackground="#9B59B6",
                                   activeforeground="white")
        register_button.pack(fill="x", pady=(0, 15))

        # Separador menor
        separator2 = tk.Frame(form_frame, bg="#ECF0F1", height=1)
        separator2.pack(fill="x", pady=10)

        # Texto para acesso demonstrativo
        demo_label = tk.Label(form_frame, text="Ou acesse rapidamente:", 
                             font=("Segoe UI", 10), 
                             bg=self.colors["white"], 
                             fg=self.colors["dark_text"])
        demo_label.pack(pady=(0, 5))

        # Botão de acesso rápido (para testes)
        demo_button = tk.Button(form_frame, text="🎯 Acesso Demonstrativo", 
                               command=self.demo_login,
                               bg=self.colors["orange"], fg=self.colors["white"], 
                               font=("Segoe UI", 11, "bold"), relief="flat", 
                               pady=8, cursor="hand2")
        demo_button.pack(fill="x", pady=(0, 10))

        # TESTE: Botão vermelho para debug
        test_button = tk.Button(form_frame, text="🔥 TESTE - CLIQUE AQUI", 
                               command=lambda: print("🎉 BOTÃO TESTE FUNCIONOU!"),
                               bg="red", fg="white", 
                               font=("Segoe UI", 10, "bold"), relief="flat", 
                               pady=6, cursor="hand2")
        test_button.pack(fill="x", pady=(5, 0))

        # Bind Enter para login
        self.bind_all("<Return>", lambda e: self.login())
        
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

    def login(self):
        """Realiza o login do usuário"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        print(f"🔐 Tentativa de login: '{username}'")  # Debug
        
        if not username or not password:
            messagebox.showwarning("Campos Obrigatórios", 
                                 "Por favor, preencha usuário e senha!")
            return
        
        users = self.load_users()
        print(f"📋 Usuários carregados: {list(users.keys())}")  # Debug
        
        hashed_password = self.hash_password(password)
        print(f"🔑 Hash da senha: {hashed_password[:10]}...")  # Debug (parte do hash)
        
        # Verifica se usuário existe (pode ser username ou email)
        user_found = False
        user_data = None
        
        # Primeiro, tenta encontrar por username/email diretamente
        if username in users:
            user_data = users[username]
            user_found = True
        else:
            # Se não encontrou, procura por username dentro dos dados do usuário
            for key, data in users.items():
                if isinstance(data, dict):
                    # Verifica se o username corresponde ao name ou ao próprio key
                    if (data.get('name', '').lower() == username.lower() or 
                        data.get('username', '').lower() == username.lower() or
                        key.lower() == username.lower()):
                        user_data = data
                        user_found = True
                        break
        
        if user_found and user_data:
            print(f"✅ Usuário encontrado: {user_data}")  # Debug
            
            # Verifica senha (compatível com diferentes estruturas)
            stored_password = (user_data.get('password') or 
                             user_data.get('password_hash') or 
                             '')
            
            print(f"🔍 Senha armazenada: {stored_password[:10]}...")  # Debug (parte do hash)
            
            if stored_password == hashed_password:
                # Login bem-sucedido
                user_name = user_data.get('name', username)
                print(f"🎉 Login bem-sucedido para: {user_name}")  # Debug
                
                messagebox.showinfo("Login", f"Bem-vindo(a), {user_name}!")
                
                self.controller.current_user = {
                    'username': username,
                    'name': user_name,
                    'email': user_data.get('email', username)
                }
                
                print("🚀 Navegando para SelectionFrame...")  # Debug
                from frames.selection_frame import SelectionFrame
                self.controller.show_frame(SelectionFrame)
                return
            else:
                print("❌ Senha incorreta")  # Debug
        else:
            print("❌ Usuário não encontrado")  # Debug
        
        # Se chegou até aqui, login falhou
        messagebox.showerror("Erro de Login", 
                           "Usuário ou senha incorretos!")
        self.password_entry.delete(0, tk.END)

    def demo_login(self):
        """Login demonstrativo sem necessidade de cadastro"""
        print("🎯 Fazendo login demonstrativo...")  # Debug
        
        self.controller.current_user = {
            'username': 'demo',
            'name': 'Usuário Demonstrativo',
            'email': 'demo@focusmind.com'
        }
        
        messagebox.showinfo("Demo", "Entrando como usuário demonstrativo!")
        
        print("🚀 Navegando para SelectionFrame (demo)...")  # Debug
        from frames.selection_frame import SelectionFrame
        self.controller.show_frame(SelectionFrame)

    def go_to_register(self):
        """Vai para tela de cadastro"""
        try:
            from frames.register_frame import RegisterFrame
            print("✅ RegisterFrame importado!")
            self.controller.show_frame(RegisterFrame)
            print("✅ Navegando para RegisterFrame!")
        except Exception as e:
            print(f"❌ Erro: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir cadastro: {e}")
