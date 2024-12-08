import customtkinter as ctk
import tkinter as tk
import webbrowser
import subprocess
import os
import threading

from services.threads_manager import ThreadsManager
from services.processes_manager import ProcessManager
from services.tetris_game import TetrisGame
from services.system_monitor import SystemMonitor


class CenteredWindow(ctk.CTk):
    def __init__(self, title="MultiApp", width_percentage=0.8, height_percentage=0.8):
        # Inicializacion de la clase:
        super().__init__()
        self.title(title)

        # Inicializar managers (orden es importante)
        self.thread_manager = ThreadsManager(self)
        self.process_manager = ProcessManager()
        self.system_monitor = None

        # Obtener la resolucion de la pantalla:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula el tamaño de la ventana según procentaje de la pantalla:
        window_width = int(screen_width * width_percentage)
        window_height = int(screen_height * height_percentage)

        # Calcular la posicion para centrar la ventana:
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        #Configura la ventana
        self.configure_window()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_window(self):
        # Configuracion de la ventana:
        self.configure(bg_color="lightgray")
        self.create_left_panel()
        self.create_right_panel()
        self.create_center_panel()
        self.create_bottom_bar()

        self.thread_manager.start_threads()

    

    def on_close(self):
        """Maneja el cierre de la ventana"""
        self.thread_manager.stop_threads()

        if hasattr(self, "tetris_game") and self.tetris_game.running:
            self.tetris_game.stop_game()

        if "tetris_game" in self.thread_manager.tasks:  
            self.thread_manager.tasks["tetris_game"].stop()

        self.destroy()



    def create_left_panel(self):
        # Panel izquierdo
        left_panel = ctk.CTkFrame(self, width=200)
        left_panel.pack(side=ctk.LEFT, fill=ctk.Y, padx=10, pady=10)
        # Secciones y botones
        sections = {
            "Aplicaciones": [
                ("Abrir Chrome", lambda: self.process_manager.open_resource("browser", "https://google.com", "Cannot open browser")),
                ("Visual Studio Code", lambda: self.process_manager.open_resource("program", r"C:\Program Files\Microsoft VS Code\Code.exe", "Can't find VSCode")),
                ("Explorador de Windows", lambda: self.process_manager.open_resource("program", "explorer.exe", "Can't open Windows Explorer")),
                ("Notepad++", lambda: self.process_manager.open_resource("program", r"C:\Program Files\Notepad++\notepad++.exe", "Can't open Notepad++"))
            ]
        }

        for section, buttons in sections.items():
            if section:
                section_label = ctk.CTkLabel(left_panel, text=section, font=("Arial", 12, "bold"))
                section_label.pack(anchor=ctk.W, pady=5, padx=10)

            for text, command in buttons:
                btn = ctk.CTkButton(left_panel, text=text, command=command, width=150)
                btn.pack(pady=5, padx=10)

        scrapping_label = ctk.CTkLabel(left_panel, text="Scrapping", font=("Arial", 12, "bold"))
        scrapping_label.pack(anchor=ctk.W, pady=5, padx=10)
        url_entry = ctk.CTkEntry(left_panel, placeholder_text="Introduce la URL")
        url_entry.pack(pady=5, padx=10)

        self.left_panel = left_panel
        self.left_panel.url_entry = url_entry
        start_button = ctk.CTkButton(left_panel, text="Iniciar Scrapping", command=lambda:
                                     self.thread_manager.tasks["scrapper"].start(self.thread_manager.scrapper.start_scraping))
        start_button.pack(pady=5, padx=10)

        stop_button = ctk.CTkButton(left_panel, text="Detener Scrapping", command=self.thread_manager.tasks["scrapper"].stop)
        stop_button.pack("pady=5, padx=10")



    def create_center_panel(self):
        # Panel central con pestañas
        center_panel = ctk.CTkFrame(self)
        center_panel.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=(10, 10), pady=10)

        tab_view = ctk.CTkTabview(center_panel, width=500, height=500)
        tab_view.pack(fill=ctk.BOTH, expand=True)

        # Crear pestañas y manejar contenido por separado
        for tab_name in ["Scrapping", "Navegador", "Correos", "Juego", "Sistema"]:
            tab = tab_view.add(tab_name)

            if tab_name == "Sistema":
                # Crear un frame para los gráficos del sistema  
                system_frame = ctk.CTkFrame(tab)  
                system_frame.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)  

                # Inicializar SystemMonitor con el frame de la pestaña  
                self.system_monitor = SystemMonitor(system_frame)  

                # Asignar el system_monitor al thread_manager  
                self.thread_manager.set_system_monitor(self.system_monitor)

            elif tab_name == "Juego":
                # Crear un marco intermedio para centrar
                game_frame = ctk.CTkFrame(tab)
                game_frame.pack(expand=True)

                # Botones para el juego
                button_frame = ctk.CTkFrame(game_frame)
                button_frame.pack(pady=10)

                start_button = ctk.CTkButton(button_frame, text="Start Game", command=self.start_tetris_game)
                start_button.pack(side=tk.LEFT, padx=5)

                pause_button = ctk.CTkButton(button_frame, text="Pause Game", command=self.pause_tetris_game)
                pause_button.pack(side=tk.LEFT, padx=5)

                restart_button = ctk.CTkButton(button_frame, text="Restart Game", command=self.restart_tetris_game)
                restart_button.pack(side=tk.LEFT, padx=5)

                # Agregar el Tetris dentro de un contenedor
                self.tetris_game = TetrisGame(game_frame)
                self.tetris_game.pack()

            else:
                # Agregar contenido genérico a otras pestañas
                label = ctk.CTkLabel(tab, text=f"Contenido de {tab_name}", font=("Arial", 12))
                label.pack(pady=10)



    def start_tetris_game(self):
        """Método para iniciar el juego."""
        if not self.tetris_game.running:
            self.tetris_game.running = True
            #self.tetris_game.update_game()



    def pause_tetris_game(self):
        """Método para pausar el juego."""
        self.tetris_game.running = False



    def restart_tetris_game(self):
        """Método para reiniciar el juego."""
        self.tetris_game.reset_game()



    def create_right_panel(self):
        # Panel derecho
        right_panel = ctk.CTkFrame(self, width=250)
        right_panel.pack(side=ctk.RIGHT, fill=ctk.Y, padx=10, pady=10)

        # Chat
        chat_label = ctk.CTkLabel(right_panel, text="Chat", font=("Arial", 14, "bold"), text_color="red")
        chat_label.pack(anchor=ctk.W, pady=5, padx=10)

        chat_box = ctk.CTkTextbox(right_panel, height=100)
        chat_box.pack(fill=ctk.X, padx=10, pady=5)

        send_button = ctk.CTkButton(right_panel, text="Enviar", command=self.dummy_action)
        send_button.pack(pady=5, padx=10)

        # Lista de alumnos
        for i in range(1, 4):
            student_label = ctk.CTkLabel(right_panel, text=f"Alumno {i}", font=("Arial", 12, "bold"), text_color="black")
            student_label.pack(anchor=ctk.W, pady=5, padx=10)

            student_info = ctk.CTkLabel(
                right_panel,
                text="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                wraplength=200,
                justify="left",
            )
            student_info.pack(anchor=ctk.W, padx=10)



    def create_bottom_bar(self):
        # Crear la barra inferior
        self.bottom_bar = ctk.CTkFrame(self, fg_color="lightblue", height=40)
        self.bottom_bar.pack(side=ctk.BOTTOM, fill=ctk.X, padx=0, pady=0)

        # Diccionario para las etiquetas dinámicas
        self.info_labels = {
            "hora": ctk.CTkLabel(self.bottom_bar, text="Hora: --:--:--", font=("Arial", 12), text_color="black"),
            "fecha": ctk.CTkLabel(self.bottom_bar, text="Fecha: --/--/----", font=("Arial", 12), text_color="black"),
            "temperatura": ctk.CTkLabel(self.bottom_bar, text="Temperatura local: --°C", font=("Arial", 12), text_color="black"),
            "emails": ctk.CTkLabel(self.bottom_bar, text="Correos sin leer: 0", font=("Arial", 12), text_color="black"),
        }

        # Empaquetar las etiquetas horizontalmente
        for label in self.info_labels.values():
            label.pack(side=ctk.LEFT, padx=10, pady=5)



    def dummy_action(self):
        print("Acción no implementada")