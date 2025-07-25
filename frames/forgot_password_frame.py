# frames/forgot_password_frame.py
import tkinter as tk
from tkinter import messagebox
from utils.user_manager import UserManager

class ForgotPasswordFrame(tk.Frame):
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
            "orange": "#E67E22",
            "light_gray": "#E8E8E8",
            "gray": "#CCCCCC"
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
                               relief="solid", bd=2)
        header_frame.pack(pady=(0, 20), padx=40, fill="x")
        
        logo_frame = tk.Frame(header_frame, bg=self.colors["white"])
        logo_frame.pack(pady=20)
        
        tk.Label(logo_frame, text="🧠", font=("Arial", 48), 
                bg=self.colors["white"], fg="#FFD700").pack()
        tk.Label(logo_frame, text="FocusMind", 
                font=("Segoe UI", 28, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(5,0))
        tk.Label(logo_frame, text="Recuperação de Senha", 
                font=("Segoe UI", 16), 
                bg=self.colors["white"], 
                fg=self.colors["purple"]).pack(pady=(5,0))
        
        form_frame = tk.Frame(center_frame, bg=self.colors["white"], 
                             relief="solid", bd=2)
        form_frame.pack(pady=(0, 20), padx=40, fill="x")
        
        tk.Label(form_frame, text="🔑 Esqueceu sua Senha?", 
                font=("Segoe UI", 20, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(20, 10))
        
        info_text = """Infelizmente, não temos sistema de email configurado ainda.
        
Por favor, entre em contato com o administrador do sistema
ou tente lembrar de suas credenciais de login."""
        
        tk.Label(form_frame, text=info_text, 
                font=("Segoe UI", 12), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"],
                justify="center").pack(pady=(10, 20))
        
        fields_frame = tk.Frame(form_frame, bg=self.colors["white"])
        fields_frame.pack(pady=(0, 20), padx=40)
        
        tk.Label(fields_frame, text="Nome de Usuário:", 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = tk.Entry(fields_frame, font=("Segoe UI", 14), 
                                      bg=self.colors["light_cream"], 
                                      fg=self.colors["dark_text"],
                                      relief="solid", bd=2, width=30)
        self.username_entry.pack(pady=(0, 20), ipady=8)
        
        buttons_frame = tk.Frame(form_frame, bg=self.colors["white"])
        buttons_frame.pack(pady=(0, 30))
        
        tk.Button(buttons_frame, text="📧 Solicitar Ajuda", 
                 command=self.request_help,
                 bg=self.colors["orange"], fg=self.colors["white"], 
                 font=("Segoe UI", 14, "bold"), relief="flat", 
                 padx=30, pady=12, cursor="hand2").pack(side="left", padx=(0, 15))
        
        tk.Button(buttons_frame, text="← Voltar ao Login", 
                 command=self.go_to_login,
                 bg=self.colors["purple"], fg=self.colors["white"], 
                 font=("Segoe UI", 14, "bold"), relief="flat", 
                 padx=30, pady=12, cursor="hand2").pack(side="left")
        
        tips_frame = tk.Frame(center_frame, bg=self.colors["light_cream"], 
                             relief="solid", bd=2)
        tips_frame.pack(padx=40, fill="x")
        
        tk.Label(tips_frame, text="💡 Dicas para Lembrar", 
                font=("Segoe UI", 14, "bold"), 
                bg=self.colors["light_cream"], 
                fg=self.colors["dark_blue"]).pack(pady=(15, 10))
        
        tips_text = """• Tente variações do seu nome ou apelido
• Verifique se não há espaços extras
• Lembre-se de maiúsculas e minúsculas
• Tente senhas que você costuma usar
• Verifique se o Caps Lock não está ativado"""
        
        tk.Label(tips_frame, text=tips_text, 
                font=("Segoe UI", 11), 
                bg=self.colors["light_cream"], 
                fg=self.colors["dark_text"],
                justify="left").pack(pady=(0, 15), padx=20)
        
        self.username_entry.bind("<Return>", lambda e: self.request_help())
        self.username_entry.focus()

    def request_help(self):
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome de usuário!")
            self.username_entry.focus()
            return
        
        if self.user_manager.user_exists(username):
            user_info = self.user_manager.get_user_info(username)
            if user_info:
                messagebox.showinfo("Usuário Encontrado", 
                                  f"Usuário '{username}' existe no sistema!\n\n"
                                  f"Nome: {user_info.get('name', 'N/A')}\n"
                                  f"Criado em: {user_info.get('created_date', 'N/A')}\n\n"
                                  f"Tente lembrar de sua senha ou entre em contato com o administrador.")
            else:
                messagebox.showinfo("Sistema", 
                                  f"Usuário '{username}' encontrado, mas não foi possível obter detalhes.\n\n"
                                  f"Entre em contato com o administrador do sistema.")
        else:
            messagebox.showerror("Usuário Não Encontrado", 
                               f"O usuário '{username}' não existe no sistema.\n\n"
                               f"Verifique se digitou corretamente ou cadastre uma nova conta.")
        
        self.username_entry.select_range(0, tk.END)

    def go_to_login(self):
        try:
            from frames.login_frame import LoginFrame
            self.controller.show_frame(LoginFrame)
            print("🔙 Voltando para tela de login")
        except Exception as e:
            print(f"❌ Erro ao voltar para login: {e}")
            messagebox.showerror("Erro", "Erro ao voltar para a tela de login!")

    def reset_form(self):
        self.username_entry.delete(0, tk.END)
        self.username_entry.focus()
