from ui.centered_window import CenteredWindow

def main():
    try:
        app = CenteredWindow()
        app.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()

    #self.tasks["scrapper"].start(self.scrapper.start_scraping)