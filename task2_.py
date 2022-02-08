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

FILLED_POINTS = []

USER = 'X'
AI = 'O'


def ai_input():
    """
    Генерируем координаты для хода компьютера, проверяем свободна ли ячейка и проставляем маркер
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


def check_list(lst, symbol):
    """
    Принимаем и проверяем список на наличие проигрышной комбинации.
    Возвращаем False в случае её отсутствия
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


def check_draw():
    """
    Проверка игрового поля на ничью
    :return: булево значение True в случае Ничьи
    """
    if len(FILLED_POINTS) == 100:
        return True


def check_win(symbol, coordinate):
    """
    Принимаем параметры клика игрока и отправляем на проверку списки с горизонтальным, вертикальным и диагональными
    рядами на наличие проигрышной комбинации
    :return: параметры окончания игры или булево значение False если условия для окончания не выполнены
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
            return 'Ничья! Нажмите пробел для сброса'
    return False


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
    Сброс параметров и отрисовка нового игрового поля
    """
    global GAME_OVER, PLAY_BOARD
    PLAY_BOARD = [[0] * 10 for _ in range(10)]
    FILLED_POINTS.clear()
    GAME_OVER = False
    screen.fill(BLACK)


def graphic_render():
    """
    # Графическая отрисовка символов X и O
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
            x = col * width + (col + 1) * margin
            y = row * height + (row + 1) * margin
            pygame.draw.rect(screen, color, (x, y, width, height))
            if color == RED:
                pygame.draw.line(screen, WHITE, (x, y), (x + width, y + height), 2)
                pygame.draw.line(screen, WHITE, (x + width, y), (x, y + height), 2)
            elif color == GREEN:
                pygame.draw.circle(screen, WHITE, (x + width // 2, y + height // 2), width // 2, 2)


if __name__ == '__main__':
    # Генерируем игровую доску и задаём стартовые игровые параметры

    size = (510, 510)
    margin = 10
    width = height = 40
    size_window = (width, height)

    screen = pygame.display.set_mode(size)
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
                col = x_mouse // (margin + width)
                if col == X:
                    col -= 1
                row = y_mouse // (margin + height)
                if row == Y:
                    row -= 1
                coordinates = (row, col)
                if coordinates not in FILLED_POINTS:
                    PLAY_BOARD[row][col] = USER
                    FILLED_POINTS.append(coordinates)
                    player_game_over = check_win(USER, coordinates)
                    if player_game_over:
                        game_over(player_game_over)

                    ai_coordinates = ai_input()
                    ai_game_over = check_win(AI, ai_coordinates)
                    if ai_game_over:
                        game_over(ai_game_over)

            # Определение и обработка параметра сброса игры
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                new_game()
        # Графически отрисовываем символы X или O
        if not GAME_OVER:
            graphic_render()

        pygame.display.update()
