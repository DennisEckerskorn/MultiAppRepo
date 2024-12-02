import customtkinter as ctk
import webbrowser
import subprocess
import os

class CenteredWindow(ctk.CTk):
    def __init__(self, title="MultiApp", width_percentage=0.8, height_percentage=0.8):
        # Inicializacion de la clase:
        super().__init__()

        # Titulo de la ventana:
        self.title(title)

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

    def configure_window(self):
        # Configuracion de la ventana:
        self.configure(bg_color="lightgray")

        self.create_menuBar()

        # Frame para organizar los botones:
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side=ctk.TOP, anchor=ctk.NW, padx=20, pady=20)

        buttons = [
            ("Abrir Google Chrome", self.open_chrome),
            ("Abrir Visual Studio Code", self.open_visual_studio_code),
            ("Abrir Explorador", self.open_explorer),
            ("Abrir NotePad++", self.open_notepad_plus)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10, padx=20)



    def create_menuBar(self):
        menu_bar = ctk.CTkFrame(self, height=25, fg_color="lightgray")
        menu_bar.pack(side=ctk.TOP, fill=ctk.X)

        #Botones del menuBar:
        # Agregar botones de menú
        menus = ["Procesos", "T2.Threads", "T3.Sockets", "T4.Servicios", "T5.Seguridad", "Configuración"]
        for menu in menus:
            btn = ctk.CTkButton(
                menu_bar,
                text=menu,
                command=lambda m=menu: self.on_menu_click(m),
                width=100,
                height=20,
                fg_color="blue",
                hover_color="lightblue"
            )
            btn.pack(side=ctk.LEFT, padx=5, pady=5)

    def open_chrome(self):
        try:
            webbrowser.get('chrome').open('https://google.es')
        except:
            webbrowser.open('https://google.es')


    def open_visual_studio_code(self):
        try:
            vs_code_path = r"C:\Program Files\Microsoft VS Code\Code.exe"
            subprocess.Popen([vs_code_path])
        except FileNotFoundError:
            print ("Can't find VSCode")


    def open_explorer(self):
        try:
            subprocess.Popen(['explorer.exe'])
        except:
            print("Can't open Windows Explorer")


    def open_notepad_plus(self):
        try:
            notepad_path = r"C:\Program Files\Notepad++\notepad++.exe"
            subprocess.Popen([notepad_path])
        except:
            print("Can't open NotePad++")



    def on_menu_click(self, menu_name):
        self.text_area.insert(ctk.END, f"Menú seleccionado: {menu_name}\n")




