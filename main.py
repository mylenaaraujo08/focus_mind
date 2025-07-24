# main.py
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Adiciona o diretório atual ao path para importar os frames
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class FocusMindApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_colors()
        self.setup_frames()
        # MUDANÇA: Inicia com LoginFrame em vez de SelectionFrame
        self.show_frame_by_name("LoginFrame")

    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("FocusMind - Auxiliar de Leitura")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Centraliza a janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configura o fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_colors(self):
        """Define o esquema de cores"""
        self.colors = {
            "beige": "#F5F3F0",
            "white": "#FFFFFF", 
            "dark_blue": "#2C3E50",
            "light_cream": "#FAF8F5",
            "dark_text": "#2C3E50",
            "purple": "#8E44AD",
            "green": "#27AE60",
            "orange": "#E67E22",
            "blue": "#3498DB"
        }

    def setup_frames(self):
        """Configura o container e todos os frames"""
        # Container principal
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dicionário para armazenar os frames
        self.frames = {}

        # Lista dos frames disponíveis (ADICIONADO LoginFrame)
        frame_classes = [
            ("LoginFrame", "frames.login_frame", "LoginFrame"),
            ("SelectionFrame", "frames.selection_frame", "SelectionFrame"),
            ("LeituraFrame", "frames.leitura_frame", "LeituraFrame"),
            ("BibliotecaFrame", "frames.biblioteca_frame", "BibliotecaFrame")
        ]

        # Cria cada frame
        for frame_name, module_name, class_name in frame_classes:
            try:
                # Importa dinamicamente o módulo
                module = __import__(module_name, fromlist=[class_name])
                FrameClass = getattr(module, class_name)
                
                # Cria o frame
                frame = FrameClass(self.container, self, self.colors)
                self.frames[frame_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                
                print(f"✅ Frame {frame_name} carregado com sucesso")
                
            except ImportError as e:
                print(f"❌ Erro ao importar {module_name}: {e}")
                messagebox.showerror("Erro", f"Erro ao carregar {frame_name}:\n{e}")
            except Exception as e:
                print(f"❌ Erro ao criar {frame_name}: {e}")
                messagebox.showerror("Erro", f"Erro ao criar {frame_name}:\n{e}")

    def show_frame(self, frame_class):
        """Mostra um frame específico pela classe"""
        frame_name = frame_class.__name__
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            frame.tkraise()
            print(f"🔄 Exibindo frame: {frame_name}")
        else:
            print(f"❌ Frame não encontrado: {frame_name}")

    def show_frame_by_name(self, frame_name):
        """Mostra um frame específico pelo nome"""
        if frame_name in self.frames:
            frame = self.frames[frame_name]
            frame.tkraise()
            print(f"🔄 Exibindo frame: {frame_name}")
        else:
            print(f"❌ Frame não encontrado: {frame_name}")

    def on_closing(self):
        """Lida com o fechamento da aplicação"""
        try:
            # Para qualquer reprodução de áudio em andamento
            for frame_name, frame in self.frames.items():
                if hasattr(frame, 'stop_reading'):
                    frame.stop_reading()
                elif hasattr(frame, 'is_reading') and frame.is_reading:
                    frame.is_reading = False
            
            print("🔄 Encerrando aplicação...")
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            print(f"❌ Erro ao fechar aplicação: {e}")
            self.root.destroy()

    def run(self):
        """Inicia a aplicação"""
        try:
            print("🚀 Iniciando FocusMind...")
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n⚠️ Aplicação interrompida pelo usuário")
            self.on_closing()
        except Exception as e:
            print(f"❌ Erro na aplicação: {e}")
            messagebox.showerror("Erro Fatal", f"Erro inesperado:\n{e}")

if __name__ == "__main__":
    app = FocusMindApp()
    app.run()