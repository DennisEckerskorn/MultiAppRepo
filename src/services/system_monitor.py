import psutil  
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import tkinter as tk  


class SystemMonitor:  
    def __init__(self, parent_frame):  
        self.parent_frame = parent_frame  
        self.max_data_points = 60  
        self.running = False
        self.previous_net_io = psutil.net_io_counters()
        self.metrics = {  
            "CPU Usage": {  
                "data": [],  
                "fetch_func": psutil.cpu_percent,  
                "interval": 1  
            },  
            "RAM Usage": {  
                "data": [],  
                "fetch_func": lambda: psutil.virtual_memory().percent,  
                "interval": 1  
            },
            "Network Usage (KB/s)": {
                "data": [],
                "fetch_func": self.get_network_usage,
                "interval": 1
            }
        }  
        self.graphs = {}  
        self.init_graphs()  

    def init_graphs(self):  
        """Crea gráficos para todas las métricas."""  
        for metric, config in self.metrics.items():  
            fig, ax, line = self.create_graph(metric)  
            self.graphs[metric] = {"figure": fig, "axis": ax, "line": line}  

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
        """Actualiza los datos de una métrica específica."""  
        config = self.metrics[metric]  
        try:  
            new_data = config["fetch_func"]()  
            config["data"].append(new_data)  

            if len(config["data"]) > self.max_data_points:  
                config["data"].pop(0)  

            self.update_graph(metric, config["data"])  
        except Exception as e:  
            print(f"Error en update_metric ({metric}): {e}")  

    def update_graph(self, metric, data):  
        """Actualiza un gráfico con nuevos datos."""  
        graph = self.graphs[metric]  
        x = list(range(len(data)))  

        def redraw():  
            graph["line"].set_data(x, data)  
            graph["axis"].set_xlim(0, len(data))
            graph["axis"].set_ylim(0, max(data) * 1.2 if data else 100) 
            graph["figure"].canvas.draw()  

        self.parent_frame.after(0, redraw)  

    def get_network_usage(self):  
        """Calcula la velocidad de transferencia de red en KB/s."""  
        current_net_io = psutil.net_io_counters()  
        sent_bytes = current_net_io.bytes_sent - self.previous_net_io.bytes_sent  
        recv_bytes = current_net_io.bytes_recv - self.previous_net_io.bytes_recv  
        self.previous_net_io = current_net_io  # Actualiza los datos previos  

        # Convierte a KB/s  
        total_kb = (sent_bytes + recv_bytes) / 1024
        print(f"Network Usage: {total_kb} KB/s")
        return total_kb 