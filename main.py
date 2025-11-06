import pygame
import random
import os
import sys
import math

pygame.init()
pygame.mixer.init()

screen_x = 800
screen_y = 450

display = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Super Pong")

# globals
paddle_size = 100
SCREEN_RECT = pygame.Rect(0, 0, screen_x, screen_y)
mouse_pos = pygame.mouse.get_pos()
play_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2, 200, 50)
options_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2 + 70, 200, 50)
quit_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2 + 140, 200, 50)


# Game state variable
game_paused = False

# colors
white = pygame.Color("#FAFAFA")
black =pygame.Color("#000000")
red = pygame.Color("#FD0000")
green = pygame.Color("#07F51B")
gray = pygame.Color("#4A5154")
PURPLE_HEX = pygame.Color("#981398")

menu_title = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# load game sound effects
hit_sound = pygame.mixer.Sound("Sound Effects/hit.mp3")
player_score_sound = pygame.mixer.Sound("Sound Effects/player_score.mp3")
computer_score_sound = pygame.mixer.Sound("Sound Effects/computer_score.mp3")
button_click = pygame.mixer.Sound("Sound Effects/button_click.wav")

def draw_text(text, font, color, display, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    display.blit(textobj, textrect)

def main_menu():
    running = True

    pygame.mixer.music.load("Music/main_menu.mp3")
    pygame.mixer.music.play(-1)

    while running: 
        display.fill(black)

        draw_text("Super Pong", menu_title, white, display, screen_x // 2, screen_y // 2 - 100)

        if play_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, play_button)
        else: 
            pygame.draw.rect(display, green, play_button)

        if options_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, options_button)
        else:
            pygame.draw.rect(display, red, options_button)
        
        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, quit_button)
        else: 
            pygame.draw.rect(display, white, quit_button)

        draw_text("Play", button_font, black, display, play_button.centerx, play_button.centery)
        draw_text("Options", button_font, black, display, options_button.centerx, options_button.centery)
        draw_text("Quit", button_font, black, display, quit_button.centerx, quit_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    button_click.play()
                    game()
                    return # Exit the menu loop to start the game
                elif options_button.collidepoint(event.pos):
                    button_click.play()
                    options()
                elif quit_button.collidepoint(event.pos):
                    button_click.play()
                    running = False
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def options():
    options = True

    while options:
        display.fill(black)

        # Mouse position
        mouse_pos = pygame.mouse.get_pos()

        draw_text("Super Pong", menu_title, white, display, screen_x // 2, screen_y // 2 - 100)
        
        difficulty_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2, 200, 50)
        audio_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2 + 70, 200, 50)
        back_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2 + 140, 200, 50)

        if difficulty_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, difficulty_button)
        else: 
            pygame.draw.rect(display, white, difficulty_button)

        if audio_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, audio_button)
        else: 
            pygame.draw.rect(display, white, audio_button)
        
        if back_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, back_button)
        else: 
            pygame.draw.rect(display, white, back_button)
            
        draw_text("Difficulty", button_font, black, display, difficulty_button.centerx, difficulty_button.centery)
        draw_text("Audio", button_font, black, display, audio_button.centerx, audio_button.centery)
        draw_text("Back", button_font, black, display, back_button.centerx, back_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if difficulty_button.collidepoint(event.pos):
                    print("Opening difficulty options")
                    button_click.play()
                    pass
                elif audio_button.collidepoint(event.pos):
                    print("Opening audio options")
                    button_click.play()
                    pass
                elif back_button.collidepoint(event.pos):
                    button_click.play()
                    main_menu()

        pygame.display.update()

def pause_menu():

    paused = True
    
    while paused: 

        display.fill((50, 50, 50))

        draw_text("PAUSED", menu_title, white, display, screen_x // 2, screen_y // 2 - 100)

        resume_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2, 200, 50)
        quit_button = pygame.Rect(screen_x // 2 - 100, screen_y // 2 + 140, 200, 50)

        draw_text("Resume", button_font, black, display, resume_button.centerx, play_button.centery)
        draw_text("Quit", button_font, black, display, quit_button.centerx, quit_button.centery)

        if resume_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, resume_button)
        else: 
            pygame.draw.rect(display, green, resume_button)

        if quit_button.collidepoint(mouse_pos):
            pygame.draw.rect(display, gray, quit_button)
        else: 
            pygame.draw.rect(display, gray, quit_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    game()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit

        pygame.display.update()


score_font = pygame.font.SysFont('Impact', 30)
rally_font = pygame.font.SysFont('Impact', 20)

# Create background
background = pygame.image.load("assets/Board.png").convert()
background = pygame.transform.scale(background, (screen_x, screen_y))

# Create enemy scorebar image
enemy_scorebar = pygame.image.load("assets/ScoreBar.png").convert_alpha()
enemy_rect = enemy_scorebar.get_rect(topleft=(0, 0))

# Create player scorebar image
player_scorebar = pygame.image.load("assets/ScoreBar.png").convert_alpha()
player_scorebar = pygame.transform.flip(player_scorebar, True, False)
player_rect = player_scorebar.get_rect(topright=(screen_x, 0))

# Function for displaying both scorebars inside the main gameplay loop 
def display_scorebar():
    display.blit(enemy_scorebar, enemy_rect)
    display.blit(player_scorebar, player_rect)

def draw_background():
    display.blit(background, (0,0))

def display_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))

