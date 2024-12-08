import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import mysql.connector
from queue import Queue

#http://books.toscrape.com/ test scrap web

class Scrapper:
    def __init__(self, ui_instance):
        self.ui_instance = ui_instance
        self.visited_links = set()
        self.running=False
        self.lock = threading.Lock()
        self.link_queue = Queue()

        #Configurar la base de datos para los enlaces
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "scrap_links_db",
            "port": 3306
        }

        try:
            connection = mysql.connector.connect(**self.db_config)
            print("Conexion exitosa a base de datos")
            connection.close()
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    def start_scraping(self):
        """Inicia el proceso de scraping"""
        self.running = True
        url = self.get_url_from_ui()
        if url:  
            print(f"Iniciando scraping en: {url}")
            threading.Thread(target=self.scrape_page, args=(url,), daemon=True).start()
            threading.Thread(target=self.insert_links_to_db, daemon=True).start()
        else:  
            print("No se proporcionó una URL válida.")  
            
    def stop_scraping(self):
        """Detiene el proceso de scraping"""
        self.running = False
        print("Scrapping detenido. Proceso finalizado.")

        #Vaciar la cola para detener el hilo de inserción
        while not self.link_queue.empty():
            self.link_queue.get()

        # Actualiza la pestaña "Scrapping" con un mensaje  
        tab = self.ui_instance.tabs["Scrapping"]  
        text_widget = tab["text_widget"]  

        text_widget.configure(state="normal")  
        text_widget.insert("end", "Scrapping finalizado.\n")  
        text_widget.see("end")  
        text_widget.configure(state="disabled")

    def scrape_page(self, url):
        """Scrapea una web y busca los enlaces"""
        if not self.running or url in self.visited_links:
            return
        
        with self.lock:
            self.visited_links.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]
                self.update_ui(url, links)

                for link in links:
                    if not self.running:
                        break
                    self.link_queue.put((url, link))

                for link in links:
                    if not self.running:
                        break
                    threading.Thread(target=self.scrape_page, args=(link,), daemon=True).start()
            else:
                print(f"Error al acceder a {url}: {response.status_code}")
        except Exception as e:
            print(f"Error al scrapear {url}: {e}")

    def update_ui(self, url, links):  
        """Actualiza la pestaña 'Scrapping' con los enlaces encontrados"""  
        tab = self.ui_instance.tabs["Scrapping"]  
        text_widget = tab["text_widget"]  

        text_widget.configure(state="normal")  
        text_widget.insert("end", f"Enlaces encontrados en {url}:\n")  
        for link in links:  
            text_widget.insert("end", f" - {link}\n")  
        text_widget.see("end")  
        text_widget.configure(state="disabled")



    def insert_links_to_db(self):  
        """Inserta los enlaces en la base de datos desde la cola"""  
        while self.running or not self.link_queue.empty():  
            try:  
            # Obtener un enlace de la cola  
                if not self.running and self.link_queue.empty():
                    break
                parent_url, link = self.link_queue.get(timeout=1)  # Espera 1 segundo si la cola está vacía  
                connection = mysql.connector.connect(**self.db_config)  
                cursor = connection.cursor()  
                cursor.execute("CREATE TABLE IF NOT EXISTS links (id INT AUTO_INCREMENT PRIMARY KEY, url TEXT, parent_url TEXT)")  
                cursor.execute("INSERT INTO links (url, parent_url) VALUES (%s, %s)", (link, parent_url))  
                connection.commit()  
                cursor.close()  
                connection.close()  
                print(f"Enlace guardado: {link} (parent: {parent_url})")  
            except Exception as e:  
                print(f"Error al guardar en la base de datos: {e}")  


    def get_url_from_ui(self):  
        """Obtiene la URL desde la interfaz de usuario"""  
        try:  
            url_entry = self.ui_instance.left_panel.url_entry  
            return url_entry.get()  
        except AttributeError:  
            print("No se pudo obtener la URL desde la interfaz")  
            return None  
"""
    def save_links_to_db(self, url, links):
        Guarda los enlaces en la base de datos
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS links (id INT AUTO_INCREMENT PRIMARY KEY, url TEXT, parent_url TEXT)")
            
            for link in links:
                print(f"Guardando enlace: {link} (parent: {url})")  # Verifica los datos  
                cursor.execute("INSERT INTO links (url, parent_url) VALUES (%s, %s)", (link, url))

            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error al gaurdar en la base de datos: {e}")
"""
    
    