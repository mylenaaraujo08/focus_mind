# frames/register_frame.py
import tkinter as tk
from tkinter import messagebox
from utils.user_manager import UserManager

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors.get("beige", "#F5F3F0"))
        self.controller = controller
        self.colors = colors
        self.user_manager = UserManager()
        
        self.colors.update({
            "beige": "#F5F3F0",
            "white": "#FFFFFF", 
            "dark_blue": "#2C3E50",
            "light_cream": "#FAF8F5",
            "dark_text": "#2C3E50",
            "purple": "#8E44AD",
            "green": "#27AE60",
            "orange": "#E67E22"
        })
        
        self.create_ui()

    def create_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_container = tk.Frame(self, bg=self.colors["beige"])
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        center_frame = tk.Frame(main_container, bg=self.colors["beige"])
        center_frame.grid(row=0, column=0)
        
        header_frame = tk.Frame(center_frame, bg=self.colors["white"], 
                               relief="solid", bd=2, width=400)
        header_frame.pack(pady=(0, 15), padx=30, fill="x")
        
        logo_frame = tk.Frame(header_frame, bg=self.colors["white"])
        logo_frame.pack(pady=15)
        
        tk.Label(logo_frame, text="🧠", font=("Arial", 36), 
                bg=self.colors["white"], fg="#FFD700").pack()
        tk.Label(logo_frame, text="FocusMind", 
                font=("Segoe UI", 22, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(5,0))
        tk.Label(logo_frame, text="Cadastro de Nova Conta", 
                font=("Segoe UI", 14), 
                bg=self.colors["white"], 
                fg=self.colors["purple"]).pack(pady=(5,0))
        
        form_frame = tk.Frame(center_frame, bg=self.colors["white"], 
                             relief="solid", bd=2, width=400)
        form_frame.pack(pady=(0, 15), padx=30, fill="x")
        
        tk.Label(form_frame, text="📝 Criar Nova Conta", 
                font=("Segoe UI", 18, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(15, 20))
        
        fields_frame = tk.Frame(form_frame, bg=self.colors["white"])
        fields_frame.pack(pady=(0, 15), padx=30)
        
        tk.Label(fields_frame, text="Nome Completo:", 
                font=("Segoe UI", 11, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 3))
        
        self.name_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), 
                                  bg=self.colors["light_cream"], 
                                  fg=self.colors["dark_text"],
                                  relief="solid", bd=2, width=28)
        self.name_entry.pack(pady=(0, 12), ipady=6)
        
        tk.Label(fields_frame, text="Nome de Usuário:", 
                font=("Segoe UI", 11, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 3))
        
        self.username_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), 
                                      bg=self.colors["light_cream"], 
                                      fg=self.colors["dark_text"],
                                      relief="solid", bd=2, width=28)
        self.username_entry.pack(pady=(0, 12), ipady=6)
        
        tk.Label(fields_frame, text="Senha:", 
                font=("Segoe UI", 11, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 3))
        
        self.password_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), 
                                      bg=self.colors["light_cream"], 
                                      fg=self.colors["dark_text"],
                                      relief="solid", bd=2, width=28, show="*")
        self.password_entry.pack(pady=(0, 12), ipady=6)
        
        tk.Label(fields_frame, text="Confirmar Senha:", 
                font=("Segoe UI", 11, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 3))
        
        self.confirm_password_entry = tk.Entry(fields_frame, font=("Segoe UI", 12), 
                                              bg=self.colors["light_cream"], 
                                              fg=self.colors["dark_text"],
                                              relief="solid", bd=2, width=28, show="*")
        self.confirm_password_entry.pack(pady=(0, 18), ipady=6)
        
        buttons_frame = tk.Frame(form_frame, bg=self.colors["white"])
        buttons_frame.pack(pady=(0, 20))
        
        create_button = tk.Button(buttons_frame, text="✅ Criar Conta", 
                                 command=self.create_account,
                                 bg=self.colors["green"], fg=self.colors["white"], 
                                 font=("Segoe UI", 12, "bold"), relief="flat", 
                                 padx=25, pady=10, cursor="hand2")
        create_button.pack(side="left", padx=(0, 12))
        
        back_button = tk.Button(buttons_frame, text="← Voltar", 
                               command=self.go_to_login,
                               bg=self.colors["purple"], fg=self.colors["white"], 
                               font=("Segoe UI", 12, "bold"), relief="flat", 
                               padx=25, pady=10, cursor="hand2")
        back_button.pack(side="left")
        
        info_frame = tk.Frame(center_frame, bg=self.colors["light_cream"], 
                             relief="solid", bd=2, width=400)
        info_frame.pack(padx=30, fill="x")
        
        tk.Label(info_frame, text="ℹ️ Informações", 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors["light_cream"], 
                fg=self.colors["dark_blue"]).pack(pady=(12, 8))
        
        info_text = """• Nome de usuário único (mín. 3 caracteres)
• Senha segura (mín. 4 caracteres)
• Confirme sua senha corretamente"""
        
        tk.Label(info_frame, text=info_text, 
                font=("Segoe UI", 10), 
                bg=self.colors["light_cream"], 
                fg=self.colors["dark_text"],
                justify="left").pack(pady=(0, 12), padx=15)
        
        self.bind_enter_keys()

    def bind_enter_keys(self):
        self.name_entry.bind("<Return>", lambda e: self.username_entry.focus())
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.confirm_password_entry.focus())
        self.confirm_password_entry.bind("<Return>", lambda e: self.create_account())

    def create_account(self):
        """Método principal para criar a conta"""
        try:
            print("🔄 Iniciando processo de criação de conta...")
            
            name = self.name_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            
            print(f"📝 Dados recebidos - Nome: '{name}', Usuário: '{username}'")
            
            if not self.validate_fields(name, username, password, confirm_password):
                return
            
            if self.user_manager.user_exists(username):
                messagebox.showerror("Erro", "Este nome de usuário já existe!\nEscolha outro nome de usuário.")
                self.username_entry.focus()
                self.username_entry.select_range(0, tk.END)
                return
            
            print("✅ Validações OK, criando usuário...")
            success = self.user_manager.register_user(name, username, password)
            
            if success:
                print(f"✅ Usuário '{username}' criado com sucesso!")
                messagebox.showinfo("Sucesso!", 
                                  f"Conta criada com sucesso!\n\n"
                                  f"Nome: {name}\n"
                                  f"Usuário: {username}\n\n"
                                  f"Você será redirecionado para a tela de login.")
                self.clear_fields()
                self.go_to_login()
            else:
                print("❌ Falha ao criar usuário")
                messagebox.showerror("Erro", "Erro ao criar conta!\nTente novamente.")
            
        except Exception as e:
            print(f"❌ Erro no cadastro: {e}")
            messagebox.showerror("Erro", f"Erro inesperado ao criar conta:\n{str(e)}")

    def validate_fields(self, name, username, password, confirm_password):
        """Valida todos os campos do formulário"""
        if not name:
            messagebox.showerror("Erro", "Por favor, digite seu nome completo!")
            self.name_entry.focus()
            return False
        
        if len(name) < 2:
            messagebox.showerror("Erro", "O nome deve ter pelo menos 2 caracteres!")
            self.name_entry.focus()
            return False
        
        if not username:
            messagebox.showerror("Erro", "Por favor, digite um nome de usuário!")
            self.username_entry.focus()
            return False
        
        if len(username) < 3:
            messagebox.showerror("Erro", "O nome de usuário deve ter pelo menos 3 caracteres!")
            self.username_entry.focus()
            return False
        
        if not password:
            messagebox.showerror("Erro", "Por favor, digite uma senha!")
            self.password_entry.focus()
            return False
        
        if len(password) < 4:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 4 caracteres!")
            self.password_entry.focus()
            return False
        
        if password != confirm_password:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            self.confirm_password_entry.delete(0, tk.END)
            self.confirm_password_entry.focus()
            return False
        
        return True

    def clear_fields(self):
        """Limpa todos os campos do formulário"""
        self.name_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

    def go_to_login(self):
        """Volta para a tela de login"""
        try:
            print("🔙 Voltando para tela de login...")
            from frames.login_frame import LoginFrame
            self.controller.show_frame(LoginFrame)
        except Exception as e:
            print(f"❌ Erro ao voltar para login: {e}")
            messagebox.showerror("Erro", "Erro ao voltar para a tela de login!")

    def reset_form(self):
        """Reseta o formulário"""
        self.clear_fields()
        self.name_entry.focus()