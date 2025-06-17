import pygame
import random
import math
from queue import PriorityQueue

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 800
GRID_SIZE = 10  # Размер поля 10x10
CELL_SIZE = WIDTH // GRID_SIZE 
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A звиоздотька")

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Типы ячеек
EMPTY = 0
OBSTACLE = 1
START = 2
END = 3
PATH = 4
VISITED = 5

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.type = EMPTY
        
    def get_pos(self):
        return self.row, self.col
        
    def is_start(self):
        return self.type == START
        
    def is_end(self):
        return self.type == END
        
    def is_barrier(self):
        return self.type == OBSTACLE
        
    def is_visited(self):
        return self.type == VISITED
        
    def reset(self):
        self.color = WHITE
        self.type = EMPTY
        
    def make_start(self):
        self.color = ORANGE
        self.type = START
        
    def make_end(self):
        self.color = TURQUOISE
        self.type = END
        
    def make_barrier(self):
        self.color = BLACK
        self.type = OBSTACLE
        
    def make_visited(self):
        self.color = RED
        self.type = VISITED
        
    def make_path(self):
        self.color = PURPLE
        self.type = PATH
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        
    def update_neighbors(self, grid):
        self.neighbors = []
        
        # проверка соседа
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
            
        if self.row < GRID_SIZE - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
            
        if self.col < GRID_SIZE - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

def make_grid():
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            grid[i].append(cell)
    return grid

def draw_grid(win, grid):
    for row in grid:
        for cell in row:
            cell.draw(win)

    # Рисуем сетку
    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

    pygame.display.update()

def generate_random_grid(grid):
    # Очищаем сетку
    for row in grid:
        for cell in row:
            cell.reset()

    # Выбираем случайные начальную и конечную точки
    start_row, start_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    end_row, end_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)

    # Убедимся, что начальная и конечная точки разные
    while (start_row, start_col) == (end_row, end_col):
        end_row, end_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]

    start.make_start()
    end.make_end()

    # Добавляем случайные препятствия (35% ячеек)
    obstacle_count = int(GRID_SIZE * GRID_SIZE * 0.35)
    for _ in range(obstacle_count):
        row, col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        cell = grid[row][col]
        if not cell.is_start() and not cell.is_end():
            cell.make_barrier()

    return start, end

def h(p1, p2):
    """ Манхэттенское расстояние между двумя точками """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    """ Восстановление пути """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def a_star_algorithm(draw, grid, start, end):
    """ Реализация алгоритма A звиоздотька """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    # значения под каждую ячейку
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
            
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_visited()
        
        draw()
        
        if current != start:
            current.make_visited()
    
    return False

def create_predefined_map(grid):

    for row in grid:
        for cell in row:
            cell.reset()
    
    # начальная точка
    start = grid[9][0]
    start.make_start()
    
    # конечная точка
    end = grid[9][9]
    end.make_end()
    
    # препятствия
    obstacles = [
        (0, 3), (0, 9),
        (1, 1), (1, 3), (1, 5),
        (2, 1), (2, 3), (2, 5),
        (3, 2), (3, 7),
        (4, 8),
        (5, 3), (5, 4), (5, 6),
        (6, 1), (6, 2), (6, 4), (6, 5),
        (7, 2), (7, 5), (7, 6),
        (8, 3), (8, 6), (8, 9),
        (9, 2)
    ]
    
    for row, col in obstacles:
        grid[row][col].make_barrier()
        
    return start, end

# двухформатная main
def main():
    grid = make_grid()
    start = None
    end = None
    
    running = True
    started = False
    mode = None
    
    while running:
        draw_grid(WIN, grid)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and not started:  # кнопка 1 - предопределенная карта
                    start, end = create_predefined_map(grid)
                    mode = 1
                    
                elif event.key == pygame.K_2 and not started:  # кнопка 2 - случайная карта
                    start, end = generate_random_grid(grid)
                    mode = 2
                    
                elif event.key == pygame.K_SPACE and start and end:
                    started = True
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    a_star_algorithm(lambda: draw_grid(WIN, grid), grid, start, end)
                    
                elif event.key == pygame.K_r:  # сброс карты
                    started = False
                    if mode == 1:
                        start, end = create_predefined_map(grid)
                    elif mode == 2:
                        start, end = generate_random_grid(grid)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and mode == 2 and not started:
                # ручное размещение только в режиме 2
                pos = pygame.mouse.get_pos()
                row = pos[1] // CELL_SIZE
                col = pos[0] // CELL_SIZE
                cell = grid[row][col]
                
                if not start and cell != end:
                    start = cell
                    start.make_start()
                elif not end and cell != start:
                    end = cell
                    end.make_end()
                elif cell != end and cell != start:
                    cell.make_barrier()
    
    pygame.quit()

if __name__ == "__main__":
    main()
