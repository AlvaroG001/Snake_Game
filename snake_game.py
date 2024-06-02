import pygame
from pygame.locals import *
from random import randint

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.rows, self.columns = 20, 20
        self.block_size = 20
        self.width = self.columns * self.block_size
        self.height = self.rows * self.block_size
        self.snake = [(self.rows//2, self.columns//2)]
        self.food = self.generate_food()
        self.direction = "right"
        self.score = 0
        self.font = pygame.font.Font(None, 30)
        self.boundaries = self.generate_boundaries()
        self.snake_color = self.generate_random_color()
        self.food_color = self.generate_random_color()
        self.background_color = self.generate_random_color()

        self.game_name = "Snake Game"

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def generate_random_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    def generate_food(self):
        while True:
            row = randint(0, self.rows-1)
            col = randint(0, self.columns-1)
            if (row, col) not in self.snake and not self.is_boundary(row, col):
                return (row, col)

    def generate_boundaries(self):
        boundaries = []
        for row in range(self.rows):
            if row == 0 or row == self.rows - 1:
                for col in range(self.columns):
                    boundaries.append((row, col))
            else:
                boundaries.append((row, 0))
                boundaries.append((row, self.columns - 1))
        return boundaries

    def is_boundary(self, row, col):
        return (
            row == 0 or
            row == self.rows - 1 or
            col == 0 or
            col == self.columns - 1
        )

    def draw(self, surface):
        self.screen.fill(self.background_color)
        surface.fill((0, 0, 0))
        for row in range(self.rows):
            for col in range(self.columns):
                if self.is_boundary(row, col):
                    pygame.draw.rect(surface, (255, 255, 255), (col*self.block_size, row*self.block_size, self.block_size, self.block_size))
                elif (row, col) in self.snake:
                    pygame.draw.rect(surface, self.snake_color, (col*self.block_size, row*self.block_size, self.block_size, self.block_size))
                elif (row, col) == self.food:
                    pygame.draw.rect(surface, self.food_color, (col*self.block_size, row*self.block_size, self.block_size, self.block_size))
        
        score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        surface.blit(score_text, (20, 20))
        pygame.display.flip()

    def move(self):
        head_row, head_col = self.snake[0]
        if self.direction == "up":
            new_head = (head_row - 1, head_col)
        elif self.direction == "down":
            new_head = (head_row + 1, head_col)
        elif self.direction == "left":
            new_head = (head_row, head_col - 1)
        elif self.direction == "right":
            new_head = (head_row, head_col + 1)

        if (
            new_head[0] == 0 or
            new_head[0] == self.rows - 1 or
            new_head[1] == 0 or
            new_head[1] == self.columns - 1 or
            new_head in self.snake
        ):
            return False

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
            self.boundaries = self.generate_boundaries()
            self.snake_color = self.generate_random_color()
            self.food_color = self.generate_random_color()
            self.background_color = self.generate_random_color()
        else:
            self.snake.pop()

        return True

    def draw_game_name(self):
        game_name_text = self.font.render(self.game_name, True, (255, 255, 255))
        game_name_rect = game_name_text.get_rect()
        game_name_rect.center = (self.width // 2, self.height // 4)
        self.screen.blit(game_name_text, game_name_rect)

    def draw_start_screen(self):
        self.screen.fill((0, 0, 0))
        self.draw_game_name()
        start_text = self.font.render("Start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect()
        start_text_rect.center = (self.width // 2, self.height // 2)
        self.screen.blit(start_text, start_text_rect)
        pygame.display.flip()

    def new_game(self):
        self.snake = [(self.rows//2, self.columns//2)]
        self.food = self.generate_food()
        self.direction = "right"
        self.score = 0
        self.boundaries = self.generate_boundaries()
        self.snake_color = self.generate_random_color()
        self.food_color = self.generate_random_color()
        self.background_color = self.generate_random_color()

    def play_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_UP and self.direction != "down":
                        self.direction = "up"
                    elif event.key == K_DOWN and self.direction != "up":
                        self.direction = "down"
                    elif event.key == K_LEFT and self.direction != "right":
                        self.direction = "left"
                    elif event.key == K_RIGHT and self.direction != "left":
                        self.direction = "right"

            if self.snake[0] == self.food:
                self.score += 1
                self.snake.append(self.snake[-1])
                self.food = self.generate_food()
                self.snake_color = self.generate_random_color()
                self.food_color = self.generate_random_color()
                self.background_color = self.generate_random_color()

            if not self.move():
                self.draw_start_screen()
                break

            self.draw(self.screen)
            self.clock.tick(10)

    def start(self):
        pygame.init()
        self.draw_start_screen()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    start_text_rect = self.font.render("Start", True, (255, 255, 255)).get_rect()
                    start_text_rect.center = (self.width // 2, self.height // 2)
                    if start_text_rect.collidepoint(mouse_pos):
                        self.new_game()
                        self.play_game()

if __name__ == "__main__":
    game = SnakeGame()
    game.start()
