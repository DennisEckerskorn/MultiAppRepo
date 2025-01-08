import vlc  
import time  
from src.services.threaden_task import ThreadenTask

class RadioPlayer:  
    def __init__(self):  
        self.player = vlc.MediaPlayer()  
        self.thread_task = ThreadenTask()  
        self.running = False  

    def play(self, url):  
        """Reproduce la emisora de radio desde la URL proporcionada."""  
        try:  
            if self.running:  
                self.stop()  
            self.thread_task.start(self.play_radio, url)  
            self.running = True  
        except Exception as e:  
            print(f"Error al reproducir la emisora: {e}")  

    def play_radio(self, url):  
        """Método interno para manejar la reproducción de la radio."""  
        try:  
            self.player.set_media(vlc.Media(url))  
            self.player.play()  
            while self.thread_task.running:  
                time.sleep(0.1)  
        except Exception as e:  
            print(f"Error en la reproducción de la radio: {e}")  

    def stop(self):  
        """Detiene la reproducción de la emisora de radio."""  
        try:  
            self.thread_task.stop()  
            self.player.stop()  
            self.running = False  
        except Exception as e:  
            print(f"Error al detener la reproducción: {e}")    