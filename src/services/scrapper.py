import threading
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import mysql.connector

class Scrapper:
    def __init__(self, ui_instance):
        self.ui_instance = ui_instance
        self.visited_links = set()
        self.running=False
        self.lock() = threading.Lock()


    #Configurar la base de datos para los enlaces
    self.db.config = {
        "host": "localhost",
        "user": "root",
        "password": "1234Scrap",
        "database": "scrap_links_db"
    }

    def start_scraping(self):
        """Inicia el proceso de scraping"""
        self.running = True
        url = self.get_url_from_ui()
        if url:
            self.scrape_page(url)

    def stop_scraping(self):
        """Detiene el proceso de scraping"""
        self.running = False

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
                self.save_links_to_db(url, links)

                for link in links:
                    if self.running:
                        threading.Thread(target=self.scrape_page, args=(link,), daemon=True).start()
            else:
                print(f"Error al acceder a {url}: {response.status_code}")
        except Exception as e:
            print(f"Error al scrapear {url}: {e}")

    def update_ui(self, url, links):
        """Actualiza la pestaña 'Scrapping' con los enlaces encontrados"""
        tab = self.ui_instance.tabs["Scrapping"]
        text_widget = tab.text_widget
        text_widget.insert("end", f"Enlaces encontrados en {url}:\n")
        for link in links:
            text_widget.insert("end", f" - {link}\n")
            text_widget.insert("end", "\n")
            text_widget.see("end")

    def save_links_to_db(self, url, links)
        """Guarda los enlaces en la base de datos"""
        try:
            connection = mysql.connector(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS links (id INT AUTO_INCREMENT PRIMARY KEY, url TEXT, parent_url TEXT)")
            for link in links:
                cursor.execute("INSERT INTO links (url, parent_url) VALUES (%s, %s)", (link, url))
                connection.commit()
                cursor.close()
        except:
            print(f"Error al gaurdar en la base de datos")

    def get_url_from_ui(self):
        """Obtiene la URL desde la interfaz de usuario"""
        try:
            url_entry = self.ui_instance.left_panel.url_entry
            return url_entry.get()
        except AttributeError:
            print("No se pudo obtener la URL desde la interfaz")
            return None
    