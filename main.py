import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Шрифт для текста
font = pygame.font.SysFont(None, 55)

# Класс для игрока
class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))

# Класс для препятствий
class Obstacle:
    def __init__(self, speed):
        self.width = 50
        self.height = 50
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

    def check_collision(self, player):
        return player.x < self.x + self.width and player.x + player.width > self.x and player.y < self.y + self.height and player.y + player.height > self.y

# Класс для управления игрой
class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.level_up_threshold = 10
        self.obstacle_timer = 0
        self.obstacle_speed = 5  # Начальная скорость препятствий

    def add_obstacle(self):
        if self.obstacle_timer > 50:
            self.obstacles.append(Obstacle(self.obstacle_speed))  # Передаем текущую скорость препятствия
            self.obstacle_timer = 0
        else:
            self.obstacle_timer += 1

    def update_obstacles(self):
        for obstacle in self.obstacles[:]:
            obstacle.move()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 1  # Очки за пройденное препятствие

    def check_collisions(self):
        for obstacle in self.obstacles:
            if obstacle.check_collision(self.player):
                return True  # Столкновение произошло
        return False

    def level_up(self):
        if self.score >= self.level * self.level_up_threshold:
            self.level += 1
            self.obstacle_speed += 1  # Увеличиваем скорость препятствий с каждым уровнем

    def draw(self):
        score_text = font.render(f"Очки: {self.score}", True, WHITE)
        level_text = font.render(f"Уровень: {self.level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

def show_game_over():
    screen.fill(BLACK)
    game_over_text = font.render("Игра окончена!", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

    # Вопрос о продолжении
    continue_text = font.render("Хотите продолжить? (Y/N)", True, WHITE)
    screen.blit(continue_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Игрок выбирает продолжить
                    waiting_for_input = False
                    return True
                if event.key == pygame.K_n:  # Игрок выбирает завершить
                    waiting_for_input = False
                    return False

# Основной игровой цикл
def main():
    game = Game()
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление игроком
        keys = pygame.key.get_pressed()
        game.player.move(keys)

        # Обновление препятствий и проверка на столкновение
        game.add_obstacle()
        game.update_obstacles()

        if game.check_collisions():
            if not show_game_over():  # Спрашиваем игрока, хочет ли он продолжить
                running = False
            else:
                main()  # Если игрок выбрал продолжить, начинаем игру заново
                return

        # Повышение уровня
        game.level_up()

        # Отрисовка объектов
        game.player.draw(screen)
        for obstacle in game.obstacles:
            obstacle.draw(screen)

        game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Запуск игры
main()
