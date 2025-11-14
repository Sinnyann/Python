import pygame
import random
import os
import sys
import time

pygame.init()
pygame.mixer.init()

screen_x = 1280
screen_y = 720

display = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Super Pong")

# globals
paddle_size = 100
SCREEN_RECT = pygame.Rect(0, 0, screen_x, screen_y)
mouse_pos = pygame.mouse.get_pos()
current_difficulty = "Normal"
snes_font = pygame.font.Font("pixel_font.ttf", 16)
score_font = pygame.font.Font("pixel_font.ttf", 22)

# Game state variable
paused = False

# colors
white = pygame.Color("#FAFAFA")
black = pygame.Color("#000000")
red = pygame.Color("#FD0000")
green = pygame.Color("#07F51B")
gray = pygame.Color("#4A5154")
yellow = pygame.Color("#DDEC0D")
orange = pygame.Color("#FF7D04")
PURPLE_HEX = pygame.Color("#981398")

class Button:
    def __init__(self, text, x, y, width, height, color, selected_color, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text_color = text_color
        self.action = action
        self.hover_color = gray
        self.default_color = color
        self.is_hovered = False
        self.selected = False
        self.selected_color = selected_color

    def draw(self):
        if self.selected:
            fill = self.selected_color
        elif self.is_hovered:
            fill = self.hover_color
        else:
            fill = self.default_color

        pygame.draw.rect(display, fill, self.rect, border_radius=12)

        font = pygame.font.Font("pixel_font.ttf", 16)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center = self.rect.center)
        display.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION: 
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.selected = True
                button_click.play()
                self.action()
                return True
            else: 
                self.selected = False
        return False
                       
def set_difficulty(level, enemies_group):
    # level is one of: "Easy", "Normal", "Hard", "Insane"
    method = level.lower()
    for e in enemies_group.sprites():
        getattr(e, method)()     # calls e.easy(), e.normal(), etc.

def choose_difficulty(level):
    global current_difficulty
    current_difficulty = level
    try:
        set_difficulty(level, enemy_group)
    except NameError:
        pass  # enemy_group not created yet; will be applied on spawn

def draw_menu_bg():
    menu_background = pygame.image.load("Assets/title_screen.png")
    menu_background = pygame.transform.scale(menu_background, (screen_x, screen_y))
    display.blit(menu_background, (0,0))

def draw_text(text, color, x, y, font_style):
    textobj = font_style.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    display.blit(textobj, textrect)

