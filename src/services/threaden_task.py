import threading

"""Clase que se encarga de manjear hilos. Permite arrancar y parar un hilo"""

class ThreadenTask:
    def __init__(self):
        self.running = False
        self.thread = None


    def start(self, target, *args):
        """Inicia un hilo con el objetivo especificado."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=target, args=args, daemon=True)
            self.thread.start()

    def stop(self):
        """Detiene el hilo"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None