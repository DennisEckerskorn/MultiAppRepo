import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import tkinter as tk
import time

class SystemMonitor:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.max_data_points = 60
        self.running = True  # Indicador para detener los hilos
        self.metrics = {
            "CPU Usage": {
                "data": [],
                "thread": None,
                "fetch_func": psutil.cpu_percent,
                "interval": 1
            },
            "RAM Usage": {
                "data": [],
                "thread": None,
                "fetch_func": lambda: psutil.virtual_memory().percent,
                "interval": 1
            }
        }
        self.graphs = {}
        self.init_graphs()

    def init_graphs(self):
        """Crea gráficos para todas las métricas y arranca sus hilos de actualización."""
        for metric, config in self.metrics.items():
            fig, ax, line = self.create_graph(metric)
            self.graphs[metric] = {"figure": fig, "axis": ax, "line": line}

            # Crear y arrancar el hilo para actualizar esta métrica
            thread = threading.Thread(target=self.update_metric, args=(metric,), daemon=True)
            self.metrics[metric]["thread"] = thread
            thread.start()

    def create_graph(self, title):
        """Crea un gráfico para una métrica específica."""
        frame = tk.Frame(self.parent_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        label = tk.Label(frame, text=title, font=("Arial", 14, "bold"))
        label.pack()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel("Usage (%)")
        ax.set_ylim(0, 100)
        line, = ax.plot([], [], lw=2)

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        return fig, ax, line

    def update_metric(self, metric):
        config = self.metrics[metric]
        while self.running:
            try:
                new_data = config["fetch_func"]()
                config["data"].append(new_data)

                if len(config["data"]) > self.max_data_points:
                    config["data"].pop(0)

                self.update_graph(metric, config["data"])
                time.sleep(config["interval"])
            except Exception as e:
                print(f"Error en update_metric ({metric}): {e}")



    def update_graph(self, metric, data):
        """Actualiza un gráfico con nuevos datos."""
        graph = self.graphs[metric]
        x = list(range(len(data)))
        graph["line"].set_data(x, data)
        graph["axis"].set_xlim(0, len(data))
        graph["figure"].canvas.draw()

    def stop_threads(self):
        """Detiene la ejecución de todos los hilos de monitoreo."""
        self.running = False
