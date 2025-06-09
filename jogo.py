import pygame
import random
import sys
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fuja dos Obstáculos")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

PLAYER_SIZE = 30
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT_MIN = 50
OBSTACLE_HEIGHT_MAX = 150
OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_RATE = 1500
PLAYER_SPEED = 8

class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.color = BLUE
    
    def update(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Obstacle:
    def __init__(self):
        OBSTACLE_HEIGHT_FIXED = 80  
        OBSTACLE_WIDTH_FIXED = 80   
        
        y = random.randint(0, SCREEN_HEIGHT - OBSTACLE_HEIGHT_FIXED)
        self.rect = pygame.Rect(SCREEN_WIDTH, y, OBSTACLE_WIDTH_FIXED, OBSTACLE_HEIGHT_FIXED)
        self.color = RED
    
    def update(self):
        self.rect.x -= OBSTACLE_SPEED
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def is_off_screen(self):
        return self.rect.right < 0

class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.last_obstacle_time = 0
        self.start_time = time.time()
        self.game_over = False
        self.font = pygame.font.SysFont(None, 36)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.game_over and event.key == pygame.K_r:
                    self.__init__()
        return True
    
    def update(self):
        if self.game_over:
            return
        
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > OBSTACLE_SPAWN_RATE:
            self.obstacles.append(Obstacle())
            self.last_obstacle_time = current_time
        
        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
            
            if self.player.rect.colliderect(obstacle.rect):
                self.game_over = True
                self.survival_time = time.time() - self.start_time
    
    def draw(self):
        screen.fill(BLACK)
        
        self.player.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        if not self.game_over:
            current_time = time.time() - self.start_time
            time_text = self.font.render(f"Tempo: {current_time:.1f}s", True, WHITE)
            screen.blit(time_text, (10, 10))
        else:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            time_text = self.font.render(f"Você sobreviveu por {self.survival_time:.1f} segundos!", True, WHITE)
            restart_text = self.font.render("Pressione R para reiniciar", True, WHITE)
            
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()