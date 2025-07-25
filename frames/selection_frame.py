# frames/selection_frame.py
import tkinter as tk
from tkinter import messagebox

class SelectionFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors.get("beige", "#F5F3F0"))
        self.controller = controller
        self.colors = colors
        
        self.colors.update({
            "beige": "#F5F3F0",
            "white": "#FFFFFF",
            "dark_blue": "#2C3E50",
            "light_cream": "#FAF8F5",
            "dark_text": "#2C3E50",
            "purple": "#8E44AD",
            "green": "#27AE60",
            "orange": "#E67E22",
            "red": "#E74C3C"
        })
        
        self.create_ui()

    def create_ui(self):
        header_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=100)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=self.colors["dark_blue"])
        header_content.pack(expand=True, fill="both")
        
        logo_frame = tk.Frame(header_content, bg=self.colors["dark_blue"])
        logo_frame.pack(side="left", padx=30, pady=20)
        
        tk.Label(logo_frame, text="🧠", font=("Arial", 42), 
                bg=self.colors["dark_blue"], fg="#FFD700").pack(side="left")
        tk.Label(logo_frame, text="FocusMind", font=("Segoe UI", 28, "bold"), 
                bg=self.colors["dark_blue"], fg=self.colors["white"]).pack(side="left", padx=(15,0))
        
        user_frame = tk.Frame(header_content, bg=self.colors["dark_blue"])
        user_frame.pack(side="right", padx=30, pady=20)
        
        current_user = self.controller.get_current_user()
        user_text = f"👤 {current_user}" if current_user else "👤 Usuário"
        
        tk.Label(user_frame, text=user_text, 
                font=("Segoe UI", 16, "bold"), 
                bg=self.colors["dark_blue"], 
                fg=self.colors["white"]).pack(side="left", padx=(0, 15))
        
        logout_button = tk.Button(user_frame, text="🚪 Sair", 
                                 command=self.logout,
                                 bg=self.colors["red"], fg=self.colors["white"], 
                                 font=("Segoe UI", 12, "bold"), relief="flat", 
                                 padx=20, pady=8, cursor="hand2")
        logout_button.pack(side="left")

        welcome_frame = tk.Frame(self, bg=self.colors["light_cream"], height=80)
        welcome_frame.pack(fill="x", padx=0, pady=0)
        welcome_frame.pack_propagate(False)
        
        welcome_text = f"Bem-vindo, {current_user}!" if current_user else "Bem-vindo ao FocusMind!"
        tk.Label(welcome_frame, text=welcome_text, 
                font=("Segoe UI", 24, "bold"), bg=self.colors["light_cream"], 
                fg=self.colors["dark_blue"]).pack(pady=25)

        main_container = tk.Frame(self, bg=self.colors["beige"])
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        left_option = tk.Frame(main_container, bg=self.colors["white"], 
                              relief="solid", bd=3, cursor="hand2")
        left_option.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        left_option.bind("<Button-1>", lambda e: self.open_leitura())
        
        for widget in left_option.winfo_children():
            widget.bind("<Button-1>", lambda e: self.open_leitura())

        icon_frame_left = tk.Frame(left_option, bg=self.colors["purple"], height=120)
        icon_frame_left.pack(fill="x")
        icon_frame_left.pack_propagate(False)
        
        tk.Label(icon_frame_left, text="📖", font=("Arial", 64), 
                bg=self.colors["purple"], fg=self.colors["white"]).pack(pady=25)

        content_frame_left = tk.Frame(left_option, bg=self.colors["white"])
        content_frame_left.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content_frame_left, text="Leitura Guiada", 
                font=("Segoe UI", 22, "bold"), bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(0, 15))
        
        desc_text_left = """Carregue seus próprios textos, 
arquivos PDF ou DOCX para uma 
experiência de leitura personalizada 
com narração e recursos de 
acessibilidade."""
        
        tk.Label(content_frame_left, text=desc_text_left, 
                font=("Segoe UI", 12), bg=self.colors["white"], 
                fg=self.colors["dark_text"], justify="center").pack(pady=(0, 20))
        
        tk.Button(content_frame_left, text="▶️ Começar Leitura", 
                 command=self.open_leitura,
                 bg=self.colors["purple"], fg=self.colors["white"], 
                 font=("Segoe UI", 14, "bold"), relief="flat", 
                 padx=25, pady=12, cursor="hand2").pack()

        right_option = tk.Frame(main_container, bg=self.colors["white"], 
                               relief="solid", bd=3, cursor="hand2")
        right_option.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        right_option.bind("<Button-1>", lambda e: self.open_biblioteca())
        
        for widget in right_option.winfo_children():
            widget.bind("<Button-1>", lambda e: self.open_biblioteca())

        icon_frame_right = tk.Frame(right_option, bg=self.colors["green"], height=120)
        icon_frame_right.pack(fill="x")
        icon_frame_right.pack_propagate(False)
        
        tk.Label(icon_frame_right, text="📚", font=("Arial", 64), 
                bg=self.colors["green"], fg=self.colors["white"]).pack(pady=25)

        content_frame_right = tk.Frame(right_option, bg=self.colors["white"])
        content_frame_right.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content_frame_right, text="Biblioteca de Histórias", 
                font=("Segoe UI", 22, "bold"), bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(0, 15))
        
        desc_text_right = """Acesse nossa coleção de histórias 
clássicas com recursos especiais 
para dislexia, incluindo coloração 
de sílabas e narração otimizada."""
        
        tk.Label(content_frame_right, text=desc_text_right, 
                font=("Segoe UI", 12), bg=self.colors["white"], 
                fg=self.colors["dark_text"], justify="center").pack(pady=(0, 20))
        
        tk.Button(content_frame_right, text="📖 Explorar Biblioteca", 
                 command=self.open_biblioteca,
                 bg=self.colors["green"], fg=self.colors["white"], 
                 font=("Segoe UI", 14, "bold"), relief="flat", 
                 padx=25, pady=12, cursor="hand2").pack()

        footer_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=60)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, text="💡 Dica: Use as opções de acessibilidade em cada módulo para uma melhor experiência!", 
                font=("Segoe UI", 11), bg=self.colors["dark_blue"], 
                fg=self.colors["white"]).pack(pady=20)

    def open_leitura(self):
        try:
            from frames.leitura_frame import LeituraFrame
            self.controller.show_frame(LeituraFrame)
            print("📖 Abrindo Leitura Guiada")
        except Exception as e:
            print(f"❌ Erro ao abrir Leitura: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir Leitura Guiada:\n{e}")

    def open_biblioteca(self):
        try:
            from frames.biblioteca_frame import BibliotecaFrame
            self.controller.show_frame(BibliotecaFrame)
            print("📚 Abrindo Biblioteca")
        except Exception as e:
            print(f"❌ Erro ao abrir Biblioteca: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir Biblioteca:\n{e}")

    def logout(self):
        """Faz logout e volta para a tela de login"""
        try:
            result = messagebox.askyesno("Confirmar Saída", 
                                       "Deseja realmente sair?\n\nVocê será redirecionado para a tela de login.")
            
            if result:
                print("🚪 Fazendo logout...")
                self.controller.logout()
                print("✅ Logout realizado com sucesso")
            else:
                print("❌ Logout cancelado pelo usuário")
                
        except Exception as e:
            print(f"❌ Erro no logout: {e}")
            messagebox.showerror("Erro", f"Erro ao fazer logout:\n{e}")
