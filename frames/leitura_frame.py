import tkinter as tk
from tkinter import font, filedialog, messagebox, scrolledtext, simpledialog
import threading, fitz, pyphen
import json
import os
from datetime import datetime

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import win32com.client
    SAPI_AVAILABLE = True
except ImportError:
    SAPI_AVAILABLE = False
    print("❌ Windows SAPI não disponível. Instale com: pip install pywin32")

class LeituraFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors.get("beige", "#F5F3F0"))
        self.controller = controller
        self.colors = colors
        self.stored_files = []
        self.storage_file = "stored_files.json"
        self.max_files = 10
        self.init_dependencies()
        self.load_stored_files()
        self.create_ui()

    def init_dependencies(self):
        self.use_dyslexic_mode = tk.BooleanVar()
        self.color_syllables_active = tk.BooleanVar()
        self.is_reading = False
        self.reading_thread = None
        
        self.colors.update({
            "soft_cream": "#F5F3F0",
            "light_cream": "#FAF8F5",
            "dark_text": "#2C3E50",
            "dyslexic_bg": "#FDF6E3",
            "dyslexic_text": "#073642",
            "beige": "#F5F3F0",
            "white": "#FFFFFF",
            "dark_blue": "#2C3E50",
            "purple": "#8E44AD",
            "green": "#27AE60",
            "orange": "#E67E22"
        })
        
        self.init_tts()
            
        try: 
            self.pyphen_dic = pyphen.Pyphen(lang='pt_BR')
        except Exception: 
            self.pyphen_dic = None
        
        self.default_font = font.Font(family="Segoe UI", size=16, weight="normal")
        
        dyslexic_families = ["OpenDyslexic", "Comic Sans MS", "Verdana", "Tahoma"]
        self.font_available = False
        
        for family in dyslexic_families:
            try: 
                self.dyslexic_font = font.Font(family=family, size=18, weight="normal")
                self.font_available = True
                break
            except tk.TclError: 
                continue
        
        if not self.font_available:
            self.dyslexic_font = font.Font(family="Arial", size=18, weight="normal")

    def init_tts(self):
        try:
            if SAPI_AVAILABLE:
                try:
                    import pythoncom
                    pythoncom.CoInitialize()
                except:
                    pass
                
                if hasattr(self, 'tts_engine') and self.tts_engine:
                    try:
                        del self.tts_engine
                    except:
                        pass
                    self.tts_engine = None
                
                self.tts_engine = win32com.client.Dispatch("SAPI.SpVoice")
                self.tts_engine.Rate = -1
                self.tts_engine.Volume = 100
                
                print("✅ Windows SAPI TTS (Leitura) inicializado com COM")
                return True
            else:
                self.tts_engine = None
                print("❌ Windows SAPI não disponível")
                return False
        except Exception as e:
            self.tts_engine = None
            print(f"❌ Erro ao inicializar SAPI: {e}")
            return False

    def load_stored_files(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.stored_files = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar arquivos armazenados: {e}")
            self.stored_files = []

    def save_stored_files(self):
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.stored_files, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar arquivos armazenados: {e}")

    def speak_text(self, text):
        try:
            try:
                import pythoncom
                pythoncom.CoInitialize()
            except:
                pass
            
            self.init_tts()
            
            if not self.tts_engine:
                self.after_idle(lambda: messagebox.showerror("Erro de Áudio", 
                                   "Sistema de voz não disponível.\nInstale: pip install pywin32"))
                return
            
            if not self.is_reading:
                return
            
            print(f"🔊 Iniciando leitura leitura_frame: {text[:50]}...")
            
            max_chars = 2000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
                print(f"⚠️ Texto limitado a {max_chars} caracteres")
            
            text = text.replace('\n\n\n', '\n\n').strip()
            
            self.tts_engine.Rate = -1
            self.tts_engine.Volume = 100
            
            if self.is_reading:
                self.tts_engine.Speak(text, 0)
                print("✅ Leitura leitura_frame concluída")
            
        except Exception as e:
            print(f"❌ Erro speak_text leitura: {e}")
            error_msg = "Erro na reprodução de áudio."
            if "CoInitialize" in str(e):
                error_msg += "\nProblema de inicialização COM.\nTente reiniciar o aplicativo."
            elif "2147352567" in str(e):
                error_msg += "\nO sistema de voz pode estar ocupado.\nTente novamente em alguns segundos."
            else:
                error_msg += f"\nDetalhes: {str(e)}"
            
            self.after_idle(lambda: messagebox.showerror("Erro", error_msg))
        finally:
            self.is_reading = False
            try:
                import pythoncom
                pythoncom.CoUninitialize()
            except:
                pass
            self.after_idle(self.update_read_button)

    def start_reading(self):
        if self.is_reading:
            self.stop_reading()
            return
            
        text_content = self.text_area.get("1.0", tk.END).strip()
        if not text_content or text_content in ["", "Digite ou cole seu texto aqui..."]:
            messagebox.showwarning("Aviso", "Nenhum texto para ler!\nDigite ou carregue um arquivo primeiro.")
            return
        
        if "Digite ou cole aqui" in text_content:
            messagebox.showwarning("Aviso", "Digite algum texto antes de ler!")
            return
        
        if len(text_content) > 5000:
            result = messagebox.askyesno("Texto Longo", 
                                       f"O texto tem {len(text_content)} caracteres.\nIsto pode causar problemas no áudio.\n\nDeseja continuar?")
            if not result:
                return
        
        print("🔊 Iniciando leitura do texto...")
        
        self.is_reading = True
        self.update_read_button()
        
        self.after(200, lambda: self._delayed_start_reading(text_content))

    def _delayed_start_reading(self, text):
        try:
            if not self.is_reading:
                return
            
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

    def create_ui(self):
        header_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        logo_frame = tk.Frame(header_frame, bg=self.colors["dark_blue"])
        logo_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(logo_frame, text="🧠", font=("Arial", 32), 
                bg=self.colors["dark_blue"], fg="#FFD700").pack(side="left")
        tk.Label(logo_frame, text="FocusMind", font=("Segoe UI", 24, "bold"), 
                bg=self.colors["dark_blue"], fg=self.colors["white"]).pack(side="left", padx=(10,0))
        
        tk.Button(header_frame, text="← Voltar ao Menu", command=self.go_back, 
                 bg="#E74C3C", fg=self.colors["white"], font=("Segoe UI", 12, "bold"), 
                 relief="flat", padx=20, pady=8, cursor="hand2").pack(side="right", padx=20, pady=15)

        title_frame = tk.Frame(self, bg=self.colors["light_cream"], height=60)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="✍️ Leitura Livre", 
                font=("Segoe UI", 26, "bold"), bg=self.colors["light_cream"], 
                fg=self.colors["dark_blue"]).pack(pady=15)

        main_container = tk.Frame(self, bg=self.colors["light_cream"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        self.create_left_panel(main_container)
        self.create_right_panel(main_container)

    def create_left_panel(self, parent):
        left_panel = tk.Frame(parent, bg=self.colors["soft_cream"], bd=2, relief="solid", width=280)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 15))
        left_panel.pack_propagate(False)
        
        tools_title = tk.Frame(left_panel, bg=self.colors["dark_blue"], height=35)
        tools_title.pack(fill="x")
        tools_title.pack_propagate(False)
        
        tk.Label(tools_title, text="🛠️ Ferramentas", 
                font=("Segoe UI", 12, "bold"), bg=self.colors["dark_blue"],
                fg=self.colors["white"]).pack(pady=8)
        
        tools_frame = tk.Frame(left_panel, bg=self.colors["soft_cream"])
        tools_frame.pack(fill="x", padx=8, pady=8)
        
        file_types = "PDF/TXT"
        if DOCX_AVAILABLE:
            file_types += "/DOCX"
        
        tk.Button(tools_frame, text=f"📂 Carregar Arquivo\n({file_types})", 
                 command=self.load_file, 
                 bg=self.colors["purple"], fg=self.colors["white"], 
                 font=("Segoe UI", 11, "bold"), relief="flat", 
                 pady=12, cursor="hand2", wraplength=200).pack(pady=(0,8), fill="x")

        button_row = tk.Frame(tools_frame, bg=self.colors["soft_cream"])
        button_row.pack(fill="x", pady=(0,8))
        
        tk.Button(button_row, text="🗑️ Limpar", command=self.clear_text, 
                 bg="#E74C3C", fg="white", 
                 font=("Segoe UI", 10, "bold"), relief="flat", 
                 pady=8, cursor="hand2").pack(side="left", fill="x", expand=True, padx=(0,4))

        tk.Button(button_row, text="💾 Salvar", command=self.save_text, 
                 bg=self.colors["green"], fg="white", 
                 font=("Segoe UI", 10, "bold"), relief="flat", 
                 pady=8, cursor="hand2").pack(side="left", fill="x", expand=True, padx=(4,0))

        separator = tk.Frame(left_panel, bg=self.colors["dark_blue"], height=2)
        separator.pack(fill="x", pady=10)

        storage_title = tk.Frame(left_panel, bg=self.colors["orange"], height=35)
        storage_title.pack(fill="x")
        storage_title.pack_propagate(False)
        
        title_container = tk.Frame(storage_title, bg=self.colors["orange"])
        title_container.pack(expand=True, fill="both")
        
        self.storage_title_label = tk.Label(title_container, text=f"📚 Arquivos ({len(self.stored_files)}/{self.max_files})", 
                font=("Segoe UI", 11, "bold"), bg=self.colors["orange"],
                fg=self.colors["white"])
        self.storage_title_label.pack(pady=8)

        storage_container = tk.Frame(left_panel, bg=self.colors["soft_cream"])
        storage_container.pack(fill="both", expand=True, padx=8, pady=(8,0))
        
        files_outer_frame = tk.Frame(storage_container, bg=self.colors["soft_cream"])
        files_outer_frame.pack(fill="both", expand=True)
        
        files_frame = tk.Frame(files_outer_frame, bg=self.colors["soft_cream"])
        files_frame.pack(fill="both", expand=True)
        
        self.scrollable_files_frame = tk.Frame(files_frame, bg=self.colors["soft_cream"])
        self.scrollable_files_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.update_files_list()

        tips_frame = tk.Frame(left_panel, bg=self.colors["light_cream"], bd=1, relief="solid")
        tips_frame.pack(fill="x", padx=10, pady=(10,10))
        
        tk.Label(tips_frame, text="💡 Dicas:", 
                font=("Segoe UI", 10, "bold"), bg=self.colors["light_cream"], 
                fg=self.colors["dark_blue"]).pack(pady=(8,4))
        
        tips = [
            "• Clique no arquivo para carregar",
            "• Botão X para remover",
            "• Máximo 10 arquivos salvos"
        ]
        
        for tip in tips:
            tk.Label(tips_frame, text=tip, 
                    font=("Segoe UI", 8), bg=self.colors["light_cream"], 
                    fg=self.colors["dark_text"], justify="left").pack(anchor="w", padx=8, pady=1)
        
        tk.Label(tips_frame, text="", bg=self.colors["light_cream"]).pack(pady=4)

    def update_files_list(self):
        for widget in self.scrollable_files_frame.winfo_children():
            widget.destroy()
        
        if not self.stored_files:
            no_files_label = tk.Label(self.scrollable_files_frame, 
                                     text="📂 Nenhum arquivo salvo\nClique em 'Anexar Arquivo' para adicionar", 
                                     font=("Segoe UI", 10, "italic"), 
                                     bg=self.colors["soft_cream"], 
                                     fg="#888888",
                                     justify="center")
            no_files_label.pack(pady=30)
            return
        
        for i, file_info in enumerate(self.stored_files):
            if isinstance(file_info, str):
                file_name = file_info
                file_path = file_info
            else:
                file_name = file_info.get('name', 'Arquivo sem nome')
                file_path = file_info.get('path', '')
            
            display_name = file_name
            if len(file_name) > 18:
                display_name = file_name[:15] + "..."
            
            file_container = tk.Frame(self.scrollable_files_frame, 
                                 bg="#FFFFFF", 
                                 relief="raised", bd=2)
            file_container.pack(fill="x", pady=3, padx=5)
            
            icon = "📄"
            if file_path.lower().endswith('.pdf'):
                icon = "📕"
            elif file_path.lower().endswith('.docx'):
                icon = "📘"
            elif file_path.lower().endswith('.txt'):
                icon = "📝"
            
            info_frame = tk.Frame(file_container, bg="#FFFFFF")
            info_frame.pack(fill="x", padx=3, pady=3)
            
            name_label = tk.Label(info_frame, 
                                 text=f"{icon} {display_name}",
                                 font=("Segoe UI", 8),
                                 bg="#FFFFFF", 
                                 fg="#2C3E50",
                                 anchor="w")
            name_label.pack(side="left", fill="x", expand=True)
            
            buttons_frame = tk.Frame(info_frame, bg="#FFFFFF")
            buttons_frame.pack(side="right")
            
            open_btn = tk.Button(buttons_frame, 
                               text="📖",  
                               command=lambda idx=i: self.load_stored_file(idx),
                               bg="#3498DB", fg="white",
                               font=("Segoe UI", 10, "bold"),
                               relief="flat", cursor="hand2",
                               width=3, height=1,
                               bd=0, 
                               padx=0, pady=0,
                               anchor="center",
                               justify="center")
            open_btn.pack(side="left", padx=2)
            
            remove_btn = tk.Button(buttons_frame, 
                                 text="✖",
                                 command=lambda idx=i: self.remove_stored_file(idx),
                                 bg="#E74C3C", fg="white",
                                 font=("Arial", 10, "bold"),
                                 relief="flat", cursor="hand2",
                                 width=3, height=1,
                                 bd=0,
                                 padx=0, pady=0,
                                 anchor="center",
                                 justify="center")
            remove_btn.pack(side="left", padx=2)
            
            self.create_button_tooltip(open_btn, "Abrir arquivo")
            self.create_button_tooltip(remove_btn, "Remover da lista")

    def create_tooltip(self, widget, text):
        def on_enter(event):
            widget.configure(bg=self.colors["light_cream"])
        
        def on_leave(event):
            widget.configure(bg=self.colors["white"])
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def create_button_tooltip(self, button, tooltip_text):
        def show_tooltip(event):
            current_bg = button.cget("bg")
            if current_bg == "#3498DB":
                button.configure(bg="#2980B9")
            elif current_bg == "#E74C3C":
                button.configure(bg="#C0392B")
        
        def hide_tooltip(event):
            if "abrir" in tooltip_text.lower():
                button.configure(bg="#3498DB")
            else:
                button.configure(bg="#E74C3C")
        
        button.bind("<Enter>", show_tooltip)
        button.bind("<Leave>", hide_tooltip)

    def load_stored_file(self, index):
        if 0 <= index < len(self.stored_files):
            file_info = self.stored_files[index]
            try:
                if self.is_reading:
                    self.stop_reading()
                
                content = ""
                file_name = file_info.get('name', 'Arquivo sem nome')
                
                if 'content' in file_info and file_info['content']:
                    content = file_info['content']
                    print(f"📂 Carregando conteúdo direto: {file_name}")
                else:
                    file_path = file_info.get('path', '')
                    if file_path and os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        print(f"📂 Carregando arquivo físico: {file_name}")
                    else:
                        messagebox.showerror("Arquivo não encontrado", 
                                           f"O arquivo '{file_name}' não foi encontrado.\nSerá removido da lista.")
                        self.remove_stored_file(index)
                        return
                
                self.set_text(content)
                
                print(f"✅ Arquivo carregado: {file_name}")
                messagebox.showinfo("Arquivo Carregado", f"'{file_name}' foi carregado com sucesso!")
                
            except Exception as e:
                print(f"❌ Erro ao carregar arquivo: {e}")
                messagebox.showerror("Erro", f"Erro ao carregar arquivo '{file_name}':\n{str(e)}")

    def remove_stored_file(self, index):
        if 0 <= index < len(self.stored_files):
            file_info = self.stored_files[index]
            
            if isinstance(file_info, str):
                file_name = file_info
            else:
                file_name = file_info.get('name', 'Arquivo sem nome')
            
            if messagebox.askyesno("Confirmar Remoção", 
                                 f"Remover '{file_name}' da lista de arquivos salvos?"):
                self.stored_files.pop(index)
                self.save_stored_files()
                self.update_files_list()
                self.update_storage_title()
                messagebox.showinfo("Arquivo Removido", f"'{file_name}' foi removido da lista!")

    def update_storage_title(self):
        if hasattr(self, 'storage_title_label'):
            self.storage_title_label.config(text=f"📚 Arquivos ({len(self.stored_files)}/{self.max_files})")

    def store_current_file(self, filepath):
        file_name = os.path.basename(filepath)
        
        for stored_file in self.stored_files:
            if stored_file['path'] == filepath:
                messagebox.showinfo("Arquivo já existe", f"'{file_name}' já está na lista de arquivos salvos.")
                return
        
        if len(self.stored_files) >= self.max_files:
            messagebox.showwarning("Limite atingido", 
                                 f"Máximo de {self.max_files} arquivos permitidos.\nRemova alguns arquivos antes de adicionar novos.")
            return
        
        file_info = {
            'name': file_name,
            'path': filepath
        }
        self.stored_files.append(file_info)
        self.save_stored_files()
        self.update_files_list()
        self.update_storage_title()
        messagebox.showinfo("Arquivo salvo", f"'{file_name}' foi adicionado aos seus arquivos!")

    def create_right_panel(self, parent):
        right_panel = tk.Frame(parent, bg=self.colors["light_cream"])
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        text_container = tk.Frame(right_panel, bg=self.colors["soft_cream"], 
                                 bd=2, relief="solid")
        text_container.grid(row=0, column=0, sticky="nsew", pady=(0,15))
        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)
        
        self.text_area = tk.Text(text_container, 
                               font=self.dyslexic_font if self.font_available else self.default_font, 
                               wrap="word", bd=0, relief="flat",
                               bg=self.colors["soft_cream"],
                               fg=self.colors["dark_text"],
                               insertbackground=self.colors["dark_blue"],
                               padx=20, pady=20, 
                               spacing1=8, spacing2=4, spacing3=8,
                               selectbackground=self.colors["purple"],
                               selectforeground=self.colors["white"])
        self.text_area.grid(row=0, column=0, sticky="nsew")
        
        placeholder = """Digite ou cole aqui o texto que deseja ler...

Você pode:
• Escrever diretamente nesta área
• Carregar um arquivo PDF, TXT ou DOCX
• Salvar arquivos favoritos na lista ao lado
• Usar as opções de acessibilidade abaixo
• Ouvir o texto sendo lido em voz alta

Experimente o Modo Dislexia para uma leitura mais confortável!"""

        self.text_area.insert("1.0", placeholder)
        self.text_area.bind("<KeyPress>", self.on_text_change)
        self.text_area.bind("<Button-1>", self.on_text_click)
        
        self.text_area.tag_configure("highlight", background="#FFE135", foreground=self.colors["dark_text"])
        self.text_area.tag_configure("placeholder", foreground="#888888", font=("Segoe UI", 14, "italic"))
        self.text_area.tag_add("placeholder", "1.0", tk.END)
        
        self.create_controls_panel(right_panel)

    def create_controls_panel(self, parent):
        controls_bg = tk.Frame(parent, bg=self.colors["dark_blue"], height=80)
        controls_bg.grid(row=1, column=0, sticky="ew")
        controls_bg.pack_propagate(False)
        
        controls_frame = tk.Frame(controls_bg, bg=self.colors["dark_blue"])
        controls_frame.pack(expand=True, pady=15)
        
        checkbox_frame = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        checkbox_frame.pack(side="left", padx=(0,30))
        
        tk.Checkbutton(checkbox_frame, text="🧠 Modo Dislexia", 
                      variable=self.use_dyslexic_mode, 
                      command=self.toggle_dyslexic_mode,
                      bg=self.colors["dark_blue"], 
                      fg=self.colors["white"],
                      selectcolor=self.colors["purple"],
                      font=("Segoe UI", 11, "bold"),
                      activebackground=self.colors["dark_blue"],
                      activeforeground=self.colors["white"]).pack(anchor="w", pady=2)
        
        syllable_text = "🎨 Colorir Sílabas"
        if not self.pyphen_dic:
            syllable_text += " (Básico)"
        
        tk.Checkbutton(checkbox_frame, text=syllable_text, 
                      variable=self.color_syllables_active, 
                      command=self.toggle_syllable_coloring,
                      bg=self.colors["dark_blue"], 
                      fg=self.colors["white"],
                      selectcolor=self.colors["purple"],
                      font=("Segoe UI", 11, "bold"),
                      activebackground=self.colors["dark_blue"],
                      activeforeground=self.colors["white"]).pack(anchor="w", pady=2)
        
        button_frame = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        button_frame.pack(side="left", padx=20)
        
        self.read_button = tk.Button(button_frame, text="🔊 Ler Texto", 
                                   command=self.toggle_reading,
                                   bg=self.colors["green"], fg=self.colors["white"], 
                                   font=("Segoe UI", 12, "bold"), relief="flat", 
                                   padx=20, pady=8, cursor="hand2")
        self.read_button.pack(side="left")
        
        info_frame = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        info_frame.pack(side="left", padx=20)
        
        tk.Label(info_frame, text="🎵 Velocidade: Otimizada", 
                bg=self.colors["dark_blue"], fg=self.colors["white"],
                font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        tts_status = "✅ Áudio: Windows SAPI" if SAPI_AVAILABLE else "❌ Áudio: Instalar pywin32"
        tts_color = self.colors["green"] if SAPI_AVAILABLE else "#E74C3C"
        
        tk.Label(info_frame, text=tts_status, 
                bg=self.colors["dark_blue"], 
                fg=tts_color,
                font=("Segoe UI", 9)).pack(anchor="w")
        
        pyphen_status = "✅ Sílabas: Pyphen avançado" if self.pyphen_dic else "⚠️ Sílabas: Modo básico"
        pyphen_color = self.colors["green"] if self.pyphen_dic else self.colors["orange"]
        
        tk.Label(info_frame, text=pyphen_status, 
                bg=self.colors["dark_blue"], 
                fg=pyphen_color,
                font=("Segoe UI", 9)).pack(anchor="w")

    def on_text_click(self, event):
        if self.text_area.tag_ranges("placeholder"):
            self.text_area.delete("1.0", tk.END)
            self.text_area.tag_remove("placeholder", "1.0", tk.END)

    def on_text_change(self, event):
        try:
            if self.text_area.tag_ranges("placeholder"):
                self.text_area.delete("1.0", tk.END)
                self.text_area.tag_remove("placeholder", "1.0", tk.END)
            
            if hasattr(self, 'color_syllables_active') and self.color_syllables_active.get():
                if hasattr(self, '_color_timer'):
                    self.after_cancel(self._color_timer)
                
                self._color_timer = self.after(800, self.apply_syllable_coloring)
                
        except Exception as e:
            print(f"❌ Erro em on_text_change: {e}")

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[
                ("Todos os suportados", "*.txt;*.pdf;*.docx"),
                ("Arquivos de texto", "*.txt"),
                ("Arquivos PDF", "*.pdf"),
                ("Arquivos Word", "*.docx"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            print(f"📁 Carregando arquivo: {file_path}")
            
            if self.is_reading:
                self.stop_reading()
            
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                content = self.load_txt_file(file_path)
            elif file_extension == '.pdf':
                content = self.load_pdf_file(file_path)
            elif file_extension == '.docx':
                content = self.load_docx_file(file_path)
            else:
                content = self.load_txt_file(file_path)
            
            if content:
                self.set_text(content)
                
                print(f"✅ Arquivo carregado: {os.path.basename(file_path)}")
                messagebox.showinfo("Arquivo Carregado", 
                                  f"Arquivo '{os.path.basename(file_path)}' carregado com sucesso!\n\n"
                                  f"Caracteres: {len(content)}\n\n"
                                  f"Use o botão '💾 Salvar' se quiser adicionar à lista.")
                
            else:
                messagebox.showerror("Erro", "Não foi possível carregar o arquivo.\nVerifique se o formato é suportado.")
                
        except Exception as e:
            print(f"❌ Erro ao carregar arquivo: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{str(e)}")

    def load_txt_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            raise Exception("Não foi possível decodificar o arquivo")

    def load_pdf_file(self, file_path):
        try:
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text() + "\n\n"
            return text
        except Exception as e:
            raise Exception(f"Erro ao ler PDF: {str(e)}")

    def load_docx_file(self, file_path):
        if not DOCX_AVAILABLE:
            raise Exception("Biblioteca python-docx não está instalada.\nInstale com: pip install python-docx")
        
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n\n"
            return text
        except Exception as e:
            raise Exception(f"Erro ao ler DOCX: {str(e)}")

    def set_text(self, text):
        try:
            if self.is_reading:
                self.stop_reading()
            
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", text)
            self.text_area.tag_remove("placeholder", "1.0", tk.END)
            
            if hasattr(self, 'color_syllables_active') and self.color_syllables_active.get():
                self.after(300, self.apply_syllable_coloring)
            
            print(f"📝 Texto definido: {len(text)} caracteres")
            
        except Exception as e:
            print(f"❌ Erro ao definir texto: {e}")

    def clear_text(self):
        try:
            if self.is_reading:
                self.stop_reading()
            
            self.text_area.delete("1.0", tk.END)
            
            placeholder = """Digite ou cole aqui o texto que deseja ler...

Você pode:
• Escrever diretamente nesta área
• Carregar um arquivo PDF, TXT ou DOCX
• Salvar arquivos favoritos na lista ao lado
• Usar as opções de acessibilidade abaixo
• Ouvir o texto sendo lido em voz alta

Experimente o Modo Dislexia para uma leitura mais confortável!"""

            self.text_area.insert("1.0", placeholder)
            self.text_area.tag_add("placeholder", "1.0", tk.END)
            
            print("🗑️ Texto limpo")
            
        except Exception as e:
            print(f"❌ Erro ao limpar texto: {e}")

    def go_back(self):
        try:
            if self.is_reading:
                self.stop_reading()
            
            from frames.selection_frame import SelectionFrame
            self.controller.show_frame(SelectionFrame)
            
            print("🔙 Voltando ao menu de seleção")
            
        except Exception as e:
            print(f"❌ Erro ao voltar: {e}")

    def toggle_reading(self):
        if self.is_reading:
            self.stop_reading()
        else:
            self.start_reading()

    def stop_reading(self):
        print("⏹ Parando leitura leitura_frame...")
        self.is_reading = False
        
        if hasattr(self, 'tts_engine') and self.tts_engine:
            try:
                self.tts_engine.Skip("Sentence", 999)
                try:
                    self.tts_engine.Speak("", 2)
                except:
                    pass
            except Exception as e:
                print(f"⚠️ Erro ao parar SAPI: {e}")
                try:
                    del self.tts_engine
                    self.tts_engine = None
                except:
                    pass
        
        self.after(100, self.update_read_button)

    def update_read_button(self):
        try:
            if hasattr(self, 'read_button'):
                if self.is_reading:
                    self.read_button.config(text="⏸️ Parar Leitura", bg="#E74C3C")
                else:
                    self.read_button.config(text="🔊 Ler Texto", bg=self.colors["green"])
        except Exception as e:
            print(f"⚠️ Erro ao atualizar botão: {e}")

    def toggle_dyslexic_mode(self):
        try:
            if self.use_dyslexic_mode.get():
                self.text_area.configure(
                    font=self.dyslexic_font,
                    bg=self.colors["dyslexic_bg"],
                    fg=self.colors["dyslexic_text"],
                    spacing1=12, spacing2=6, spacing3=12
                )
                print("🧠 Modo Dislexia ATIVADO")
            else:
                self.text_area.configure(
                    font=self.default_font,
                    bg=self.colors["soft_cream"],
                    fg=self.colors["dark_text"],
                    spacing1=8, spacing2=4, spacing3=8
                )
                print("📖 Modo Dislexia DESATIVADO")
            
            self.update_text_display()
            
        except Exception as e:
            print(f"❌ Erro ao alternar modo dislexia: {e}")

    def update_text_display(self):
        try:
            if hasattr(self, 'color_syllables_active') and self.color_syllables_active.get():
                self.after(50, self.apply_syllable_coloring)
            else:
                for tag in self.text_area.tag_names():
                    if tag.startswith("syllable_"):
                        self.text_area.tag_delete(tag)
                print("🎨 Coloração de sílabas removida")
        except Exception as e:
            print(f"❌ Erro ao atualizar display: {e}")

    def toggle_syllable_coloring(self):
        try:
            if self.color_syllables_active.get():
                print("🎨 Ativando coloração de sílabas...")
                for tag in self.text_area.tag_names():
                    if tag.startswith("syllable_"):
                        self.text_area.tag_delete(tag)
                self.after(100, self.apply_syllable_coloring)
            else:
                print("🎨 Desativando coloração de sílabas...")
                for tag in self.text_area.tag_names():
                    if tag.startswith("syllable_"):
                        self.text_area.tag_delete(tag)
        except Exception as e:
            print(f"❌ Erro ao alternar coloração: {e}")

    def apply_syllable_coloring(self):
        if not hasattr(self, 'color_syllables_active') or not self.color_syllables_active.get():
            return
        
        try:
            for tag in self.text_area.tag_names():
                if tag.startswith("syllable_"):
                    self.text_area.tag_delete(tag)
            
            content = self.text_area.get("1.0", "end-1c")
            if not content.strip():
                return
            
            if "Digite ou cole aqui" in content:
                return
            
            colors = ["#B3D9FF", "#D1C4E9"]
            
            print(f"🎨 Aplicando coloração COMPLETA em texto de {len(content)} caracteres...")
            
            self.color_text_line_by_line(content, colors)
            
            print("✅ Coloração COMPLETA aplicada - incluindo números e símbolos")
            
        except Exception as e:
            print(f"❌ Erro ao colorir texto completo: {e}")

    def color_text_line_by_line(self, text, colors):
        try:
            lines = text.split('\n')
            
            for line_num, line_content in enumerate(lines, 1):
                if not line_content.strip():
                    continue
                
                char_pos = 0
                i = 0
                
                while i < len(line_content):
                    char = line_content[i]
                    
                    if not char.isspace():
                        word_start = i
                        word = ""
                        
                        while i < len(line_content) and not line_content[i].isspace():
                            word += line_content[i]
                            i += 1
                        
                        if word.strip():
                            self.color_complete_word(word, line_num, char_pos, colors)
                        
                        char_pos += len(word)
                    else:
                        char_pos += 1
                        i += 1
            
        except Exception as e:
            print(f"❌ Erro na coloração linha por linha: {e}")

    def color_complete_word(self, word, line_num, col_start, colors):
        try:
            if not word.strip():
                return
            
            syllables = self.split_complete_word(word)
            
            char_offset = 0
            for syll_index, syllable in enumerate(syllables):
                if syllable:
                    start_pos = f"{line_num}.{col_start + char_offset}"
                    end_pos = f"{line_num}.{col_start + char_offset + len(syllable)}"
                    
                    tag_name = f"syllable_L{line_num}_C{col_start}_O{char_offset}"
                    
                    color = colors[syll_index % 2]
                    
                    try:
                        self.text_area.tag_add(tag_name, start_pos, end_pos)
                        self.text_area.tag_config(tag_name, background=color)
                    except tk.TclError:
                        pass
                
                char_offset += len(syllable)
                
        except Exception as e:
            print(f"❌ Erro ao colorir palavra completa '{word}': {e}")

    def split_complete_word(self, word):
        try:
            if not word:
                return []
            
            syllables = []
            current_part = ""
            current_type = None
            
            for char in word:
                char_type = 'alpha' if (char.isalpha() or char in 'áéíóúâêîôûãõàèìòùç') else 'other'
                
                if current_type is None:
                    current_type = char_type
                    current_part = char
                elif current_type == char_type:
                    current_part += char
                else:
                    if current_type == 'alpha':
                        alpha_syllables = self.split_syllables_advanced(current_part)
                        syllables.extend(alpha_syllables)
                    else:
                        syllables.append(current_part)
                    
                    current_type = char_type
                    current_part = char
            
            if current_part:
                if current_type == 'alpha':
                    alpha_syllables = self.split_syllables_advanced(current_part)
                    syllables.extend(alpha_syllables)
                else:
                    syllables.append(current_part)
            
            return syllables if syllables else [word]
            
        except Exception:
            return [word]

    def split_syllables_advanced(self, word):
        try:
            if hasattr(self, 'pyphen_dic') and self.pyphen_dic:
                try:
                    hyphenated = self.pyphen_dic.inserted(word)
                    syllables = hyphenated.split('-')
                    return syllables
                except:
                    pass
            
            return self.split_syllables_basic(word)
            
        except Exception:
            return [word]

    def split_syllables_basic(self, word):
        if not word:
            return []
        
        vowels = "aeiouáéíóúâêîôûãõàèìòù"
        syllables = []
        current_syllable = ""
        
        i = 0
        while i < len(word):
            char = word[i]
            current_syllable += char
            
            if char.lower() in vowels:
                if i + 1 < len(word):
                    next_char = word[i + 1]
                    
                    if next_char.lower() not in vowels:
                        if i + 2 < len(word) and word[i + 2].lower() in vowels:
                            syllables.append(current_syllable)
                            current_syllable = ""
                    else:
                        syllables.append(current_syllable)
                        current_syllable = ""
                else:
                    syllables.append(current_syllable)
                    current_syllable = ""
            
            i += 1
        
        if current_syllable:
            if syllables:
                syllables[-1] += current_syllable
            else:
                syllables.append(current_syllable)
        
        return syllables if syllables else [word]

    def save_text(self):
        try:
            content = self.text_area.get("1.0", tk.END).strip()
            
            if not content or content == "":
                messagebox.showwarning("Aviso", "Não há texto para salvar!")
                return
            
            if "Digite ou cole aqui" in content:
                messagebox.showwarning("Aviso", "Digite algum texto antes de salvar!")
                return
            
            file_name = simpledialog.askstring("Nome do Arquivo", 
                                             "Digite o nome do arquivo (sem extensão):")
            
            if not file_name:
                return
            
            if not file_name.endswith('.txt'):
                file_name += '.txt'
            
            for i, stored_file in enumerate(self.stored_files):
                existing_name = stored_file.get('name', '')
                if existing_name == file_name:
                    if messagebox.askyesno("Arquivo Existente", 
                                         f"'{file_name}' já existe.\nDeseja substituir?"):
                        self.stored_files.pop(i)
                        break
                    else:
                        return
            
            if len(self.stored_files) >= self.max_files:
                messagebox.showwarning("Limite atingido", 
                                     f"Máximo de {self.max_files} arquivos permitidos.\nRemova alguns arquivos antes de salvar novos.")
                return
            
            file_info = {
                'name': file_name,
                'content': content,
                'saved_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'type': 'saved_text'
            }
            
            self.stored_files.append(file_info)
            self.save_stored_files()
            self.update_files_list()
            self.update_storage_title()
            
            messagebox.showinfo("Texto Salvo", f"'{file_name}' foi salvo com sucesso!")
            print(f"💾 Arquivo salvo: {file_name}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar texto: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar texto:\n{str(e)}")

    def store_current_file(self, file_path, content):
        """Armazena arquivo atual na lista"""
        try:
            file_name = os.path.basename(file_path)
            
            # Verifica se arquivo já está na lista
            for stored_file in self.stored_files:
                if stored_file.get('path') == file_path:
                    messagebox.showinfo("Arquivo já existe", f"'{file_name}' já está na lista de arquivos salvos.")
                    return
            
            # Verifica limite
            if len(self.stored_files) >= self.max_files:
                messagebox.showwarning("Limite atingido", 
                                     f"Máximo de {self.max_files} arquivos permitidos.\nRemova alguns arquivos antes de adicionar novos.")
                return
            
            # Adiciona arquivo à lista
            file_info = {
                'name': file_name,
                'path': file_path,
                'content': content,  # Salva também o conteúdo
                'saved_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'type': 'external_file'
            }
            
            self.stored_files.append(file_info)
            self.save_stored_files()
            self.update_files_list()
            self.update_storage_title()
            
            messagebox.showinfo("Arquivo adicionado", f"'{file_name}' foi adicionado aos seus arquivos!")
            
        except Exception as e:
            print(f"❌ Erro ao armazenar arquivo: {e}")