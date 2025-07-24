# frames/foco_frame.py
import tkinter as tk

class FocoFrame(tk.Frame):
    def __init__(self, parent, controller, colors):
        super().__init__(parent, bg=colors["beige"])
        self.colors = colors
        
        self.timer_running = False
        self.is_focus_time = True
        self.cycles_completed = 0
        self.focus_min = tk.IntVar(value=25)
        self.break_min = tk.IntVar(value=5)
        self.time_left = self.focus_min.get() * 60

        self.mode_label = tk.Label(self, text="Hora de Focar!", font=("Arial", 24, "bold"), bg=colors["beige"], fg=colors["dark_blue"])
        self.mode_label.pack(pady=20)
        
        self.timer_label = tk.Label(self, text=self.format_time(), font=("Arial", 80, "bold"), bg=colors["beige"], fg=colors["dark_blue"])
        self.timer_label.pack(pady=20)

        control_frame = tk.Frame(self, bg=colors["beige"])
        control_frame.pack(pady=10)
        
        self.start_pause_button = tk.Button(control_frame, text="Começar", command=self.toggle_timer, width=10, bg=colors["green"], fg=colors["white"], font=("Arial", 14, "bold"), relief="flat", pady=5)
        self.start_pause_button.pack(side="left", padx=10)
        
        reset_button = tk.Button(control_frame, text="Resetar", command=self.reset_timer, width=10, bg=colors["red"], fg=colors["white"], font=("Arial", 14, "bold"), relief="flat", pady=5)
        reset_button.pack(side="left", padx=10)

        self.cycle_label = tk.Label(self, text=f"Ciclos completos: {self.cycles_completed}", font=("Arial", 14), bg=colors["beige"], fg=colors["dark_blue"])
        self.cycle_label.pack(pady=10)
        
        self.reward_label = tk.Label(self, text="", font=("Arial", 16, "bold"), bg=colors["beige"], fg=colors["green"])
        self.reward_label.pack(pady=10)

        settings_frame = tk.Frame(self, bg=colors["white"], bd=1, relief="solid")
        settings_frame.pack(pady=20, padx=20, fill="x", ipady=10)
        tk.Label(settings_frame, text="Configurar Tempo:", font=("Arial", 12, "bold"), bg=colors["white"], fg=colors["dark_blue"]).pack(pady=5)
        
        tk.Label(settings_frame, text="Foco (min):", font=("Arial", 12), bg=colors["white"], fg=colors["dark_blue"]).pack(side="left", padx=(20, 5))
        tk.Entry(settings_frame, textvariable=self.focus_min, width=5, font=("Arial", 12), bd=1, relief="solid").pack(side="left")
        
        tk.Label(settings_frame, text="Pausa (min):", font=("Arial", 12), bg=colors["white"], fg=colors["dark_blue"]).pack(side="left", padx=(20, 5))
        tk.Entry(settings_frame, textvariable=self.break_min, width=5, font=("Arial", 12), bd=1, relief="solid").pack(side="left", padx=(0, 20))

    def format_time(self):
        mins, secs = divmod(self.time_left, 60)
        return f'{mins:02d}:{secs:02d}'

    def bell(self):
        self.winfo_toplevel().bell()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=self.format_time())
            self.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.bell()
            if self.is_focus_time:
                self.cycles_completed += 1
                self.reward_label.config(text=f"Você completou {self.cycles_completed} ciclo(s)!")
            else:
                self.reward_label.config(text="")
            
            self.is_focus_time = not self.is_focus_time
            self.reset_timer(switch_mode=True)
            self.toggle_timer()

    def toggle_timer(self):
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.start_pause_button.config(text="Pausar", bg="#f39c12")
            self.reward_label.config(text="")
            self.update_timer()
        else:
            self.start_pause_button.config(text="Continuar", bg=self.colors["green"])

    def reset_timer(self, switch_mode=False):
        self.timer_running = False
        self.start_pause_button.config(text="Começar", bg=self.colors["green"])
        
        if not switch_mode:
            self.is_focus_time = True
            self.cycles_completed = 0
            self.reward_label.config(text="")
        
        if self.is_focus_time:
            self.mode_label.config(text="Hora de Focar!")
            self.time_left = self.focus_min.get() * 60
        else:
            self.mode_label.config(text="Faça uma Pausa!")
            self.time_left = self.break_min.get() * 60
            
        self.cycle_label.config(text=f"Ciclos completos: {self.cycles_completed}")
        self.timer_label.config(text=self.format_time())