# frames/forgot_password_frame.py
import tkinter as tk
from tkinter import messagebox

class ForgotPasswordFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["beige"])
        self.controller = controller

        # CORREÇÃO: Importa o frame aqui e o atribui a 'self' para uso em outros métodos
        from frames.login_frame import LoginFrame
        self.LoginFrame = LoginFrame

        container = tk.Frame(self, bg=colors["dark_blue"])
        container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=350)

        tk.Label(container, text="Recuperar Senha", font=("Arial", 24, "bold"), bg=colors["dark_blue"], fg=colors["white"]).pack(pady=(30, 20))
        tk.Label(container, text="Digite seu e-mail para receber ajuda.", font=("Arial", 11), bg=colors["dark_blue"], fg=colors["light_gray"]).pack(pady=(0,20))

        tk.Label(container, text="Email", font=("Arial", 12), bg=colors["dark_blue"], fg=colors["white"]).pack(padx=50, anchor="w")
        self.email_entry = tk.Entry(container, font=("Arial", 14), width=30, bd=0)
        self.email_entry.pack(pady=(0, 20), ipady=5)

        recover_btn = tk.Button(container, text="Recuperar", command=self.recover, bg=colors["green"], fg=colors["white"], font=("Arial", 14, "bold"), relief="flat", width=25, pady=5)
        recover_btn.pack(pady=10)

        back_btn = tk.Button(container, text="Voltar para o Login", command=lambda: controller.show_frame(self.LoginFrame), bg=colors["dark_blue"], fg=colors["light_gray"], relief="flat", activebackground=colors["dark_blue"])
        back_btn.pack()

    def recover(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showerror("Erro", "Por favor, digite um e-mail.")
            return
        
        message = self.controller.user_manager.get_user_password_hint(email)
        messagebox.showinfo("Recuperação de Senha", message)
