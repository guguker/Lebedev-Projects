# FINAL STABLE

import pygame
import sys
import os
import json
import TetrisAPI  # type: ignore

pygame.init()

"""работа с окнами чтобы было красиво"""
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000
GRID_WIDTH = 10
GRID_HEIGHT = 20 
GRID_MARGIN = 15
GRID_TOP_MARGIN = 30

""" размеры игрового поля """
FIELD_WIDTH = int(WINDOW_WIDTH * 0.6)
GRID_SIZE = FIELD_WIDTH // GRID_WIDTH

"""фигуры падают каждые 350 миллисекунд"""
FALL_SPEED = 350

""" превью-окошко справа """
NEXT_PIECES = 5   # количество следующих фигур для показа
game_field_right = GRID_MARGIN + GRID_WIDTH * GRID_SIZE
PREVIEW_BOX_WIDTH = WINDOW_WIDTH - game_field_right - 15 - 20  # высчитал 20px от правого края по красоте
PREVIEW_BOX_HEIGHT = 600
PREVIEW_BLOCK_SIZE = 25  # размер блока в превью следующих фигур
PREVIEW_SECTION_HEIGHT = PREVIEW_BOX_HEIGHT // NEXT_PIECES  # высота одной секции
PREVIEW_BOX_PADDING = 20  # отступ внутри превью

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BUTTON_BG = (230, 230, 230)
BUTTON_HOVER = (200, 200, 200)
MENU_BG = (240, 240, 240, 200)
DARK_ORANGE = (255, 140, 0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("TetRizz")

"""работа с фонами и вывод ошибки возможной"""
try:
    # основной фон
    background = pygame.image.load(os.path.join('images', 'bg.jpg'))
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # фон игрового поля
    game_bg = pygame.image.load(os.path.join('images', 'bg2.png'))
    field_width = (WINDOW_WIDTH // 2) - (GRID_MARGIN * 2)
    field_height = WINDOW_HEIGHT - (GRID_TOP_MARGIN + GRID_MARGIN)
    game_bg = pygame.transform.scale(game_bg, (field_width, field_height))
    
    # фон превью
    preview_bg = pygame.image.load(os.path.join('images', 'bg3.png'))
    
    # затемняем фоны
    for bg in [game_bg, preview_bg]:
        dark = pygame.Surface(bg.get_size(), flags=pygame.SRCALPHA)
        dark.fill((0, 0, 0, 128))
        bg.blit(dark, (0, 0))

except pygame.error as e:
    print(f"фон меняй, абас!!: {e}")
    background = None
    game_bg = None
    preview_bg = None

"""работа со шрифтом и вывод ошибки возможной"""
try:
    font = pygame.font.Font(os.path.join('fonts', 'font.ttf'), 48)
    menu_font = pygame.font.Font(os.path.join('fonts', 'font.ttf'), 36)
    score_font = pygame.font.Font(os.path.join('fonts', 'font.ttf'), 24)

except pygame.error:
    print("шрифт меняй, абас!!")
    font = pygame.font.Font(None, 48)
    menu_font = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 24)

"""кнопки и их классы с функциями"""
class Button:
    def __init__(self, text, color, font_obj, is_rounded=True, padding=(20, 10)):
        self.text = text
        self.color = color
        self.is_hovered = False
        self.is_rounded = is_rounded
        self.font = font_obj
        
        # поверхность текста
        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect()
        
        # высчитываем размеры кнопки на основе текста
        self.width = self.text_rect.width + (padding[0] * 2)
        self.height = self.text_rect.height + (padding[1] * 2)
        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.text_rect.center = self.rect.center

    def draw(self, surface):
        color = BUTTON_HOVER if self.is_hovered else self.color
        
        if self.is_rounded:
            radius = 10
            rect = self.rect
            pygame.draw.rect(surface, color, rect, border_radius=radius)
            pygame.draw.rect(surface, BLACK, rect, 2, border_radius=radius)

        else:
            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

""" работа с рекордами и их сохранение """
def load_high_score():
    try:
        with open('scores.json', 'r') as f:
            data = json.load(f)
            return data.get('high_score', 0)
        
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_high_score(score):
    try:
        with open('scores.json', 'w') as f:
            json.dump({'high_score': score}, f)

    except IOError as e:
        print(f"рекорд не сохраняется, абас!!: {e}")

""" отрисовка игрового поля и счета """
def draw_game_field(score, high_score):
    # размеры и позиция игрового поля
    field_width = GRID_SIZE * GRID_WIDTH
    field_height = GRID_SIZE * GRID_HEIGHT
    field_x = GRID_MARGIN
    field_y = GRID_TOP_MARGIN
    
    # рисуем фон поля
    if game_bg:
        scaled_bg = pygame.transform.scale(game_bg, (field_width, field_height))
        screen.blit(scaled_bg, (field_x, field_y))
    
    # рисуем сетку
    for x in range(GRID_WIDTH + 1):
        x_pos = field_x + (x * GRID_SIZE)
        pygame.draw.line(screen, GRAY, 
                        (x_pos, field_y),
                        (x_pos, field_y + field_height))
        
    for y in range(GRID_HEIGHT + 1):
        y_pos = field_y + (y * GRID_SIZE)
        pygame.draw.line(screen, GRAY,
                        (field_x, y_pos),
                        (field_x + field_width, y_pos))
    
    # отрисовка счета и рекорда
    score_text = score_font.render(f"score: {score}", True, BLACK)
    record_text = score_font.render(f"record: {high_score}", True, BLACK)
    
    screen.blit(score_text, (WINDOW_WIDTH - score_text.get_width() - 20, 
                            WINDOW_HEIGHT - record_text.get_height() * 2 - 30))
    screen.blit(record_text, (WINDOW_WIDTH - record_text.get_width() - 20, 
                             WINDOW_HEIGHT - record_text.get_height() - 10))

""" класс игры Tetris и ваще ВСЕЕЕЕ её функции"""
class TetrisGame:

    SHAPES = {
        'I': [(0,0), (0,-1), (0,1), (0,2)],  # вертикальная палка
        'J': [(0,0), (0,-1), (0,1), (-1,1)],  # J-фигура
        'L': [(0,0), (0,-1), (0,1), (1,1)],   # L-фигура
        'O': [(0,0), (1,0), (0,1), (1,1)],    # квадрат
        'S': [(0,0), (1,0), (-1,1), (0,1)],   # S-фигура
        'T': [(0,0), (-1,0), (1,0), (0,1)],   # T-фигура
        'Z': [(-1,0), (0,0), (0,1), (1,1)]    # Z-фигура
    }
    
    """повороты фигур кроме квадрата"""
    def get_rotated_shape(self, shape, rotation):
        rotated = []
        for x, y in shape:
            for _ in range(rotation % 4):
                x, y = -y, x  # Поворот на 90° против часовой стрелки
            rotated.append((x, y))
        return rotated
    
    """возвращает абсолютные координаты всех блоков фигуры"""
    def get_piece_blocks(self, piece_type, x, y, rotation=0):
        shape = self.SHAPES[piece_type]
        rotated = self.get_rotated_shape(shape, rotation)
        return [(x + dx, y + dy) for dx, dy in rotated]

    PIECE_TYPES = {
        0: 'I',
        1: 'O',
        2: 'T',
        3: 'S',
        4: 'Z',
        5: 'J',
        6: 'L'
    }

    """инициализация игры и всё что с ней"""
    def __init__(self):
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.piece_queue = []
        self.last_fall_time = pygame.time.get_ticks()
        self.score = 0
        self.game_over = False
        self.rotation = 0  # поле для отслеживания поворота
        self.generate_new_pieces()

    """генерирует новую последовательность фигур"""
    def generate_new_pieces(self):
        new_pieces = TetrisAPI.generate7bag(7)  # get 7 новых фигур

        new_pieces = [self.PIECE_TYPES[p] for p in new_pieces]
        self.piece_queue.extend(new_pieces)
        
        # если это первая генерация или очередь слишком короткая, создаем текущую фигуру
        if self.current_piece is None:
            self.spawn_new_piece()

    """работа со спавном фигуры"""
    def spawn_new_piece(self):
        if len(self.piece_queue) <= NEXT_PIECES:
            self.generate_new_pieces()
        
        self.current_piece = {
            'type': self.piece_queue.pop(0),
            'x': GRID_WIDTH // 2 - 1,
            'y': 0,
            'rotation': 0  # добавляем поворот к каждой фигуре
        }
        
        # проверка на game over - если новая фигура сразу сталкивается
        if not self.can_move(0, 0):
            self.game_over = True

    """проверяет, может ли фигура двигаться/вращаться (игнорирует by < 0 чтобы не рисовать фигуры за пределами экрана)"""
    def can_move(self, dx, dy, rotation=None):
        if not self.current_piece:
            return False
        x = self.current_piece['x'] + dx
        y = self.current_piece['y'] + dy
        rot = self.current_piece.get('rotation', 0) if rotation is None else rotation
        blocks = self.get_piece_blocks(self.current_piece['type'], x, y, rot)
        for bx, by in blocks:
            if bx < 0 or bx >= GRID_WIDTH:
                return False
            if by >= GRID_HEIGHT:
                return False
            if by >= 0 and self.board[by][bx] != 0:
                return False
        return True

    """фиксирует фигуру на поле (все блоки, только by >= 0)"""
    def lock_piece(self):
        if not self.current_piece:
            return
        x = self.current_piece['x']
        y = self.current_piece['y']
        rot = self.current_piece.get('rotation', 0)
        blocks = self.get_piece_blocks(self.current_piece['type'], x, y, rot)
        for bx, by in blocks:
            if bx < 0 or bx >= GRID_WIDTH:
                self.game_over = True
                return
            if by >= GRID_HEIGHT:
                self.game_over = True
                return
            if by >= 0:
                self.board[by][bx] = self.current_piece['type']
        self.check_lines()
        self.spawn_new_piece()

    """проверяет и удаляет заполненные линии"""
    def check_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1

        while y >= 0:
            if all(cell != 0 for cell in self.board[y]):
                self.board.pop(y)
                self.board.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1

            else:
                y -= 1
        
        # начисление очков
        if lines_cleared > 0:
            self.score += lines_cleared * 100

    def update(self):
        if self.game_over:
            return

        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_fall_time > FALL_SPEED:
            if self.can_move(0, 1):
                self.current_piece['y'] += 1
            else:
                self.lock_piece()
            self.last_fall_time = current_time

    """отрисовка следующих фигур справа"""
    def draw_preview(self, surface):
        preview_x = WINDOW_WIDTH - PREVIEW_BOX_WIDTH - 20
        preview_y = (WINDOW_HEIGHT - PREVIEW_BOX_HEIGHT) // 2  # центрируем по вертикали

        # заголовок превью (в стиле меню)
        next_text = Button("Дальше:", DARK_ORANGE, menu_font, is_rounded=False)
        next_text.set_position(preview_x, preview_y - next_text.height - 10)  # 10px отступ до бокса
        next_text.draw(surface)

        # рисуем фон и рамку превью
        preview_rect = pygame.Rect(preview_x, preview_y, PREVIEW_BOX_WIDTH, PREVIEW_BOX_HEIGHT)

        if preview_bg:
            scaled_bg = pygame.transform.scale(preview_bg, (PREVIEW_BOX_WIDTH, PREVIEW_BOX_HEIGHT))
            surface.blit(scaled_bg, preview_rect)

        else:
            pygame.draw.rect(surface, WHITE, preview_rect)
        pygame.draw.rect(surface, BLACK, preview_rect, 2)

        # рисуем разделительные линии для секций (красева :3)
        for i in range(1, NEXT_PIECES):
            y = preview_y + i * PREVIEW_SECTION_HEIGHT
            pygame.draw.line(surface, BLACK, 
                           (preview_x, y),
                           (preview_x + PREVIEW_BOX_WIDTH, y))

        # отрисовка самих фигур
        for i, piece_type in enumerate(self.piece_queue[:NEXT_PIECES]):
            piece_num = self.get_piece_number(piece_type)
            color = TetrisAPI.get_colors(piece_num)
            
            # вычисляем центр для каждой фигуры в своей секции (красева :3)
            center_x = preview_x + PREVIEW_BOX_WIDTH // 2
            section_center_y = preview_y + (i * PREVIEW_SECTION_HEIGHT) + (PREVIEW_SECTION_HEIGHT // 2)
            
            self.draw_piece_shape(surface, piece_type, center_x, section_center_y, PREVIEW_BLOCK_SIZE, color)

    """преобразует букву в номер фигуры для получения цвета"""
    def get_piece_number(self, piece_type):
        return list(self.PIECE_TYPES.keys())[list(self.PIECE_TYPES.values()).index(piece_type)]

    """отрисовка фигуры по её типу и координатам"""
    def draw_piece_shape(self, surface, piece_type, x, y, block_size, color):

        blocks = self.get_piece_blocks(piece_type, 0, 0)
        
        # вычисляем границы фигуры
        min_x = min(bx for bx, _ in blocks)
        max_x = max(bx for bx, _ in blocks)
        min_y = min(by for _, by in blocks)
        max_y = max(by for _, by in blocks)
        
        # вычисляем центр фигуры
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        for bx, by in blocks:
            # смещаем блоки относительно центра фигуры
            dx = bx - center_x
            dy = by - center_y
            
            # финальные координаты блока
            block_x = x + (dx * block_size)
            block_y = y + (dy * block_size)
            
            # создаем и отрисовываем блок
            rect = pygame.Rect(
                round(block_x - block_size/2),  # округляем для точного позиционирования
                round(block_y - block_size/2),
                block_size - 1,
                block_size - 1
            )
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

    """отрисовка игрового поля и текущей фигуры"""
    def draw(self, surface):

        # отрисовка зафиксированных фигур
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board[y][x] != 0:
                    piece_type = self.board[y][x]
                    piece_num = self.get_piece_number(piece_type)
                    color = TetrisAPI.get_colors(piece_num)
                    block_x = GRID_MARGIN + x * GRID_SIZE
                    block_y = GRID_TOP_MARGIN + y * GRID_SIZE
                    rect = pygame.Rect(block_x, block_y, GRID_SIZE - 1, GRID_SIZE - 1)
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, BLACK, rect, 1)

        # отрисовка текущей фигуры
        if self.current_piece and not self.game_over:
            piece_type = self.current_piece['type']
            piece_num = self.get_piece_number(piece_type)
            color = TetrisAPI.get_colors(piece_num)
            rotation = self.current_piece.get('rotation', 0)
            
            # получаем блоки текущей фигуры с учётом её позиции и поворота
            blocks = self.get_piece_blocks(piece_type, self.current_piece['x'], self.current_piece['y'], rotation)
            
            # отрисовка каждого блока фигуры
            for bx, by in blocks:
                if by >= 0:  # рисуем только видимые блоки
                    block_x = GRID_MARGIN + bx * GRID_SIZE
                    block_y = GRID_TOP_MARGIN + by * GRID_SIZE
                    rect = pygame.Rect(block_x, block_y, GRID_SIZE - 1, GRID_SIZE - 1)
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, BLACK, rect, 1)

