# frames/register_frame.py
import tkinter as tk
from tkinter import messagebox
import json
import os
import hashlib
import re
import win32com.client  # Importa aqui para evitar problemas depois
import threading

# Verifica se o SAPI está disponível
try:
    win32com.client.Dispatch("SAPI.SpVoice")
    SAPI_AVAILABLE = True
except:
    SAPI_AVAILABLE = False

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors.get("beige", "#F5F3F0"))
        self.controller = controller
        self.colors = colors
        self.users_file = "users.json"
        
        print("✅ RegisterFrame criado com sucesso!")
        
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
        
        # Atributos para TTS
        self.tts_engine = None
        self.is_reading = False
        self.reading_thread = None

    def create_ui(self):
        # Header com logo - MAIS COMPACTO
        header_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=80)  # Reduzido ainda mais
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Logo e título centralizado
        logo_container = tk.Frame(header_frame, bg=self.colors["dark_blue"])
        logo_container.pack(expand=True, pady=15)  # Reduzido
        
        tk.Label(logo_container, text="🧠", font=("Arial", 28), 
                bg=self.colors["dark_blue"], fg="#FFD700").pack()
        
        tk.Label(logo_container, text="FocusMind - Cadastro", 
                font=("Segoe UI", 18, "bold"), 
                bg=self.colors["dark_blue"], 
                fg=self.colors["white"]).pack(pady=(3, 0))

        # Container principal
        main_container = tk.Frame(self, bg=self.colors["beige"])
        main_container.pack(fill="both", expand=True, padx=30, pady=15)  # Reduzido padding
        
        # Card de cadastro centralizado - ALTURA OTIMIZADA
        register_card = tk.Frame(main_container, bg=self.colors["white"], 
                         bd=2, relief="solid", width=450, height=650)  # Largura e altura reduzidas
        register_card.pack(expand=True)
        register_card.pack_propagate(False)

        # Header do card - MAIS COMPACTO
        card_header = tk.Frame(register_card, bg=self.colors["purple"], height=50)  # Reduzido
        card_header.pack(fill="x", padx=3, pady=3)
        card_header.pack_propagate(False)
        
        tk.Label(card_header, text="📝 Criar Conta", 
                font=("Segoe UI", 16, "bold"), 
                bg=self.colors["purple"], 
                fg=self.colors["white"]).pack(expand=True, pady=12)

        # Corpo do formulário SEM SCROLL - mais compacto
        form_frame = tk.Frame(register_card, bg=self.colors["white"])
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)  # Padding reduzido

        # Campo Nome Completo
        tk.Label(form_frame, text="👤 Nome Completo:", 
                font=("Segoe UI", 10, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 2))
        
        self.name_entry = tk.Entry(form_frame, font=("Segoe UI", 10), 
                                  relief="solid", bd=1, 
                                  bg=self.colors["light_cream"])
        self.name_entry.pack(fill="x", pady=(0, 8), ipady=3)  # Padding reduzido
        self.name_entry.focus()

        # Campo Email
        tk.Label(form_frame, text="📧 E-mail:", 
                font=("Segoe UI", 10, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 2))
        
        self.email_entry = tk.Entry(form_frame, font=("Segoe UI", 10), 
                                   relief="solid", bd=1,
                                   bg=self.colors["light_cream"])
        self.email_entry.pack(fill="x", pady=(0, 8), ipady=3)

        # Campo Usuário
        tk.Label(form_frame, text="🆔 Nome de Usuário:", 
                font=("Segoe UI", 10, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 2))
        
        self.username_entry = tk.Entry(form_frame, font=("Segoe UI", 10), 
                                      relief="solid", bd=1,
                                      bg=self.colors["light_cream"])
        self.username_entry.pack(fill="x", pady=(0, 8), ipady=3)

        # Campo Senha
        tk.Label(form_frame, text="🔒 Senha:", 
                font=("Segoe UI", 10, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 2))
        
        self.password_entry = tk.Entry(form_frame, font=("Segoe UI", 10), 
                                      show="*", relief="solid", bd=1,
                                      bg=self.colors["light_cream"])
        self.password_entry.pack(fill="x", pady=(0, 8), ipady=3)

        # Campo Confirmar Senha
        tk.Label(form_frame, text="🔒 Confirmar Senha:", 
                font=("Segoe UI", 10, "bold"), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(anchor="w", pady=(0, 2))
        
        self.confirm_password_entry = tk.Entry(form_frame, font=("Segoe UI", 10), 
                                              show="*", relief="solid", bd=1,
                                              bg=self.colors["light_cream"])
        self.confirm_password_entry.pack(fill="x", pady=(0, 8), ipady=3)

        # Checkbox de termos - MAIS COMPACTO
        self.terms_var = tk.BooleanVar()
        terms_frame = tk.Frame(form_frame, bg=self.colors["white"])
        terms_frame.pack(fill="x", pady=(0, 8))
        
        tk.Checkbutton(terms_frame, text="Aceito os termos de uso", 
                      variable=self.terms_var,
                      bg=self.colors["white"], 
                      fg=self.colors["dark_text"],
                      font=("Segoe UI", 8),  # Fonte menor
                      activebackground=self.colors["white"]).pack(anchor="w")

        # BOTÃO DE CADASTRO - CENTRALIZADO
        register_button = tk.Button(form_frame, text="✅ Criar Conta", 
                                   command=self.register,
                                   bg=self.colors["green"], fg=self.colors["white"], 
                                   font=("Segoe UI", 12, "bold"), relief="flat", 
                                   pady=8, cursor="hand2")
        register_button.pack(fill="x", pady=(0, 15))

        # Separador
        separator = tk.Frame(form_frame, bg="#ECF0F1", height=2)
        separator.pack(fill="x", pady=10)

        # Texto "Já possui conta?"
        tk.Label(form_frame, text="Já possui conta?", 
                font=("Segoe UI", 10), 
                bg=self.colors["white"], 
                fg=self.colors["dark_text"]).pack(pady=(0, 8))

        # BOTÃO DE LOGIN - ABAIXO DA LABEL
        login_button = tk.Button(form_frame, text="🔐 Fazer Login", 
                                command=self.go_to_login,
                                bg=self.colors["blue"], fg=self.colors["white"], 
                                font=("Segoe UI", 11, "bold"), relief="flat", 
                                pady=6, cursor="hand2")
        login_button.pack(fill="x", pady=(0, 10))

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

    def validate_email(self, email):
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register(self):
        """Realiza o cadastro do usuário com o formato de dados correto."""
        print("🎯 Função register() chamada!")

        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip().lower() # E-mail em minúsculas
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validações (seu código aqui já estava ótimo)
        if not all([name, email, username, password, confirm_password]):
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos!")
            return
        if not self.terms_var.get():
            messagebox.showwarning("Termos de Uso", "Você deve aceitar os termos de uso!")
            return
        if not self.validate_email(email):
            messagebox.showwarning("Email Inválido", "Por favor, digite um email válido!")
            return
        if len(password) < 6:
            messagebox.showwarning("Senha Inválida", "A senha deve ter pelo menos 6 caracteres!")
            return
        if password != confirm_password:
            messagebox.showwarning("Senhas Diferentes", "A confirmação da senha não confere!")
            return

        users = self.load_users()

        # Verifica se email ou username já existem
        for user_data in users.values():
            if user_data.get('email', '').lower() == email:
                messagebox.showerror("Email Existente", "Este email já está cadastrado!")
                return
            if user_data.get('username', '').lower() == username.lower():
                messagebox.showerror("Usuário Existente", "Este nome de usuário já está em uso!")
                return
        
        # Cria novo usuário com formato correto
        # A chave principal será o E-MAIL
        # A senha será salva como "password_hash"
        # O "username" será salvo dentro do objeto do usuário
        users[email] = {
            'name': name,
            'username': username,
            'email': email,
            'password_hash': self.hash_password(password),
            'library': {}  # Adiciona uma biblioteca vazia para o novo usuário
        }
        
        self.save_users(users)
        self.go_to_login(name)

    def go_to_login(self, name=None):
        """Navega de volta para a tela de login."""
        from frames.login_frame import LoginFrame
        self.controller.show_frame(LoginFrame)
        if name:
            messagebox.showinfo("Cadastro Realizado", f"Conta criada com sucesso para {name}!\nAgora você pode fazer o login.")

    def init_tts(self):
        """Inicializa Windows SAPI TTS de forma robusta"""
        try:
            if SAPI_AVAILABLE:
                # Fecha engine anterior se existir
                if hasattr(self, 'tts_engine') and self.tts_engine:
                    try:
                        del self.tts_engine
                    except:
                        pass
                    self.tts_engine = None
                
                # Cria nova instância
                self.tts_engine = win32com.client.Dispatch("SAPI.SpVoice")
                
                # Configura propriedades básicas
                self.tts_engine.Rate = -1  # Velocidade fixa otimizada
                self.tts_engine.Volume = 100
                
                print("✅ Windows SAPI TTS (Leitura) inicializado")
            else:
                self.tts_engine = None
                print("❌ Windows SAPI não disponível")
        except Exception as e:
            self.tts_engine = None
            print(f"❌ Erro ao inicializar SAPI: {e}")

    def speak_text(self, text):
        """Fala o texto usando TTS de forma robusta - IGUAL BIBLIOTECA"""
        try:
            # Reinicializa TTS sempre antes de usar
            self.init_tts()
            
            if not self.tts_engine:
                messagebox.showerror("Erro de Áudio", 
                                   "Sistema de voz não disponível.\nInstale: pip install pywin32")
                return
            
            # Para qualquer leitura anterior
            if self.is_reading:
                self.stop_reading()
                # Aguarda um pouco mais
                threading.Event().wait(0.5)
            
            self.is_reading = True
            self.update_read_button()
            
            print(f"🔊 Iniciando leitura leitura_frame: {text[:50]}...")
            
            # Limita o tamanho do texto para evitar travamentos
            max_chars = 2000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
                print(f"⚠️ Texto limitado a {max_chars} caracteres")
            
            # Configura velocidade fixa
            self.tts_engine.Rate = -1
            
            # Usa SAPI para falar - modo síncrono com fallback
            try:
                self.tts_engine.Speak(text, 0)  # 0 = síncrono
                print("✅ Leitura leitura_frame concluída")
            except Exception as speak_error:
                print(f"❌ Erro específico na fala: {speak_error}")
                # Tenta usar modo assíncrono como fallback
                try:
                    self.tts_engine.Speak(text, 1)  # 1 = assíncrono
                    print("✅ Leitura em modo assíncrono")
                except Exception as async_error:
                    print(f"❌ Erro também no modo assíncrono: {async_error}")
                    raise speak_error
            
        except Exception as e:
            print(f"❌ Erro speak_text leitura: {e}")
            error_msg = "Erro na reprodução de áudio."
            if "2147352567" in str(e):
                error_msg += "\nO sistema de voz pode estar ocupado.\nTente novamente em alguns segundos."
            else:
                error_msg += f"\nDetalhes: {str(e)}"
            messagebox.showerror("Erro", error_msg)
        finally:
            self.is_reading = False
            self.after_idle(self.update_read_button)

    def stop_reading(self):
        """Para a leitura de forma robusta - IGUAL BIBLIOTECA"""
        print("⏹ Parando leitura leitura_frame...")
        self.is_reading = False
        
        if self.tts_engine:
            try:
                # Para a fala atual de múltiplas formas
                self.tts_engine.Skip("Sentence", 999)
                # Força parada
                try:
                    self.tts_engine.Speak("", 2)  # 2 = purge (limpa fila)
                except:
                    pass
            except Exception as e:
                print(f"⚠️ Erro ao parar SAPI: {e}")
                # Se der erro, reinicializa o engine
                try:
                    del self.tts_engine
                    self.tts_engine = None
                except:
                    pass
        
        self.after(100, self.update_read_button)

    def start_reading(self):
        """Inicia leitura do texto com verificações extras - IGUAL BIBLIOTECA"""
        if self.is_reading:
            self.stop_reading()
            return
            
        # Pega o texto da área de texto
        text_content = self.text_area.get("1.0", tk.END).strip()
        if not text_content or text_content in ["", "Digite ou cole seu texto aqui..."]:
            messagebox.showwarning("Aviso", "Nenhum texto para ler!\nDigite ou carregue um arquivo primeiro.")
            return
        
        # Verifica se o texto não é muito longo
        if len(text_content) > 5000:
            result = messagebox.askyesno("Texto Longo", 
                                       f"O texto tem {len(text_content)} caracteres.\nIsto pode causar problemas no áudio.\n\nDeseja continuar?")
            if not result:
                return
        
        print("🔊 Iniciando leitura do texto...")
        
        # Para qualquer leitura anterior primeiro
        self.stop_reading()
        
        # Aguarda um pouco antes de iniciar nova leitura
        self.after(200, lambda: self._delayed_start_reading(text_content))

    def _delayed_start_reading(self, text):
        """Inicia leitura com delay para garantir limpeza - IGUAL BIBLIOTECA"""
        try:
            # Cria thread para leitura
            self.reading_thread = threading.Thread(
                target=self.speak_text, 
                args=(text,), 
                daemon=True
            )
            self.reading_thread.start()
        except Exception as e:
            print(f"❌ Erro ao criar thread de leitura: {e}")
            self.is_reading = False
            self.update_read_button()

    def toggle_reading(self):
        """Alterna entre ler e parar - IGUAL BIBLIOTECA"""
        if self.is_reading:
            self.stop_reading()
        else:
            self.start_reading()

    def update_read_button(self):
        """Atualiza o texto e cor do botão de leitura - IGUAL BIBLIOTECA"""
        try:
            if hasattr(self, 'read_button'):
                if self.is_reading:
                    self.read_button.config(text="⏸️ Parar Leitura", bg="#E74C3C")
                else:
                    self.read_button.config(text="🔊 Ler Texto", bg=self.colors["green"])
        except Exception as e:
            print(f"⚠️ Erro ao atualizar botão: {e}")

    def create_controls_panel(self, parent):
        """Cria o painel de controles na parte inferior - ATUALIZADO"""
        controls_bg = tk.Frame(parent, bg=self.colors["dark_blue"], height=80)
        controls_bg.grid(row=1, column=0, sticky="ew")
        controls_bg.pack_propagate(False)
        
        controls_frame = tk.Frame(controls_bg, bg=self.colors["dark_blue"])
        controls_frame.pack(expand=True, pady=15)
        
        # Checkboxes com design melhorado
        checkbox_frame = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        checkbox_frame.pack(side="left", padx=(0,30))
        
        tk.Checkbutton(checkbox_frame, text="🔤 Modo Dislexia", 
                      variable=self.use_dyslexic_mode, 
                      command=self.toggle_dyslexic_mode,
                      bg=self.colors["dark_blue"], 
                      fg=self.colors["white"],
                      selectcolor=self.colors["purple"],
                      font=("Segoe UI", 11, "bold"),
                      activebackground=self.colors["dark_blue"],
                      activeforeground=self.colors["white"]).pack(anchor="w", pady=2)
        
        tk.Checkbutton(checkbox_frame, text="🎨 Colorir Sílabas", 
                      variable=self.color_syllables_active, 
                      command=self.update_text_display,
                      bg=self.colors["dark_blue"], 
                      fg=self.colors["white"],
                      selectcolor=self.colors["purple"],
                      font=("Segoe UI", 11, "bold"),
                      activebackground=self.colors["dark_blue"],
                      activeforeground=self.colors["white"]).pack(anchor="w", pady=2)
        
        # Botões de controle
        button_frame = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        button_frame.pack(side="left", padx=20)
        
        # BOTÃO DE LEITURA/PARAR - IGUAL BIBLIOTECA
        self.read_button = tk.Button(button_frame, text="🔊 Ler Texto", 
                                   command=self.toggle_reading,  # Conecta ao toggle
                                   bg=self.colors["green"], fg=self.colors["white"], 
                                   font=("Segoe UI", 12, "bold"), relief="flat", 
                                   padx=20, pady=8, cursor="hand2")
        self.read_button.pack(side="left", padx=(0,10))
        
        # Botão limpar texto
        tk.Button(button_frame, text="🗑️ Limpar", 
                 command=self.clear_text,
                 bg=self.colors["orange"], fg=self.colors["white"], 
                 font=("Segoe UI", 12, "bold"), relief="flat", 
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=10)
        
        # Informações do sistema
        info_frame = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        info_frame.pack(side="left", padx=20)
        
        tk.Label(info_frame, text="🎵 Velocidade: Otimizada", 
                bg=self.colors["dark_blue"], fg=self.colors["white"],
                font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        # Status TTS com verificação em tempo real
        tts_status = "✅ Áudio: Windows SAPI" if SAPI_AVAILABLE else "❌ Áudio: Instalar pywin32"
        tts_color = self.colors["green"] if SAPI_AVAILABLE else "#E74C3C"
        
        tk.Label(info_frame, text=tts_status, 
                bg=self.colors["dark_blue"], 
                fg=tts_color,
                font=("Segoe UI", 9)).pack(anchor="w")

    def clear_text(self):
        """Limpa o texto da área de edição"""
        # Para a leitura se estiver ativa
        if self.is_reading:
            self.stop_reading()
        
        # Limpa o texto
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", "")
        
        print("🗑️ Texto limpo")