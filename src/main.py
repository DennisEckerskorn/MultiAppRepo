from ui.centered_window import CenteredWindow

def main():
    # Crear una instancia de la ventana centrada
    app = CenteredWindow(title="Ventana Principal", width_percentage=0.75, height_percentage=0.75)
    
    # Ejecutar la ventana
    app.mainloop()

if __name__ == "__main__":
    main()