"""класс меню паузы и его функции"""
class PauseMenu:
    def __init__(self):
        self.is_visible = False
        
        # кнопки меню
        self.resume_button = Button("продолжить игру (нада)", BUTTON_BG, menu_font)
        self.restart_button = Button("начать игру заново (норм идея)", BUTTON_BG, menu_font)
        self.exit_button = Button("выйти из игры (ненада)", BUTTON_BG, menu_font)
        
        self.menu_text = Button("Меню", DARK_ORANGE, menu_font, is_rounded=False)
        self.menu_button = Button("⋮", DARK_ORANGE, font, is_rounded=True, padding=(15, 5))
        
        # позиционка кнопок
        self.menu_button.set_position(WINDOW_WIDTH - 60, 20)
        self.menu_text.set_position(WINDOW_WIDTH - 230, 20)
        
        button_y = WINDOW_HEIGHT // 3
        self.resume_button.set_position(WINDOW_WIDTH // 2 - self.resume_button.width // 2, button_y)
        self.restart_button.set_position(WINDOW_WIDTH // 2 - self.restart_button.width // 2, 
                                      button_y + self.resume_button.height + 20)
        self.exit_button.set_position(WINDOW_WIDTH // 2 - self.exit_button.width // 2, 
                                    button_y + self.resume_button.height * 2 + 40)

    """обработка событий меню паузы"""
    def handle_events(self, event):
        if not self.is_visible and self.menu_button.handle_event(event):
            self.is_visible = True
            return "pause"
            
        if self.is_visible:
            if self.resume_button.handle_event(event):
                self.is_visible = False
                return "resume"
            elif self.restart_button.handle_event(event):
                self.is_visible = False
                return "restart"
            elif self.exit_button.handle_event(event):
                return "exit"
        return None

    """отрисовка меню паузы"""
    def draw(self, surface):

        self.menu_text.draw(surface)
        self.menu_button.draw(surface)
        
        if self.is_visible:
            # рисуем полупрозрачный фон
            s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(s, MENU_BG, s.get_rect())
            surface.blit(s, (0,0))
            
            # рисуем элементы меню
            self.resume_button.draw(surface)
            self.restart_button.draw(surface)
            self.exit_button.draw(surface)

"""главное меню"""
def main_menu():

    play_button = Button("play the game!", BUTTON_BG, font)
    play_button.set_position(WINDOW_WIDTH//2 - play_button.width//2, WINDOW_HEIGHT//2 - play_button.height//2)
    
    # заголовок
    title_button = Button("TetRizz", BUTTON_BG, font, is_rounded=False)
    title_button.set_position(WINDOW_WIDTH//2 - title_button.width//2, 300)  # сдвинули вниз
    
    while True:
        # отрисовка фона
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            play_button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and play_button.is_hovered:
                game_loop()
        
        title_button.draw(screen)
        play_button.draw(screen)
        
        pygame.display.flip()

"""основной игровой цикл"""
def game_loop():
    pause_menu = PauseMenu()
    game_paused = False
    high_score = load_high_score()
    game = TetrisGame()
    
    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(max(high_score, game.score))
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    save_high_score(max(high_score, game.score))
                    return  # возврат в мэйн меню
                
                elif not game_paused:
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        if game.can_move(-1, 0):
                            game.current_piece['x'] -= 1
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        if game.can_move(1, 0):
                            game.current_piece['x'] += 1
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        if game.can_move(0, 1):
                            game.current_piece['y'] += 1
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        # квадрату вертеться нельзя
                        if game.current_piece['type'] != 'O':
                            new_rotation = (game.current_piece['rotation'] + 1) % 4
                            if game.can_move(0, 0, new_rotation):
                                game.current_piece['rotation'] = new_rotation
            
            # события меню паузы
            menu_action = pause_menu.handle_events(event)
            if menu_action == "pause":
                game_paused = True

            elif menu_action == "resume":
                game_paused = False

            elif menu_action == "restart":

                if game.score > high_score:
                    save_high_score(game.score)

                game = TetrisGame()
                game_paused = False

            elif menu_action == "exit":
                save_high_score(max(high_score, game.score))
                pygame.quit()
                sys.exit()
        
        if not game_paused and not game.game_over:
            draw_game_field(game.score, high_score)
            game.update()
            game.draw(screen)
            game.draw_preview(screen)
            
            if game.score > high_score:
                high_score = game.score

        elif game.game_over:

            game_over_text = font.render("гейм овер нах!", True, BLACK)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        pause_menu.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()

