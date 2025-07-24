import tkinter as tk
from tkinter import messagebox, font
import threading, random, re

try:
    import win32com.client
    SAPI_AVAILABLE = True
except ImportError:
    SAPI_AVAILABLE = False
    print("❌ Windows SAPI não disponível. Instale com: pip install pywin32")

try:
    import pyphen
    PYPHEN_AVAILABLE = True
except ImportError:
    PYPHEN_AVAILABLE = False
    print("❌ Pyphen não disponível. Instale com: pip install pyphen")

class BibliotecaFrame(tk.Frame):
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
            "dyslexic_bg": "#FDF6E3",    
            "dyslexic_text": "#073642"    
        })
        
        self.use_dyslexic_mode = tk.BooleanVar()
        self.color_syllables_active = tk.BooleanVar()
        
        try:
            if PYPHEN_AVAILABLE:
                self.pyphen_dic = pyphen.Pyphen(lang='pt_BR')
            else:
                self.pyphen_dic = None
        except Exception:
            self.pyphen_dic = None
        
        self.init_fonts()
        
        self.stories = {
            "O Patinho Feio": {
                "content": """Era uma vez, numa fazenda muito bonita, uma pata que estava chocando seus ovos. Ela esperava ansiosamente pelo dia em que seus filhotes nasceriam.

Finalmente chegou o grande dia! Um por um, os ovos começaram a se quebrar e lindos patinhos amarelos apareceram. Mas havia um ovo maior que demorou mais para chocar.

Quando finalmente se abriu, saiu um patinho diferente dos outros. Ele era maior, cinzento e não se parecia nada com seus irmãos.

Os outros patinhos começaram a rir dele: "Que patinho feio! Você não é como nós!"

O patinho ficou muito triste e decidiu ir embora da fazenda. Ele caminhou por muito tempo, procurando um lugar onde fosse aceito.

Durante o inverno, o patinho passou muito frio e fome. Mas ele não desistiu de procurar amigos.

Quando a primavera chegou, o patinho viu seu reflexo na água e ficou surpreso. Ele não era mais um patinho feio - havia se transformado em um lindo cisne branco!

Os outros cisnes o receberam com alegria, e ele finalmente encontrou sua verdadeira família.

Moral da história: Todos nós temos nossa beleza única, e às vezes precisamos de tempo para descobrir quem realmente somos."""
            },
            
            "Os Três Porquinhos": {
                "content": """Era uma vez três porquinhos que decidiram construir suas próprias casas.

O primeiro porquinho, que era preguiçoso, construiu sua casa de palha muito rapidamente. "Pronto! Agora posso brincar o dia todo", disse ele.

O segundo porquinho construiu sua casa de madeira. Demorou um pouco mais, mas logo estava terminada.

O terceiro porquinho, que era muito trabalhador, decidiu construir sua casa de tijolos. Seus irmãos riram dele: "Por que você está trabalhando tanto? Nossas casas já estão prontas!"

Mas o terceiro porquinho continuou trabalhando duro até sua casa ficar bem forte.

Um dia, um lobo mau chegou na floresta com muita fome. Ele foi até a casa de palha e soprou: "Vou soprar, vou bufar e sua casa vou derrubar!"

A casa de palha voou pelos ares! O primeiro porquinho correu para a casa do irmão.

O lobo foi até a casa de madeira e soprou ainda mais forte. A casa de madeira também caiu! Os dois porquinhos correram para a casa de tijolos.

O lobo soprou e bufou, mas a casa de tijolos era muito forte e não caiu.

Furioso, o lobo tentou entrar pela chaminé, mas o porquinho esperto tinha posto uma panela de água fervendo embaixo.

O lobo caiu na água quente e saiu correndo, prometendo nunca mais incomodar os três porquinhos.

Moral da história: O trabalho duro e o planejamento nos protegem dos problemas."""
            },
            
            "Chapeuzinho Vermelho": {
                "content": """Era uma vez uma menina que sempre usava uma capa vermelha com capuz. Por isso, todos a chamavam de Chapeuzinho Vermelho.

Um dia, sua mãe lhe pediu para levar uma cesta com doces para a vovó, que estava doente.

"Vá pela estrada principal e não converse com estranhos", alertou a mãe.

Chapeuzinho Vermelho pegou a cesta e foi caminhando pela floresta, cantando alegremente.

No meio do caminho, encontrou um lobo que perguntou: "Para onde você está indo, menina?"

Chapeuzinho, esquecendo do conselho da mãe, respondeu: "Vou levar doces para minha vovó que mora na casinha amarela."

O lobo, que era muito esperto e malvado, correu por um atalho e chegou primeiro na casa da vovó.

Ele trancou a vovó no armário e se vestiu com suas roupas, deitando na cama para esperar Chapeuzinho.

Quando a menina chegou, estranhou a aparência da vovó:
"Vovó, que olhos grandes você tem!"
"É para te ver melhor", respondeu o lobo.
"Vovó, que dentes grandes você tem!"
"É para te comer melhor!", gritou o lobo saltando da cama.

Por sorte, um lenhador que passava por ali ouviu os gritos, entrou na casa e expulsou o lobo malvado.

Chapeuzinho libertou sua vovó e prometeu nunca mais desobedecer à sua mãe.

Moral da história: Devemos sempre ouvir os conselhos de quem nos ama e nunca confiar em estranhos."""
            },
            
            "A Cigarra e a Formiga": {
                "content": """Durante todo o verão, a cigarra cantou alegremente sob o sol quente, sem se preocupar com mais nada.

Enquanto isso, a formiga trabalhava duro, carregando grãos e comida para guardar em sua casa.

"Por que você trabalha tanto?", perguntou a cigarra. "Vem cantar comigo! O sol está lindo e a vida é boa!"

"Não posso", respondeu a formiga. "Preciso me preparar para o inverno. Você deveria fazer o mesmo."

A cigarra riu: "Inverno? Isso ainda está longe! Prefiro aproveitar este momento."

Mas os dias passaram, o outono chegou e logo veio o inverno rigoroso.

A cigarra, tremendo de frio e com muita fome, foi bater na porta da formiga.

"Por favor, me ajude! Estou com frio e fome, e não tenho onde me abrigar."

A formiga, que tinha coração bondoso, abriu a porta: "Entre, mas primeiro me conte: o que você fez durante todo o verão?"

"Eu cantei", respondeu a cigarra, envergonhada.

"Então agora dance para se aquecer", disse a formiga com um sorriso. "Mas não se preocupe, vou compartilhar minha comida com você. Só prometa que no próximo verão vai me ajudar a trabalhar."

A cigarra prometeu e aprendeu que é importante equilibrar diversão com responsabilidade.

Moral da história: É bom se divertir, mas também devemos nos preparar para os momentos difíceis."""
            },
            
            "A Lebre e a Tartaruga": {
                "content": """Era uma vez uma lebre muito vaidosa que vivia se gabando de ser a mais rápida da floresta.

Um dia, ela encontrou uma tartaruga e começou a rir: "Você é tão devagar! Aposto que nunca conseguiria me vencer numa corrida!"

A tartaruga, calmamente, aceitou o desafio: "Aceito sua aposta. Vamos correr até aquela árvore grande."

Todos os animais da floresta vieram assistir à corrida. A raposa foi escolhida para dar a largada.

"Preparar... Apontar... JÁ!"

A lebre saiu disparada, deixando a tartaruga para trás. Em pouco tempo, estava muito à frente.

"Isso é fácil demais!", pensou a lebre. "Vou tirar uma soneca debaixo desta árvore. Quando acordar, ainda terei tempo de sobra para ganhar."

E assim fez. Deitou-se na sombra e dormiu profundamente.

Enquanto isso, a tartaruga continuou caminhando devagar, mas sem parar nem um minuto.

Passo a passo, ela passou pela lebre adormecida e continuou em direção à linha de chegada.

Quando a lebre acordou, viu a tartaruga quase chegando ao fim! Correu o mais rápido que pôde, mas já era tarde.

A tartaruga havia vencido! Todos os animais aplaudiram e comemoraram.

A lebre aprendeu uma lição valiosa naquele dia.

Moral da história: Devagar e sempre se chega na frente. A perseverança vale mais que a velocidade."""
            },
            
            "A Raposa e as Uvas": {
                "content": """Era um dia muito quente de verão. Uma raposa caminhava pela floresta quando sentiu uma sede terrível.

Procurou por todos os lados: riachos secos, poças vazias. Não havia água em lugar nenhum.

De repente, avistou uma parreira carregada de uvas roxas e suculentas.

"Que maravilha!", exclamou. "Essas uvas vão matar minha sede!"

A raposa correu até a parreira e deu um grande salto, tentando alcançar as uvas. Mas elas estavam muito altas.

Tentou novamente, saltando ainda mais alto. Nada! As uvas continuavam fora de seu alcance.

Correu, tomou impulso e saltou com todas as suas forças. Quase conseguiu tocar uma uva com a ponta do focinho, mas não foi suficiente.

Tentou subir no tronco da videira, mas era muito liso e ela escorregava.

Depois de uma hora tentando, a raposa estava exausta e ainda mais sedenta.

Olhou mais uma vez para as uvas apetitosas e disse em voz alta:

"Bah! Aposto que essas uvas estão verdes e azedas mesmo! Não prestam para nada!"

E saiu andando, fingindo que não se importava.

Mas no fundo, ela sabia que as uvas estavam maduras e doces. Só não conseguia admitir que havia falhado.

Moral da história: É fácil desprezar aquilo que não conseguimos alcançar."""
            }
        }
        
        self.current_story = ""
        self.is_reading = False
        
        self.init_tts()
        self.create_ui()

    def init_fonts(self):
        """Inicializa as fontes para leitura normal e dislexia"""
        try:
            self.default_font = font.Font(family="Segoe UI", size=14, weight="normal")
            
            dyslexic_families = ["OpenDyslexic", "Comic Sans MS", "Verdana", "Tahoma"]
            self.font_available = False
            
            for family in dyslexic_families:
                try:
                    self.dyslexic_font = font.Font(family=family, size=16, weight="normal")
                    self.font_available = True
                    break
                except tk.TclError:
                    continue
            
            if not self.font_available:
                self.dyslexic_font = font.Font(family="Arial", size=16, weight="normal")
                
        except Exception as e:
            print(f"❌ Erro ao configurar fontes: {e}")
            self.default_font = None
            self.dyslexic_font = None

    def init_tts(self):
        """Inicializa Windows SAPI TTS de forma mais robusta"""
        try:
            if SAPI_AVAILABLE:
                if hasattr(self, 'tts_engine') and self.tts_engine:
                    try:
                        del self.tts_engine
                    except:
                        pass
                    self.tts_engine = None
                
                self.tts_engine = win32com.client.Dispatch("SAPI.SpVoice")
                
                self.tts_engine.Rate = -2 
                self.tts_engine.Volume = 100
                
                print("✅ Windows SAPI TTS (Biblioteca) inicializado")
            else:
                self.tts_engine = None
                print("❌ Windows SAPI não disponível")
        except Exception as e:
            self.tts_engine = None
            print(f"❌ Erro ao inicializar SAPI: {e}")

    def toggle_dyslexic_mode(self):
        """Alterna modo para dislexia"""
        if self.use_dyslexic_mode.get():
            self.story_text.config(
                bg=self.colors["dyslexic_bg"],
                fg=self.colors["dyslexic_text"],
                font=self.dyslexic_font if self.dyslexic_font else ("Arial", 16)
            )
            print("✅ Modo Dislexia ATIVADO")
        else:
            self.story_text.config(
                bg=self.colors["white"],
                fg=self.colors["dark_text"],
                font=self.default_font if self.default_font else ("Segoe UI", 14)
            )
            print("❌ Modo Dislexia DESATIVADO")
        
        # Reaplica coloração de sílabas se estiver ativa
        if self.color_syllables_active.get():
            self.apply_syllable_coloring()

    def separate_syllables(self, word):
        """Separa palavra em sílabas usando pyphen"""
        if not self.pyphen_dic:
            return self.simple_syllable_split(word)
        
        try:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if not clean_word:
                return [word]
            
            syllables = self.pyphen_dic.inserted(clean_word).split('-')
            
            if len(syllables) == 1:
                return self.simple_syllable_split(word)
            
            result = []
            char_index = 0
            for syllable in syllables:
                original_part = word[char_index:char_index + len(syllable)]
                result.append(original_part)
                char_index += len(syllable)
            
            if char_index < len(word):
                if result:
                    result[-1] += word[char_index:]
                else:
                    result.append(word[char_index:])
            
            return result
            
        except Exception:
            return self.simple_syllable_split(word)

    def simple_syllable_split(self, word):
        """Separação simples de sílabas como fallback"""
        vowels = 'aeiouáéíóúâêîôûãõ'
        syllables = []
        current = ""
        
        for i, char in enumerate(word.lower()):
            current += word[i]  
            
            if char in vowels:
                if i + 1 < len(word):
                    next_char = word[i + 1].lower()
                    if next_char not in vowels:
                        if i + 2 < len(word) and word[i + 2].lower() in vowels:
                            syllables.append(current)
                            current = ""
                else:
                    syllables.append(current)
                    current = ""
        
        if current:
            syllables.append(current)
        
        return syllables if syllables else [word]

    def apply_syllable_coloring(self):
        """Aplica coloração alternada às sílabas"""
        if not self.color_syllables_active.get():
            return
        
        try:
            for tag in self.story_text.tag_names():
                if tag.startswith("syllable_"):
                    self.story_text.tag_delete(tag)
            
            content = self.story_text.get("1.0", "end-1c")
            
            colors = ["#B3D9FF", "#D1C4E9"] 
            
            lines = content.split('\n')
            current_line = 1
            current_col = 0
            
            for line in lines:
                words = line.split(' ')
                line_col = 0
                
                for word_index, word in enumerate(words):
                    if not word.strip():
                        line_col += 1
                        continue
                    
                    syllables = self.separate_syllables(word)
                    char_offset = 0
                    
                    for syll_index, syllable in enumerate(syllables):
                        if syllable.strip():
                            start_pos = f"{current_line}.{line_col + char_offset}"
                            end_pos = f"{current_line}.{line_col + char_offset + len(syllable)}"
                            
                            color = colors[syll_index % 2]  
                            tag_name = f"syllable_{current_line}_{line_col}_{syll_index}"
                            
                            self.story_text.tag_add(tag_name, start_pos, end_pos)
                            self.story_text.tag_config(tag_name, background=color, foreground="#2C3E50")  
                        
                        char_offset += len(syllable)
                    
                    line_col += len(word)
                    if word_index < len(words) - 1:
                        line_col += 1  
                
                current_line += 1
            
            print("✅ Coloração de sílabas aplicada (2 cores suaves)")
            
        except Exception as e:
            print(f"❌ Erro ao colorir sílabas: {e}")

    def speak_text(self, text):
        """Fala o texto usando TTS de forma mais robusta"""
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
            
            max_chars = 2000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            
            self.tts_engine.Rate = -2
            
            if self.is_reading:
                self.tts_engine.Speak(text, 0)
            
        except Exception as e:
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
            self.after_idle(self.update_play_button)

    def stop_reading(self):
        """Para a leitura de forma mais robusta"""
        print("⏹ Parando leitura biblioteca...")
        self.is_reading = False
        
        if self.tts_engine:
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
        
        self.after(100, self.update_play_button)

    def start_reading(self):
        """Inicia leitura da história com verificações extras"""
        if self.is_reading:
            self.stop_reading()
            return
            
        story_text = self.story_text.get("1.0", tk.END).strip()
        if not story_text or story_text.startswith("Selecione uma história"):
            messagebox.showwarning("Aviso", "Nenhuma história carregada!")
            return
        
        if len(story_text) > 5000:
            result = messagebox.askyesno("Texto Longo", 
                                       f"O texto tem {len(story_text)} caracteres.\nIsto pode causar problemas no áudio.\n\nDeseja continuar?")
            if not result:
                return
        
        self.is_reading = True
        self.update_play_button()
        
        self.after(200, lambda: self._delayed_start_reading(story_text))

    def _delayed_start_reading(self, text):
        """Inicia leitura com delay para garantir limpeza"""
        try:
            self.reading_thread = threading.Thread(
                target=self.speak_text, 
                args=(text,), 
                daemon=True
            )
            self.reading_thread.start()
        except Exception as e:
            self.is_reading = False
            self.update_play_button()

    def toggle_reading(self):
        """Alterna entre ler e parar"""
        if self.is_reading:
            self.stop_reading()
        else:
            self.start_reading()

    def update_play_button(self):
        """Atualiza botão de play/pause"""
        try:
            if hasattr(self, 'play_button'):
                if self.is_reading:
                    self.play_button.config(text="⏸️ Pausar", bg="#E74C3C")
                else:
                    self.play_button.config(text="▶️ Reproduzir", bg="#27AE60")
        except:
            pass

    def toggle_syllable_coloring(self):
        """Alterna coloração de sílabas"""
        if self.color_syllables_active.get():
            self.apply_syllable_coloring()
            print("✅ Coloração de sílabas ATIVADA")
        else:
            # Remove todas as tags de sílabas
            for tag in self.story_text.tag_names():
                if tag.startswith("syllable_"):
                    self.story_text.tag_delete(tag)
            print("❌ Coloração de sílabas DESATIVADA")

    def speak_text(self, text):
        """Fala o texto usando TTS de forma mais robusta"""
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
            self.update_play_button()
            
            print(f"🔊 Iniciando leitura da história: {text[:50]}...")
            
            # Limita o tamanho do texto para evitar travamentos
            max_chars = 2000  # Limita para evitar textos muito longos
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
                print(f"⚠️ Texto limitado a {max_chars} caracteres")
            
            # Configura velocidade para histórias
            self.tts_engine.Rate = -2
            
            # Usa SAPI para falar - modo síncrono com timeout
            try:
                self.tts_engine.Speak(text, 0)  # 0 = síncrono
                print("✅ Leitura biblioteca concluída")
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
            print(f"❌ Erro speak_text: {e}")
            error_msg = "Erro na reprodução de áudio."
            if "2147352567" in str(e):
                error_msg += "\nO sistema de voz pode estar ocupado.\nTente novamente em alguns segundos."
            else:
                error_msg += f"\nDetalhes: {str(e)}"
            messagebox.showerror("Erro", error_msg)
        finally:
            self.is_reading = False
            self.after_idle(self.update_play_button)

    def stop_reading(self):
        """Para a leitura de forma mais robusta"""
        print("⏹ Parando leitura biblioteca...")
        self.is_reading = False
        
        if self.tts_engine:
            try:
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
        
        self.after(100, self.update_play_button)

    def start_reading(self):
        """Inicia leitura da história com verificações extras"""
        if self.is_reading:
            self.stop_reading()
            return
            
        story_text = self.story_text.get("1.0", tk.END).strip()
        if not story_text or story_text.startswith("Selecione uma história"):
            messagebox.showwarning("Aviso", "Nenhuma história carregada!")
            return
        
        if len(story_text) > 5000:
            result = messagebox.askyesno("Texto Longo", 
                                       f"O texto tem {len(story_text)} caracteres.\nIsto pode causar problemas no áudio.\n\nDeseja continuar?")
            if not result:
                return
        
        print("🔊 Iniciando leitura da história...")
        
        self.stop_reading()
        
        self.after(200, lambda: self._delayed_start_reading(story_text))

    def _delayed_start_reading(self, text):
        """Inicia leitura com delay para garantir limpeza"""
        try:
            self.reading_thread = threading.Thread(
                target=self.speak_text, 
                args=(text,), 
                daemon=True
            )
            self.reading_thread.start()
        except Exception as e:
            print(f"❌ Erro ao criar thread de leitura: {e}")
            self.is_reading = False
            self.update_play_button()

    def load_story(self, story_name):
        """Carrega uma história específica"""
        if story_name in self.stories:
            self.current_story = story_name
            story_content = self.stories[story_name]["content"]
            
            self.story_text.config(state="normal")
            self.story_text.delete("1.0", tk.END)
            
            self.story_text.insert("1.0", story_content)
            self.story_text.config(state="disabled")
            
            self.story_title.config(text=f"📖 {story_name}")
            
            if self.use_dyslexic_mode.get():
                self.toggle_dyslexic_mode()
            
            if self.color_syllables_active.get():
                self.story_text.config(state="normal")
                self.apply_syllable_coloring()
                self.story_text.config(state="disabled")
            
            print(f"📚 História carregada: {story_name}")

    def random_story(self):
        """Carrega uma história aleatória"""
        story_name = random.choice(list(self.stories.keys()))
        self.load_story(story_name)

    def create_ui(self):
        """Cria a interface do usuário"""
        # Header com logo e título
        header_frame = tk.Frame(self, bg=self.colors["dark_blue"], height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Logo à esquerda
        logo_frame = tk.Frame(header_frame, bg=self.colors["dark_blue"])
        logo_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(logo_frame, text="🧠", font=("Arial", 32), 
                bg=self.colors["dark_blue"], fg="#FFD700").pack(side="left")
        tk.Label(logo_frame, text="FocusMind", font=("Segoe UI", 24, "bold"), 
                bg=self.colors["dark_blue"], fg=self.colors["white"]).pack(side="left", padx=(10,0))
        
        # Botão voltar à direita
        tk.Button(header_frame, text="← Voltar ao Menu", command=self.go_back, 
                 bg="#E74C3C", fg=self.colors["white"], font=("Segoe UI", 12, "bold"), 
                 relief="flat", padx=20, pady=8, cursor="hand2").pack(side="right", padx=20, pady=15)

        # Título da seção
        title_frame = tk.Frame(self, bg=self.colors["light_cream"], height=60)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📚 Biblioteca de Histórias", 
                font=("Segoe UI", 26, "bold"), bg=self.colors["light_cream"], 
                fg=self.colors["dark_blue"]).pack(pady=15)

        # Container principal
        main_container = tk.Frame(self, bg=self.colors["light_cream"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Painel esquerdo - Seleção de histórias
        left_panel = tk.Frame(main_container, bg=self.colors["white"], 
                             bd=2, relief="solid", width=280)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Título da seleção
        selection_title = tk.Frame(left_panel, bg=self.colors["purple"], height=45)
        selection_title.pack(fill="x")
        selection_title.pack_propagate(False)
        
        tk.Label(selection_title, text="📖 Escolha uma História", 
                font=("Segoe UI", 14, "bold"), bg=self.colors["purple"], 
                fg=self.colors["white"]).pack(pady=12)

        # Status do sistema
        status_frame = tk.Frame(left_panel, bg=self.colors["white"])
        status_frame.pack(fill="x", padx=10, pady=10)
        
        # Status áudio
        audio_status = "✅ Áudio: Windows SAPI" if SAPI_AVAILABLE else "❌ Áudio: Não disponível"
        audio_color = self.colors["green"] if SAPI_AVAILABLE else "#E74C3C"
        
        tk.Label(status_frame, text=audio_status, 
                font=("Segoe UI", 9), bg=self.colors["white"], 
                fg=audio_color).pack()
        
        # Status pyphen
        pyphen_status = "✅ Sílabas: Pyphen" if PYPHEN_AVAILABLE else "⚠️ Sílabas: Básico"
        pyphen_color = self.colors["green"] if PYPHEN_AVAILABLE else self.colors["orange"]
        
        tk.Label(status_frame, text=pyphen_status, 
                font=("Segoe UI", 9), bg=self.colors["white"], 
                fg=pyphen_color).pack()

        # SEÇÃO DE ACESSIBILIDADE
        accessibility_frame = tk.LabelFrame(left_panel, text="♿ Acessibilidade", 
                                          font=("Segoe UI", 11, "bold"),
                                          bg=self.colors["white"], fg=self.colors["purple"],
                                          relief="groove", bd=2)
        accessibility_frame.pack(fill="x", padx=10, pady=10)

        # Checkbox Modo Dislexia
        dyslexia_frame = tk.Frame(accessibility_frame, bg=self.colors["white"])
        dyslexia_frame.pack(fill="x", padx=5, pady=5)
        
        tk.Checkbutton(dyslexia_frame, text="🧠 Modo Dislexia", 
                      variable=self.use_dyslexic_mode,
                      command=self.toggle_dyslexic_mode,
                      bg=self.colors["white"], fg=self.colors["dark_text"],
                      font=("Segoe UI", 10), selectcolor=self.colors["light_cream"],
                      activebackground=self.colors["white"]).pack(anchor="w")

        # Checkbox Colorir Sílabas
        syllables_frame = tk.Frame(accessibility_frame, bg=self.colors["white"])
        syllables_frame.pack(fill="x", padx=5, pady=(0,5))
        
        tk.Checkbutton(syllables_frame, text="🎨 Colorir Sílabas", 
                      variable=self.color_syllables_active,
                      command=self.toggle_syllable_coloring,
                      bg=self.colors["white"], fg=self.colors["dark_text"],
                      font=("Segoe UI", 10), selectcolor=self.colors["light_cream"],
                      activebackground=self.colors["white"]).pack(anchor="w")

        # Botões das histórias
        stories_frame = tk.Frame(left_panel, bg=self.colors["white"])
        stories_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botão história aleatória
        tk.Button(stories_frame, text="🎲 História Aleatória", 
                 command=self.random_story,
                 bg=self.colors["orange"], fg=self.colors["white"], 
                 font=("Segoe UI", 12, "bold"), relief="flat", 
                 pady=10, cursor="hand2").pack(fill="x", pady=(0,10))
        
        # Botões para cada história
        for story_name in self.stories.keys():
            tk.Button(stories_frame, text=f"📚 {story_name}", 
                     command=lambda name=story_name: self.load_story(name),
                     bg=self.colors["purple"], fg=self.colors["white"], 
                     font=("Segoe UI", 10, "bold"), relief="flat", 
                     pady=8, cursor="hand2", wraplength=220).pack(fill="x", pady=2)

        # Painel direito - Texto da história
        right_panel = tk.Frame(main_container, bg=self.colors["light_cream"])
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Título da história atual
        self.story_title = tk.Label(right_panel, text="📖 Selecione uma história", 
                                   font=("Segoe UI", 20, "bold"), 
                                   bg=self.colors["light_cream"], 
                                   fg=self.colors["dark_blue"])
        self.story_title.grid(row=0, column=0, pady=(0,15))

        # Área de texto da história
        text_container = tk.Frame(right_panel, bg=self.colors["white"], 
                                 bd=2, relief="solid")
        text_container.grid(row=1, column=0, sticky="nsew", pady=(0,15))
        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)

        self.story_text = tk.Text(text_container, 
                                 font=self.default_font if self.default_font else ("Segoe UI", 14),
                                 wrap="word", 
                                 bd=0, relief="flat",
                                 bg=self.colors["white"], 
                                 fg=self.colors["dark_text"],
                                 padx=20, pady=20, 
                                 spacing1=5, spacing2=3, spacing3=5,
                                 state="disabled")  # Somente leitura
        self.story_text.grid(row=0, column=0, sticky="nsew")

        # Scrollbar para o texto
        scrollbar = tk.Scrollbar(text_container, command=self.story_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.story_text.config(yscrollcommand=scrollbar.set)

        # Placeholder inicial
        self.story_text.config(state="normal")
        self.story_text.insert("1.0", "Selecione uma história no painel à esquerda para começar a ler! 📚\n\nVocê pode escolher entre várias histórias clássicas ou usar o botão 'História Aleatória' para uma surpresa.\n\nDepois de carregar uma história, use o botão 'Reproduzir' para ouvir a narração.\n\n♿ Use as opções de acessibilidade para ativar o Modo Dislexia e colorir as sílabas!")
        self.story_text.config(state="disabled")

        # Painel de controles
        controls_frame = tk.Frame(right_panel, bg=self.colors["dark_blue"], height=70)
        controls_frame.grid(row=2, column=0, sticky="ew")
        controls_frame.pack_propagate(False)
        
        controls_container = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        controls_container.pack(expand=True, pady=15)
        
        # Botão de reprodução
        self.play_button = tk.Button(controls_container, text="▶️ Reproduzir", 
                                   command=self.toggle_reading,
                                   bg=self.colors["green"], fg=self.colors["white"], 
                                   font=("Segoe UI", 14, "bold"), relief="flat", 
                                   padx=30, pady=10, cursor="hand2")
        self.play_button.pack(side="left", padx=20)

        # Label de instruções
        tk.Label(controls_container, text="🎧 Clique para ouvir a história", 
                font=("Segoe UI", 12), bg=self.colors["dark_blue"], 
                fg=self.colors["white"]).pack(side="left", padx=20)

    def go_back(self):
        """Volta para o menu principal"""
        # Para qualquer reprodução em andamento
        self.stop_reading()
        
        # Volta para a tela de seleção
        from frames.selection_frame import SelectionFrame
        self.controller.show_frame(SelectionFrame)

    def clear_text(self):
        """Limpa o texto da área de leitura"""
        try:
            # Para qualquer leitura ativa
            if self.is_reading:
                self.stop_reading()
            
            # Limpa o texto da área de leitura
            self.reading_area.config(state="normal")
            self.reading_area.delete("1.0", tk.END)
            
            # Insere placeholder
            placeholder_text = "Nenhum arquivo selecionado.\nEscolha um arquivo da lista ao lado para visualizar e ouvir o conteúdo."
            self.reading_area.insert("1.0", placeholder_text)
            self.reading_area.tag_add("placeholder", "1.0", tk.END)
            self.reading_area.config(state="disabled")
            
            # Limpa informações do arquivo atual
            self.current_file_content = ""
            self.current_file_name = "Nenhum arquivo selecionado"
            
            print("🗑️ Área de leitura limpa")
            
        except Exception as e:
            print(f"❌ Erro ao limpar texto: {e}")

    def create_controls_panel(self, parent):
        """Cria painel de controles"""
        controls_bg = tk.Frame(parent, bg=self.colors["dark_blue"], height=80)
        controls_bg.grid(row=1, column=0, sticky="ew")
        controls_bg.pack_propagate(False)
        
        controls_frame = tk.Frame(controls_bg, bg=self.colors["dark_blue"])
        controls_frame.pack(expand=True, pady=15)
        
        # Checkboxes
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
        
        # Botões de controle
        button_frame = tk.Frame(controls_frame, bg=self.colors["dark_blue"])
        button_frame.pack(side="left", padx=20)
        
        # Botão de leitura/parar
        self.read_button = tk.Button(button_frame, text="🔊 Ler Texto", 
                                   command=self.toggle_reading,
                                   bg=self.colors["green"], fg=self.colors["white"], 
                                   font=("Segoe UI", 12, "bold"), relief="flat", 
                                   padx=20, pady=8, cursor="hand2")
        self.read_button.pack(side="left", padx=(0,10))
        
        # ADICIONADO: Botão limpar texto
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
        
        # Status TTS
        tts_status = "✅ Áudio: Windows SAPI" if SAPI_AVAILABLE else "❌ Áudio: Instalar pywin32"
        tts_color = self.colors["green"] if SAPI_AVAILABLE else "#E74C3C"
        
        tk.Label(info_frame, text=tts_status, 
                bg=self.colors["dark_blue"], 
                fg=tts_color,
                font=("Segoe UI", 9)).pack(anchor="w")
        
        # Status Pyphen
        pyphen_status = "✅ Sílabas: Pyphen avançado" if self.pyphen_dic else "⚠️ Sílabas: Modo básico"
        pyphen_color = self.colors["green"] if self.pyphen_dic else self.colors["orange"]
        
        tk.Label(info_frame, text=pyphen_status, 
                bg=self.colors["dark_blue"], 
                fg=pyphen_color,
                font=("Segoe UI", 9)).pack(anchor="w")