def main_menu():
    main_menu = True

    pygame.mixer.music.load("Music/main_menu.mp3")
    pygame.mixer.music.play(-1)

    play_button = Button("P L A Y", screen_x // 2 - 100, screen_y // 2, 200, 50, white, white, black, game)
    settings_button = Button("S E T T I N G S", screen_x // 2 - 100, screen_y // 2 + 70, 200, 50, white, white, black, settings)
    quit_button = Button("Q U I T", screen_x // 2 - 100, screen_y // 2 + 140, 200, 50, white, white, black, sys.exit)

    draw_menu_bg()
    
    title_style = pygame.font.Font("pixel_font.ttf", 50)
    title_font = title_style.render("Super Pong!", True, white)
    display.blit(title_font, (screen_x // 2 - 260, screen_y // 2 - 100))

    while main_menu:
        
        play_button.draw()
        settings_button.draw()
        quit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()            
            play_button.handle_event(event)
            settings_button.handle_event(event)
            quit_button.handle_event(event)
        pygame.display.update()

def settings():
    settings = True
    
    easy_button = Button("E A S Y", screen_x // 2 - 250, screen_y // 2, 140, 50, white, green, black, lambda: choose_difficulty("Easy"))
    normal_button = Button("N O R M A L", screen_x // 2 - 80, screen_y // 2, 150, 50, white, yellow, black, lambda: choose_difficulty("Normal"))
    hard_button = Button("H A R D", screen_x // 2 + 100, screen_y // 2, 140, 50, white, red, black, lambda: choose_difficulty("Hard"))
    insane_button = Button("I N S A N E", screen_x // 2 - 80, screen_y // 2 + 80, 150, 50, white, orange, black, lambda: choose_difficulty("Insane"))

    back_button = Button("<-----", 10, 10, 100, 50, white, white, black, main_menu)

    while settings:
        display.fill(black)

        easy_button.draw()
        normal_button.draw()
        hard_button.draw()
        back_button.draw()
        insane_button.draw()

        draw_text("S E T T I N G S", white, screen_x // 2, screen_y // 2 - 250, snes_font)
        draw_text("D I F F I C U L T Y", white, screen_x // 2, screen_y // 2 - 50, snes_font)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            back_button.handle_event(event)
            easy_button.handle_event(event)
            normal_button.handle_event(event)
            hard_button.handle_event(event)
            insane_button.handle_event(event)

        pygame.display.update()

def pause_menu():

    global paused

    resume_button = Button("R E S U M E", screen_x // 2 - 100, screen_y // 2, 200, 50, white, white, black, game)
    quit_button = Button("Q U I T", screen_x // 2 - 100, screen_y // 2 + 140, 200, 50, white, white, black, sys.exit)
    title_screen = Button("M A I N  M E N U", screen_x // 2 - 100, screen_y // 2 + 180, 200, 50, white, white, black, main_menu)

    while paused: 

        display.fill((50, 50, 50))

        draw_text("P A U S E D", white, screen_x // 2, screen_y // 2 - 100, snes_font)

        resume_button.draw()
        quit_button.draw()
        title_screen.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

            resume_button.handle_event(event)
            quit_button.handle_event(event)
            title_screen.handle_event(event)

        pygame.display.update()

# load game sound effects
hit_sound = pygame.mixer.Sound("Sound Effects/hit.mp3")
player_score_sound = pygame.mixer.Sound("Sound Effects/player_score.mp3")
computer_score_sound = pygame.mixer.Sound("Sound Effects/computer_score.mp3")
button_click = pygame.mixer.Sound("Sound Effects/button_click.wav")

# Create play area background
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

def countdown_timer():
   countdown_value = 3
   # Custom user event for the timer 
   TIMER_EVENT = pygame.USEREVENT + 1
   pygame.time.set_timer(TIMER_EVENT, 1000)  # Trigger every 1000 milliseconds (1 second)
   countdown_value -= 1
   if countdown_value < 0:
    draw_text("S T A R T", white, screen_x // 2, screen_y // 2)

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
        self.image = pygame.transform.scale(self.image, (17, 120))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 16

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
            self.vy += (1 if target > self.rect.centery else -1) * self.ACCEL_STEP # acceleration step
        self.vy = max(-self.maxv, min(self.maxv, self.vy * self.DAMPING))     # clamp & damp
        self.rect.y += int(self.vy)
        self.rect.clamp_ip(SCREEN_RECT)
    
    def reset(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image = pygame.image.load("assets/Computer.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (17, 120))
        self.rect = self.image.get_rect(center=(x, y))
        self.vy, self.t = 0.0, 0        # velocity, think timer
  
    # Difficulty: Easy
    def easy(self):
        self.maxv, self.err, self.react, self.miss = 14, 8, 2, 0.1   # lower cap, sloppier aim, slow reactions, more misses
        self.ACCEL_STEP = 2.3
        self.DAMPING = 0.96

    # Difficulty: Normal
    def normal(self):
        self.maxv, self.err, self.react, self.miss = 14, 6, 2, 0.08 # normalized variables
        self.ACCEL_STEP = 2.8
        self.DAMPING = 0.97

    # Difficulty: Hard
    def hard(self):
        self.maxv, self.err, self.react, self.miss = 14, 3, 1, 0.03 # higher max velocity cap, better aim, faster reactions, slightly more misses
        self.ACCEL_STEP = 3.0
        self.DAMPING = 0.985

    # Difficulty: Insane
    def insane(self):
        self.maxv, self.err, self.react, self.miss = 16, 2, 1, 0.02 # pinpoint precision
        self.ACCEL_STEP = 5.0
        self.DAMPING = 0.99

class Ball(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, x, y):
        super().__init__()
        self.reset(x, y)

    def reset(self, x, y):
        self.image = pygame.image.load("assets/pongball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=(x, y))

        # simple integer speeds
        base_speed = 12
        self.dx = random.choice([-base_speed, base_speed])   # left or right
        self.dy = random.randint(-3, 3)
        if self.dy == 0:
            self.dy = 1

        self.max_dy = 16
        self.rally_count = 0
        self.goal = 0

    def move(self):
        prev = self.rect.copy()

        # move
        self.rect.x += self.dx
        self.rect.y += self.dy

        # bounce top/bottom
        if self.rect.top < 0:
            self.rect.top = 0
            self.dy = -self.dy
        elif self.rect.bottom > screen_y:
            self.rect.bottom = screen_y
            self.dy = -self.dy

        # --- paddle collisions ---
        # right paddle (player)
        if self.rect.colliderect(player.rect) and self.dx > 0 and prev.right <= player.rect.left:
            self.rect.right = player.rect.left
            self.dx = -self.dx
            self._simple_spin(player.rect)
            self.rally_count += 1
            hit_sound.play()

        # left paddle (enemy)
        elif self.rect.colliderect(enemy.rect) and self.dx < 0 and prev.left >= enemy.rect.right:
            self.rect.left = enemy.rect.right
            self.dx = -self.dx
            self._simple_spin(enemy.rect)
            self.rally_count += 1
            hit_sound.play()

        # goals
        if self.rect.left < 0:
            self.goal = 1     # player scores
            self.rally_count = 0
        elif self.rect.right > screen_x:
            self.goal = -1    # CPU scores
            self.rally_count = 0
        else:
            self.goal = 0

        return self.goal

    def _simple_spin(self, paddle_rect):
        # relative hit: above, middle, or below
        if self.rect.centery < paddle_rect.centery - paddle_rect.height // 4:
            self.dy -= 2
        elif self.rect.centery > paddle_rect.centery + paddle_rect.height // 4:
            self.dy += 2
        else:
            # center hit: tiny random variation to avoid perfectly flat rallies
            self.dy += random.choice([-1, 0, 1])

        # clamp dy and avoid dead-flat
        if self.dy == 0:
            self.dy = random.choice([-1, 1])
        if self.dy > self.max_dy:
            self.dy = self.max_dy
        elif self.dy < -self.max_dy:
            self.dy = -self.max_dy

# create objects
player = Player(screen_x - 50, screen_y // 2, paddle_size)
enemy = Enemy(50, screen_y // 2, paddle_size)
ball = Ball(screen_x // 2, screen_y // 2)
getattr(enemy, current_difficulty.lower())()

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
    live_ball = False
    running = True
    
    # load in music at random from the tracklist
    music_folder = "Tracks"
    songs = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(('.mp3', '.ogg', '.wav'))]
    random_song = random.choice(songs)
    pygame.mixer.music.load(random_song)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    
    while running: 

        clock.tick(FPS)
        draw_background()
        # Display UI
        display_scorebar()
        draw_text(f"CPU: {enemy_score}", black, 300, 30, score_font)
        draw_text(f"Player: {player_score}", black, screen_x - 250, 30, score_font)
        draw_text(f"R a l l i e s", white, screen_x // 2, 15, snes_font)
        draw_text(f"{ball.rally_count}", white, screen_x // 2, 40, snes_font)

        keys = pygame.key.get_pressed()
        player_group.draw(display)
        enemy_group.draw(display)

        if live_ball == True:
            speed_increase += 1.5
            goal = ball.move()
            ball_group.update()
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
                draw_text("PRESS ANY KEY TO START", white, screen_x // 2, screen_y // 2, snes_font)
            if goal == 1: 
                draw_text("YOU SCORED!", white, screen_x // 2, screen_y // 2 - 100, snes_font)
                draw_text("PRESS ANY KEY TO CONTINUE", white, screen_x // 2, screen_y // 2, snes_font)
            if goal == -1: 
                draw_text("THE COMPUTER SCORED!", white, screen_x // 2, screen_y // 2 - 100, snes_font)
                draw_text("PRESS ANY KEY TO CONTINUE", white, screen_x // 2, screen_y // 2, snes_font)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and live_ball == False:
                countdown_timer()
                live_ball = True
                ball.reset(screen_x // 2, screen_y // 2)
                player.reset(screen_x - 50, screen_y // 2, paddle_size)
                enemy.reset(50, screen_y // 2, paddle_size)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    pause_menu()

        if speed_increase > 500:
            speed_increase = 0

            
        pygame.display.update()

if __name__ == "__main__":
    main_menu()