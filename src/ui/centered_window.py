import customtkinter as ctk

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

        #Configura la ventana (fuera del constructor)
        self.configure_window()

    def configure_window(self):
        # Configuraciones adicionales:
        self.configure(bg_color="lightgray")
            # Ejemplo de añadir un botón
        btn = ctk.CTkButton(self, text="Haz clic aquí", command=self.on_button_click)
        btn.pack(pady=20)

    def on_button_click(self):
        print("¡Botón clickeado!")




