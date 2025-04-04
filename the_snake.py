from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс"""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        """Конструктор"""
        self.position = position
        self.body_color = None

    def draw(self):
        """Базовый метод отрисовки"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, body_color=(255, 0, 0), position=None):
        """Конструктор"""
        super().__init__(self.randomize_position())
        self.body_color = body_color

    def randomize_position(self, snake_pos=[]):
        """Метод позиции"""
        offset = randint(0, 0)
        x_axis = [x for x in range(offset, SCREEN_WIDTH, GRID_SIZE)]
        y_axis = [y for y in range(offset, SCREEN_HEIGHT, GRID_SIZE)]
        possible_pos = [(x, y) for x in x_axis for y in y_axis]
        possible_pos = [pos for pos in possible_pos if pos not in snake_pos]
        return choice(possible_pos)

    def draw(self):
        """Метод отрисовки"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи"""

    def __init__(self, body_color=(0, 255, 0)):
        """Конструктор"""
        self.position = None
        self.length = 2
        self.positions = [self.randomize_position()]
        self.direction = (1, 0)  # Движение вправо
        self.next_direction = None
        self.body_color = body_color  # Зеленый цвет
        self.last = None

    def randomize_position(self):
        """Метод позиции"""
        return (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Центр экрана

    def update_direction(self):
        """Метод изменения направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения"""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * GRID_SIZE, head_y + dir_y * GRID_SIZE)

        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])

        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        if new_head in self.positions:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод отрисовки"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод получения позиции головы"""
        return self.positions[0]

    def reset(self):
        """Метод сброс к началу игры"""
        self.length = 2
        self.positions = [self.positions[0]]
        self.last = None


def handle_keys(game_object):
    """Метод обработки нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главный цикл программы"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
