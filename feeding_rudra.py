import pygame
import time
import random
import math

# Game settings
initial_snake_speed = 8
speed_increment = 0.5
max_speed = 20

# Window size - smaller like Google Snake for more challenge
window_x = 600
window_y = 400
grid_size = 20  # Larger grid for better visibility

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(220, 20, 60)
green = pygame.Color(50, 205, 50)
blue = pygame.Color(30, 144, 255)
yellow = pygame.Color(255, 215, 0)
grey = pygame.Color(70, 70, 70)
dark_green = pygame.Color(34, 139, 34)
orange = pygame.Color(255, 165, 0)
purple = pygame.Color(147, 112, 219)

# Initialize pygame
pygame.init()

# Initialize game window
pygame.display.set_caption('Feeding Rudra')
game_window = pygame.display.set_mode((window_x, window_y), pygame.RESIZABLE)

# FPS controller
fps = pygame.time.Clock()

# Font setup
title_font = pygame.font.Font(None, 28)
score_font = pygame.font.Font(None, 24)
game_over_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 20)

class SnakeGame:
    def __init__(self):
        self.fullscreen = False
        self.reset_game()
        
    def toggle_fullscreen(self):
        global game_window, window_x, window_y
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            # Get monitor size and switch to fullscreen
            info = pygame.display.Info()
            window_x = info.current_w
            window_y = info.current_h
            game_window = pygame.display.set_mode((window_x, window_y), pygame.FULLSCREEN)
        else:
            # Back to windowed mode
            window_x = 600
            window_y = 400
            game_window = pygame.display.set_mode((window_x, window_y), pygame.RESIZABLE)
        
    def reset_game(self):
        # Snake setup
        start_x = (window_x // grid_size // 2) * grid_size
        start_y = (window_y // grid_size // 2) * grid_size
        
        self.snake_position = [start_x, start_y]
        self.snake_body = [
            [start_x, start_y],
            [start_x - grid_size, start_y],
            [start_x - 2*grid_size, start_y]
        ]
        
        # Game state
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.fruits_eaten = 0
        self.current_speed = initial_snake_speed
        
        # Fruit setup
        self.spawn_fruit()
        
    def spawn_fruit(self):
        while True:
            self.fruit_position = [
                random.randrange(0, window_x//grid_size) * grid_size,
                random.randrange(0, window_y//grid_size) * grid_size
            ]
            # Make sure fruit doesn't spawn on snake
            if self.fruit_position not in self.snake_body:
                break
    
    def get_fruit_points(self):
        # Simple scoring: 5 points per fruit
        return 5
    
    def update_speed(self):
        # Increase speed every 3 fruits
        if self.fruits_eaten % 3 == 0 and self.fruits_eaten > 0:
            self.current_speed = min(max_speed, self.current_speed + speed_increment)
    
    def handle_input(self):
        global window_x, window_y, game_window
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.VIDEORESIZE and not self.fullscreen:
                # Handle window resize
                window_x, window_y = event.size
                game_window = pygame.display.set_mode((window_x, window_y), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.change_to = 'UP'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.change_to = 'DOWN'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.change_to = 'RIGHT'
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen with F11
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE and self.fullscreen:
                    # Exit fullscreen with ESC
                    self.toggle_fullscreen()
        
        # Prevent reverse direction
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
            
        return True
    
    def move_snake(self):
        if self.direction == 'UP':
            self.snake_position[1] -= grid_size
        elif self.direction == 'DOWN':
            self.snake_position[1] += grid_size
        elif self.direction == 'LEFT':
            self.snake_position[0] -= grid_size
        elif self.direction == 'RIGHT':
            self.snake_position[0] += grid_size
    
    def check_collisions(self):
        # Wall collision
        if (self.snake_position[0] < 0 or self.snake_position[0] >= window_x or
            self.snake_position[1] < 0 or self.snake_position[1] >= window_y):
            return True
        
        # Self collision
        for block in self.snake_body[1:]:
            if self.snake_position == block:
                return True
                
        return False
    
    def update_game(self):
        # Add new head
        self.snake_body.insert(0, list(self.snake_position))
        
        # Check if fruit eaten
        if self.snake_position == self.fruit_position:
            points = self.get_fruit_points()
            self.score += points
            self.fruits_eaten += 1
            self.update_speed()
            self.spawn_fruit()
        else:
            # Remove tail if no fruit eaten
            self.snake_body.pop()
    
    def draw_game(self):
        # Fill background
        game_window.fill(black)
        
        # Draw border
        pygame.draw.rect(game_window, grey, pygame.Rect(0, 0, window_x, window_y), 2)
        
        # Draw snake with gradient effect
        for i, pos in enumerate(self.snake_body):
            if i == 0:  # Head
                pygame.draw.rect(game_window, yellow, 
                               pygame.Rect(pos[0]+1, pos[1]+1, grid_size-2, grid_size-2))
                # Add eyes
                eye_size = 3
                pygame.draw.circle(game_window, black, 
                                 (pos[0] + 5, pos[1] + 5), eye_size)
                pygame.draw.circle(game_window, black, 
                                 (pos[0] + grid_size - 5, pos[1] + 5), eye_size)
            else:  # Body
                # Alternating colors with fade effect
                intensity = max(100, 255 - i * 10)
                if i % 2 == 0:
                    color = pygame.Color(0, min(255, intensity), 0)
                else:
                    color = pygame.Color(0, min(255, intensity - 20), 0)
                pygame.draw.rect(game_window, color, 
                               pygame.Rect(pos[0]+1, pos[1]+1, grid_size-2, grid_size-2))
        
        # Draw fruit with pulsing effect
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
        fruit_size = int(grid_size * pulse)
        fruit_offset = (grid_size - fruit_size) // 2
        pygame.draw.rect(game_window, red,
                        pygame.Rect(self.fruit_position[0] + fruit_offset,
                                  self.fruit_position[1] + fruit_offset,
                                  fruit_size, fruit_size))
        
        # Draw UI
        self.draw_ui()
    
    def draw_ui(self):
        # Title in top-left corner (subtle)
        title_surface = title_font.render("Feeding Rudra", True, grey)
        game_window.blit(title_surface, (10, 10))
        
        # Score in top-right corner
        score_text = f"Score: {self.score}"
        score_surface = score_font.render(score_text, True, white)
        score_rect = score_surface.get_rect()
        score_rect.topright = (window_x - 10, 10)
        game_window.blit(score_surface, score_rect)
        
        # Length and speed info
        length_text = f"Length: {len(self.snake_body)}"
        length_surface = subtitle_font.render(length_text, True, grey)
        game_window.blit(length_surface, (10, window_y - 40))
        
        speed_text = f"Speed: {self.current_speed:.1f}"
        speed_surface = subtitle_font.render(speed_text, True, grey)
        game_window.blit(speed_surface, (10, window_y - 20))
    
    def draw_game_over_screen(self):
        # Create semi-transparent overlay
        overlay = pygame.Surface((window_x, window_y))
        overlay.set_alpha(180)
        overlay.fill(black)
        game_window.blit(overlay, (0, 0))
        
        # Animated game over text
        time_ms = pygame.time.get_ticks()
        scale = 1 + 0.1 * math.sin(time_ms * 0.003)
        
        # Main game over text
        game_over_text = "GAME OVER"
        font_size = int(48 * scale)
        dynamic_font = pygame.font.Font(None, font_size)
        game_over_surface = dynamic_font.render(game_over_text, True, red)
        game_over_rect = game_over_surface.get_rect(center=(window_x//2, window_y//2 - 60))
        game_window.blit(game_over_surface, game_over_rect)
        
        # Score with glow effect
        score_text = f"Final Score: {self.score}"
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            shadow_surface = score_font.render(score_text, True, (50, 50, 50))
            shadow_rect = shadow_surface.get_rect(center=(window_x//2 + offset[0], window_y//2 + offset[1]))
            game_window.blit(shadow_surface, shadow_rect)
        
        score_surface = score_font.render(score_text, True, yellow)
        score_rect = score_surface.get_rect(center=(window_x//2, window_y//2))
        game_window.blit(score_surface, score_rect)
        
        # Additional stats
        length_text = f"Snake Length: {len(self.snake_body)}"
        length_surface = subtitle_font.render(length_text, True, white)
        length_rect = length_surface.get_rect(center=(window_x//2, window_y//2 + 40))
        game_window.blit(length_surface, length_rect)
        
        fruits_text = f"Fruits Eaten: {self.fruits_eaten}"
        fruits_surface = subtitle_font.render(fruits_text, True, white)
        fruits_rect = fruits_surface.get_rect(center=(window_x//2, window_y//2 + 60))
        game_window.blit(fruits_surface, fruits_rect)
        
        # Restart instruction
        controls_text = "SPACE: Play Again | ESC: Quit | F11: Fullscreen"
        restart_surface = subtitle_font.render(controls_text, True, green)
        restart_rect = restart_surface.get_rect(center=(window_x//2, window_y//2 + 100))
        game_window.blit(restart_surface, restart_rect)
        
        pygame.display.update()
    
    def show_game_over(self):
        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            # Keep animating while waiting
            self.draw_game_over_screen()
            fps.tick(30)
    
    def run(self):
        running = True
        game_active = True
        
        while running:
            if game_active:
                if not self.handle_input():
                    running = False
                    continue
                
                self.move_snake()
                
                if self.check_collisions():
                    game_active = False
                else:
                    self.update_game()
                    self.draw_game()
                    pygame.display.update()
                    fps.tick(self.current_speed)
            else:
                # Game over state
                restart = self.show_game_over()
                if restart:
                    self.reset_game()
                    game_active = True
                else:
                    running = False
        
        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = SnakeGame()
    game.run()