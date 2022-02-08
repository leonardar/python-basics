import sys
import pygame
import random

"""
Игра 'Обратные крестики-нолики'.
"""

RED = (199, 21, 133)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)

X = 10
Y = 10
PLAY_BOARD = [[0] * 10 for i in range(10)]
GAME_OVER = False

SIZE = (510, 510)
MARGIN = 10
WIDTH = HEIGHT = 40
size_window = (WIDTH, HEIGHT)

FILLED_POINTS = []

USER = 'X'
AI = 'O'


def ai_input():
    """
    Генерация координат для хода компьютера, проверка ячейки и установка маркера
    :return координаты выбранной ячейки
    """
    global PLAY_BOARD
    while True:
        x = random.randrange(X)
        y = random.randrange(Y)
        if (x, y) not in FILLED_POINTS:
            FILLED_POINTS.append((x, y))
            PLAY_BOARD[x][y] = AI
            return x, y


def get_diagonal1(x0, y0):
    """
    Определение первой диагонали от выбранной ячейки
    :param x0: строка выбранной ячейки
    :param y0: столбец выбранной ячейки
    :return: первую диагональ от выбранной ячейки
    """
    diagonal = []
    x = x0
    y = y0
    while 0 < x and 0 < y:
        x -= 1
        y -= 1
    while x < 10 and y < 10:
        diagonal.append(PLAY_BOARD[x][y])
        x += 1
        y += 1
    return diagonal


def get_diagonal2(x0, y0):
    """
    Определение второй диагонали от выбранной ячейки
    :param x0: строка выбранной ячейки
    :param y0: столбец выбранной ячейки
    :return: вторую диагональ от выбранной ячейки
    """
    diagonal = []
    x = x0
    y = y0
    while x < 10 - 1 and 0 < y:
        x += 1
        y -= 1
    while 0 <= x and y < 10:
        diagonal.append(PLAY_BOARD[x][y])
        x -= 1
        y += 1
    return diagonal


def check_losing(symbol, coordinate):
    """
    Обработка параметров клика игрока и отправление на проверку списков от выбранной ячейки с горизонтальным,
    вертикальным и диагональными рядами на наличие проигрышной комбинации :return: параметры окончания игры или
    булево значение False если условие для окончания игры не выполнено
    """
    if coordinate:
        x = coordinate[0]
        y = coordinate[1]

        vertical = [PLAY_BOARD[x][y] for y in range(10)]
        if check_list(vertical, symbol):
            return f'{symbol} проиграл. Нажмите пробел для новой игры'

        horizontal = [PLAY_BOARD[x][y] for x in range(10)]
        if check_list(horizontal, symbol):
            return f'{symbol} проиграл. Нажмите пробел для новой игры'

        diagonal_1 = get_diagonal1(x, y)
        if check_list(diagonal_1, symbol):
            return f'{symbol} проиграл. Нажмите пробел для новой игры'

        diagonal_2 = get_diagonal2(x, y)
        if check_list(diagonal_2, symbol):
            return f'{symbol} проиграл. Нажмите пробел для новой игры'

        if check_draw():
            return 'Ничья! Нажмите пробел для новой игры'
    return False


def check_list(lst, symbol):
    """
    Проверка списка на наличие проигрышной комбинации.
    :return: False в случае отсутствия проигрышной комбинации
    """
    sum = 0
    for item in lst:
        if item == symbol:
            sum += 1
            if sum >= 5:
                return True
        else:
            sum = 0
    return False


def check_draw():
    """
    Проверка игрового поля на ничью
    :return: булево значение True
    """
    if len(FILLED_POINTS) == 100:
        return True


def game_over(message):
    """
    Отрисовка окончания игры
    """
    global GAME_OVER
    GAME_OVER = True
    screen.fill(BLACK)
    font = pygame.font.SysFont('stxingkai', 30)
    text1 = font.render(message, True, WHITE)
    text_rect = text1.get_rect()
    text_x = screen.get_width() / 2 - text_rect.width / 2
    text_y = screen.get_height() / 2 - text_rect.height / 2
    screen.blit(text1, [text_x, text_y])


def new_game():
    """
    Сброс финальных параметров и отрисовка нового игрового поля
    """
    global GAME_OVER, PLAY_BOARD
    PLAY_BOARD = [[0] * 10 for _ in range(10)]
    FILLED_POINTS.clear()
    GAME_OVER = False
    screen.fill(BLACK)


def graphic_render():
    """
    Графическая отрисовка символов и ячеек X и O
    """
    global PLAY_BOARD
    for row in range(10):
        for col in range(10):
            if PLAY_BOARD[row][col] == USER:
                color = RED
            elif PLAY_BOARD[row][col] == AI:
                color = GREEN
            else:
                color = WHITE
            x = col * WIDTH + (col + 1) * MARGIN
            y = row * HEIGHT + (row + 1) * MARGIN
            pygame.draw.rect(screen, color, (x, y, WIDTH, HEIGHT))
            if color == RED:
                pygame.draw.line(screen, WHITE, (x, y), (x + WIDTH, y + HEIGHT), 2)
                pygame.draw.line(screen, WHITE, (x + WIDTH, y), (x, y + HEIGHT), 2)
            elif color == GREEN:
                pygame.draw.circle(screen, WHITE, (x + WIDTH // 2, y + HEIGHT // 2), WIDTH // 2, 2)


if __name__ == '__main__':
    # Генерация игровой доски и инициализация стартовых игровых параметров

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Обратные Крестики-Нолики")

    pygame.init()
    while True:
        coordinates = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # Обработка клика игрока и формирование кортежа с координатами
            elif event.type == pygame.MOUSEBUTTONDOWN and not GAME_OVER:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                col = x_mouse // (MARGIN + WIDTH)
                if col == X:
                    col -= 1
                row = y_mouse // (MARGIN + HEIGHT)
                if row == Y:
                    row -= 1
                coordinates = (row, col)
                if coordinates not in FILLED_POINTS:
                    PLAY_BOARD[row][col] = USER
                    FILLED_POINTS.append(coordinates)
                    # Проверка хода игрока на проигрышную комбинацию
                    player_game_over = check_losing(USER, coordinates)
                    if player_game_over:
                        game_over(player_game_over)

                    ai_coordinates = ai_input()
                    # Проверка хода компьютера на проигрышную комбинацию
                    ai_game_over = check_losing(AI, ai_coordinates)
                    if ai_game_over:
                        game_over(ai_game_over)

            # Определение и обработка параметра запуска новой игры
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                new_game()
        # Графическая отрисовка символов X или O
        if not GAME_OVER:
            graphic_render()

        pygame.display.update()
