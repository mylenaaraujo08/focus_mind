# main.py
import tkinter as tk
from tkinter import messagebox
import os
import sys

class FocusMindApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FocusMind - Leitura Acessível")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F5F3F0")
        
        self.colors = {
            "beige": "#F5F3F0",
            "white": "#FFFFFF",
            "dark_blue": "#2C3E50", 
            "light_cream": "#FAF8F5",
            "dark_text": "#2C3E50",
            "purple": "#8E44AD",
            "green": "#27AE60",
            "orange": "#E67E22",
            "light_gray": "#E8E8E8",
            "gray": "#CCCCCC",
            "dyslexic_bg": "#FDF6E3",
            "dyslexic_text": "#073642"
        }
        
        self.frames = {}
        self.current_user = None
        
        self.setup_frames()
        self.show_frame_by_name("LoginFrame")

    def setup_frames(self):
        frame_configs = [
            ("frames.login_frame", "LoginFrame"),
            ("frames.register_frame", "RegisterFrame"), 
            ("frames.selection_frame", "SelectionFrame"),
            ("frames.leitura_frame", "LeituraFrame"),
            ("frames.biblioteca_frame", "BibliotecaFrame"),
            ("frames.foco_frame", "FocoFrame"),
            ("frames.forgot_password_frame", "ForgotPasswordFrame")
        ]
        
        for module_name, class_name in frame_configs:
            try:
                print(f"🔄 Carregando {class_name}...")
                
                module = __import__(module_name, fromlist=[class_name])
                frame_class = getattr(module, class_name)
                
                frame = frame_class(self.root, self, self.colors)
                frame.grid(row=0, column=0, sticky="nsew")
                frame.grid_remove()
                
                self.frames[frame_class] = frame
                
                print(f"✅ {class_name} carregado com sucesso")
                
            except Exception as e:
                print(f"❌ Erro ao criar {class_name}: {e}")
                messagebox.showerror("Erro", f"Erro ao criar {class_name}:\n{e}")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def show_frame(self, frame_class):
        try:
            for frame in self.frames.values():
                frame.grid_remove()
            
            if frame_class in self.frames:
                frame = self.frames[frame_class]
                frame.grid()
                frame.tkraise()
                print(f"📱 Exibindo {frame_class.__name__}")
            else:
                print(f"❌ Frame {frame_class.__name__} não encontrado")
                
        except Exception as e:
            print(f"❌ Erro ao exibir frame: {e}")

    def show_frame_by_name(self, frame_name):
        try:
            for frame_class, frame in self.frames.items():
                if frame_class.__name__ == frame_name:
                    self.show_frame(frame_class)
                    return
            print(f"❌ Frame '{frame_name}' não encontrado")
        except Exception as e:
            print(f"❌ Erro ao exibir frame por nome: {e}")

    def set_current_user(self, username):
        self.current_user = username
        print(f"👤 Usuário logado: {username}")

    def get_current_user(self):
        return self.current_user

    def logout(self):
        self.current_user = None
        self.show_frame_by_name("LoginFrame")
        print("🔐 Usuário deslogado")

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n🛑 Aplicação interrompida pelo usuário")
        except Exception as e:
            print(f"❌ Erro na aplicação: {e}")
            messagebox.showerror("Erro Crítico", f"Erro na aplicação:\n{e}")

if __name__ == "__main__":
    app = FocusMindApp()
    app.run()