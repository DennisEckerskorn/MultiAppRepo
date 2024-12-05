import subprocess
import webbrowser

class ProcessManager:
    def open_resource(self, resource_type, path_or_url, fallback_message="Resource not found"):
        """
        Método genérico para abrir programas, archivos o URLs.

        Args:
            resource_type (str): Tipo de recurso ("program" para programas/archivos o "browser" para URLs).
            path_or_url (str): Ruta del programa/archivo o URL a abrir.
            fallback_message (str): Mensaje a mostrar en caso de error. Por defecto, "Resource not found".
        """
        try:
            if resource_type == "program":
                subprocess.Popen([path_or_url])  # Abre un programa o archivo
            elif resource_type == "browser":
                webbrowser.get('chrome').open(path_or_url)  # Intenta abrir con Chrome
            else:
                print("Unknown resource type")
        except FileNotFoundError:
            print(fallback_message)
        except Exception as e:
            if resource_type == "browser":
                # Fallback al navegador por defecto si Chrome falla
                webbrowser.open(path_or_url)
            else:
                print(f"Error: {e}")
