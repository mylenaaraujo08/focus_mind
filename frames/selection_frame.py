# frames/selection_frame.py
import tkinter as tk

class SelectionFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors.get("beige", "#F5F3F0"))
        self.controller = controller
        self.colors = colors
        self.create_ui()

    def create_ui(self):
        """Cria a interface de seleção"""
        # Header com logo
        header_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=100)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Container do logo centralizado
        logo_container = tk.Frame(header_frame, bg=self.colors["dark_blue"])
        logo_container.pack(expand=True, pady=20)
        
        # Logo e título
        tk.Label(logo_container, text="🧠", font=("Arial", 48), 
                bg=self.colors["dark_blue"], fg="#FFD700").pack()
        tk.Label(logo_container, text="FocusMind", font=("Segoe UI", 36, "bold"), 
                bg=self.colors["dark_blue"], fg=self.colors["white"]).pack()

        # Título da seção
        title_frame = tk.Frame(self, bg=self.colors["light_cream"], height=80)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🎯 Escolha uma Atividade", 
                font=("Segoe UI", 28, "bold"), bg=self.colors["light_cream"], 
                fg=self.colors["dark_blue"]).pack(pady=25)

        # Container principal dos botões
        main_frame = tk.Frame(self, bg=self.colors["beige"])
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # APENAS 2 CARDS AGORA - Leitura e Biblioteca
        cards_frame = tk.Frame(main_frame, bg=self.colors["beige"])
        cards_frame.pack(expand=True)

        # Card Leitura Guiada
        leitura_card = tk.Frame(cards_frame, bg=self.colors["white"], 
                               relief="raised", bd=3, padx=30, pady=30)
        leitura_card.pack(side="left", padx=30, pady=20, fill="both", expand=True)

        tk.Label(leitura_card, text="📖", font=("Arial", 64), 
                bg=self.colors["white"]).pack(pady=(0, 20))
        
        tk.Label(leitura_card, text="Leitura Guiada", 
                font=("Segoe UI", 24, "bold"), bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(0, 15))
        
        tk.Label(leitura_card, text="Carregue textos e ouça\na narração com recursos\nde acessibilidade", 
                font=("Segoe UI", 14), bg=self.colors["white"], 
                fg=self.colors["dark_text"], justify="center").pack(pady=(0, 25))
        
        tk.Button(leitura_card, text="Começar Leitura", 
                 command=self.open_leitura,
                 bg=self.colors["purple"], fg=self.colors["white"], 
                 font=("Segoe UI", 16, "bold"), relief="flat", 
                 padx=30, pady=15, cursor="hand2").pack()

        # Card Biblioteca
        biblioteca_card = tk.Frame(cards_frame, bg=self.colors["white"], 
                                  relief="raised", bd=3, padx=30, pady=30)
        biblioteca_card.pack(side="left", padx=30, pady=20, fill="both", expand=True)

        tk.Label(biblioteca_card, text="📚", font=("Arial", 64), 
                bg=self.colors["white"]).pack(pady=(0, 20))
        
        tk.Label(biblioteca_card, text="Biblioteca", 
                font=("Segoe UI", 24, "bold"), bg=self.colors["white"], 
                fg=self.colors["dark_blue"]).pack(pady=(0, 15))
        
        tk.Label(biblioteca_card, text="Histórias clássicas com\nnarrações e recursos\npara dislexia", 
                font=("Segoe UI", 14), bg=self.colors["white"], 
                fg=self.colors["dark_text"], justify="center").pack(pady=(0, 25))
        
        tk.Button(biblioteca_card, text="Abrir Biblioteca", 
                 command=self.open_biblioteca,
                 bg=self.colors["green"], fg=self.colors["white"], 
                 font=("Segoe UI", 16, "bold"), relief="flat", 
                 padx=30, pady=15, cursor="hand2").pack()

        # Rodapé com informações
        footer_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=60)
        footer_frame.pack(fill="x", side="bottom")
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, text="💡 Aplicativo desenvolvido para auxiliar pessoas com dislexia na leitura", 
                font=("Segoe UI", 12), bg=self.colors["dark_blue"], 
                fg=self.colors["white"]).pack(pady=20)

    def open_leitura(self):
        """Abre a tela de leitura guiada"""
        from frames.leitura_frame import LeituraFrame
        self.controller.show_frame(LeituraFrame)

    def open_biblioteca(self):
        """Abre a biblioteca de histórias"""
        from frames.biblioteca_frame import BibliotecaFrame
        self.controller.show_frame(BibliotecaFrame)
