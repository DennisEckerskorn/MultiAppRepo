import tkinter as tk
import random

class TetrisGame(tk.Canvas):
    def __init__(self, parent, width=300, height=600, cell_size=30):
        super().__init__(parent, width=width, height=height, bg="black")
        self.cell_size = cell_size
        self.cols = width // cell_size
        self.rows = height // cell_size
        self.grid = [[0] * self.cols for _ in range(self.rows)]

        self.current_piece = None
        self.running = True
        self.init_game()

    def init_game(self):
        self.bind_all("<Key>", self.handle_keypress)
        self.spawn_piece()
        self.update_game()

    def spawn_piece(self):
        shapes = [
            [[1, 1, 1], [0, 1, 0]],  # T-shape
            [[1, 1], [1, 1]],        # Square
            [[1, 1, 1, 1]],          # Line
            [[0, 1, 1], [1, 1, 0]],  # S-shape
            [[1, 1, 0], [0, 1, 1]],  # Z-shape
        ]
        shape = random.choice(shapes)
        self.current_piece = {
            "shape": shape,
            "row": 0,
            "col": (self.cols - len(shape[0])) // 2,
        }

    def draw_piece(self):
        shape = self.current_piece["shape"]
        row = self.current_piece["row"]
        col = self.current_piece["col"]
        for r, line in enumerate(shape):
            for c, block in enumerate(line):
                if block:
                    self.draw_cell(row + r, col + c, "cyan")

    def draw_cell(self, row, col, color):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def move_piece(self, drow, dcol):
        if self.can_move(drow, dcol):
            self.current_piece["row"] += drow
            self.current_piece["col"] += dcol

    def rotate_piece(self):
        """Rota la pieza actual en el sentido horario."""
        shape = self.current_piece["shape"]
        rotated_shape = list(zip(*shape[::-1]))  # Rotar la matriz en sentido horario

        # Verifica si la pieza rotada cabe en la posición actual
        if self.can_place(rotated_shape, self.current_piece["row"], self.current_piece["col"]):
            self.current_piece["shape"] = rotated_shape

    def can_place(self, shape, row, col):
        for r, line in enumerate(shape):
            for c, block in enumerate(line):
                if block:
                    if row + r >= self.rows or col + c < 0 or col + c >= self.cols:
                        return False  # Fuera de los límites del tablero
                    if self.grid[row + r][col + c]:
                        return False  # Choca con otro bloque
        return True

    def can_move(self, drow, dcol):
        shape = self.current_piece["shape"]
        row = self.current_piece["row"] + drow
        col = self.current_piece["col"] + dcol
        return self.can_place(shape, row, col)

    def place_piece(self):
        shape = self.current_piece["shape"]
        row = self.current_piece["row"]
        col = self.current_piece["col"]
        for r, line in enumerate(shape):
            for c, block in enumerate(line):
                if block:
                    self.grid[row + r][col + c] = 1
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        self.grid = [line for line in self.grid if any(cell == 0 for cell in line)]
        while len(self.grid) < self.rows:
            self.grid.insert(0, [0] * self.cols)

    def handle_keypress(self, event):
        if event.keysym == "Left":
            self.move_piece(0, -1)
        elif event.keysym == "Right":
            self.move_piece(0, 1)
        elif event.keysym == "Down":
            self.move_piece(1, 0)
        elif event.keysym == "Up":
            self.rotate_piece()

    def update_game(self):
        if self.running:
            if not self.can_move(1, 0):
                self.place_piece()
            else:
                self.move_piece(1, 0)
            self.render()
            self.after(500, self.update_game)

    def render(self):
        self.delete("all")
        for r, line in enumerate(self.grid):
            for c, block in enumerate(line):
                if block:
                    self.draw_cell(r, c, "blue")
        self.draw_piece()

    def stop_game(self):
        self.running = False

    def reset_game(self):
        """Reinicia el estado del juego."""
        self.running = False  # Detener el juego actual
        self.grid = [[0] * self.cols for _ in range(self.rows)]  # Reiniciar la cuadrícula
        self.current_piece = None  # Eliminar la pieza actual
        self.delete("all")  # Limpiar el lienzo
        self.spawn_piece()  # Generar una nueva pieza
        self.running = True  # Habilitar el juego nuevamente
        self.update_game()  # Reanudar el ciclo del juego