class Player(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, x, y, size):
        super().__init__()
        self.reset(x, y, size)
        
    def update(self, keys):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed 
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed 
        if self.rect.top < 0:
            self.rect.top = 0 
        if self.rect.bottom > screen_y:
            self.rect.bottom = screen_y
    
    def reset(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.image.load("assets/Player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8

class Enemy(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, x, y, size):
        super().__init__()
        self.reset(x, y, size)

    # Basic AI logic
    def update(self):
        self.t = (self.t + 1) % self.react
        if self.t == 0:                               # reaction delay
            target = ball.rect.centery + random.randint(-self.err, self.err)
            if random.random() < self.miss:           # occasional whiff
                target += random.choice((-1, 1)) * random.randint(70, 130)
            self.vy += (1 if target > self.rect.centery else -1) * 3.5  # acceleration step
        self.vy = max(-self.maxv, min(self.maxv, self.vy * 0.97))     # clamp & damp
        self.rect.y += int(self.vy)
        self.rect.clamp_ip(SCREEN_RECT)
    
    def reset(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.image.load("assets/Computer.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.vy, self.t = 0.0, 0        # velocity, think timer
        # knobs
        self.maxv, self.err, self.react, self.miss = 12, 6, 3, 0.04

class Ball(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, x, y, size):
        super().__init__()
        self.reset(x, y, size)

    def move(self):
        prev = self.rect.copy()
        self.motion_image = pygame.image.load("assets/BallMotion.png").convert_alpha()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # bounce off top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= screen_y:
            self.speed_y = -self.speed_y
        # right paddle (player)
        if self.rect.colliderect(player.rect) and self.speed_x > 0 and prev.right <= player.rect.left:
            self.rect.right = player.rect.left # resolve overlap
            self.speed_x = -self.speed_x
            hit_sound.play()
        # left paddle (enemy) 
        elif self.rect.colliderect(enemy.rect) and self.speed_x < 0 and prev.left >= enemy.rect.right:
            self.rect.left = enemy.rect.right
            self.speed_x = -self.speed_x
            hit_sound.play()
        # designated goal area
        if self.rect.left < 0:
            self.goal = 1
        if self.rect.right > screen_x:
            self.goal = -1
        return self.goal
    
    def rally(self):
        if self.rect.colliderect(player) or self.rect.colliderect(enemy):
            self.rally_count += 1
        return self.rally_count

    def reset(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = 6
        angle = random.uniform(0, 2 * math.pi)  
        self.speed_x = self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)
        
        self.goal = 0 # 1 is the player and -1 is the CPU
        self.rally_count = 0
        self.image = pygame.image.load("assets/Ball.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

# create player objects
player = Player(screen_x - 50, screen_y // 2, paddle_size)
enemy = Enemy(50, screen_y // 2, paddle_size)
ball = Ball(screen_x // 2, screen_y // 2, size = 10)

# create sprite groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()

# Add objects to groups
enemy_group.add(enemy)
player_group.add(player)
ball_group.add(ball)

def game():

    # Gameplay variables
    player_score = 0
    enemy_score = 0
    goal = 0 # 1 is the player and -1 is the CPU
    FPS = 60
    speed_increase = 0
    rally_count = 0
    live_ball = False
    running = True
    
    # load in music at random from the tracklist
    music_folder = "Tracks"
    songs = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(('.mp3', '.ogg', '.wav'))]
    random_song = random.choice(songs)
    pygame.mixer.music.load(random_song)
    pygame.mixer.music.play(-1)

    while running: 

        clock.tick(FPS)

        draw_background()
        # Display UI
        display_scorebar()
        display_text(f"CPU: {enemy_score}", score_font, black, 220, 5)
        display_text(f"Player: {player_score}", score_font, black, screen_x - 300, 5)
        display_text(f"R a l l i e s", rally_font, PURPLE_HEX, screen_x // 2 - 40, 0)
        display_text(f"{rally_count}", rally_font, PURPLE_HEX, screen_x // 2 - 7, 20)

        keys = pygame.key.get_pressed()
        player_group.draw(display)
        enemy_group.draw(display)

        if live_ball == True:
            speed_increase += 1.5
            goal = ball.move()
            rally_count = ball.rally()
            if goal == 0:
                ball_group.draw(display)
                player_group.update(keys)
                enemy_group.update() 
            else:
                live_ball = False
                if goal == 1:
                    player_score += 1
                    player_score_sound.play()
                elif goal == -1:
                    enemy_score += 1
                    computer_score_sound.play()
        
        if live_ball == False: 
            if goal == 0:
                display_text("CLICK ANYWHERE TO START", score_font, white, screen_x // 2 - 150, screen_y // 2)
            if goal == 1: 
                display_text("YOU SCORED!", score_font, white, 325, screen_y // 2 - 100)
                display_text("CLICK ANYWHERE TO START", score_font, white, screen_x // 2 - 150, screen_y // 2)
            if goal == -1: 
                display_text("THE COMPUTER SCORED!", score_font, white, 265, screen_y // 2 - 100)
                display_text("CLICK ANYWHERE TO START", score_font, white, screen_x // 2 - 150, screen_y // 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and live_ball == False:
                live_ball = True
                ball.reset(screen_x // 2, screen_y // 2, size = 10)
                player.reset(screen_x - 50, screen_y // 2, paddle_size)
                enemy.reset(50, screen_y // 2, paddle_size)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

        if speed_increase > 500:
            speed_increase = 0
            if ball.speed_x < 0:
                ball.speed_x -= 1
            if ball.speed_x > 0:
                ball.speed_x += 1
            if ball.speed_x < 0:
                ball.speed_x -= 1
            if ball.speed_x > 0:
                ball.speed_x += 1

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    options()
    game() # This fucntion will be called after the Play button is clicked from the main menu
    pause_menu()