import math
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('back.png')

# Caption and Icon
pygame.display.set_caption("Covid Killer - 2 Player")
icon = pygame.image.load('bacteria.png')
pygame.display.set_icon(icon)

# Player 1 (Green)
player1Img = pygame.image.load('takla.png')
player1X = 370
player1Y = 480
player1X_change = 0
player1_health = 100

# Player 2 (Red)
player2Img = pygame.image.load('virus.png')  # Same image for now
player2X = 370
player2Y = 100
player2X_change = 0
player2_health = 100

# Player 1 Bullet
bulletImg = pygame.image.load('weather.png')
bullet1X = 0
bullet1Y = 480
bullet1X_change = 0
bullet1Y_change = 20
bullet1_state = "ready"
player1_last_fire_time = 0
player1_fire_rate = 100  # Reduced fire rate to make it faster

# Player 2 Bullet
bullet2Img = pygame.image.load('covidbullet.png')
bullet2X = 0
bullet2Y = 100
bullet2X_change = 0
bullet2Y_change = 20
bullet2_state = "ready"
player2_last_fire_time = 0
player2_fire_rate = 100  # Reduced fire rate to make it faster

# Score
score_value = 0
high_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Player win
over_font = pygame.font.Font('freesansbold.ttf', 64)
small_font = pygame.font.Font('freesansbold.ttf', 32)


def game_over_screen(winner):
    screen.fill((0, 0, 0))  # Fill the screen with black
    if winner == 1:
        game_over_text = over_font.render("Swordmaster Wins", True, (0, 255, 0))
    else:
        game_over_text = over_font.render("Raito_san Wins", True, (255, 0, 0))
    
    screen.blit(game_over_text, (180, 230))
    restart_button = create_button("Restart", 150, 350, 200, 50)
    quit_button = create_button("Quit", 450, 350, 200, 50)
    pygame.display.update()
    return restart_button, quit_button

def player(x, y, img):
    screen.blit(img, (x, y))

def fire_bullet(x, y, player_num):
    global bullet1_state, bullet2_state
    if player_num == 1:
        bullet1_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))
    elif player_num == 2:
        bullet2_state = "fire"
        screen.blit(bullet2Img, (x + 16, y + 10))

def isCollision(objX, objY, bulletX, bulletY):
    distance = math.sqrt(math.pow(objX - bulletX, 2) + (math.pow(objY - bulletY, 2)))
    return distance < 27

def show_health_bar(x, y, health, is_player=True):
    if is_player:
        # Player's health bar (white background, green foreground)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 5))  # White background
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health, 5))  # Green foreground
    else:
        # Player's health bar (white background, red foreground)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 5))  # White background
        pygame.draw.rect(screen, (255, 0, 0), (x, y, health, 5))  # Red foreground

def create_button(text, x, y, width, height):
    button_color = (255, 255, 255)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = small_font.render(text, True, (0, 0, 0))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return button_rect

def handle_button_click(button_rect, action):
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
        return action
    return None

# Create a Clock object to manage the frame rate
clock = pygame.time.Clock()

# Game Loop
running = True
game_over = False
game_started = False

# Main Menu
def main_menu():
    screen.fill((0, 0, 0))  # Fill the screen with black
    menu_text = over_font.render("Covid Killer", True, (255, 255, 255))
    screen.blit(menu_text, (200, 250))
    start_button = create_button("Start", 150, 350, 200, 50)
    quit_button = create_button("Quit", 450, 350, 200, 50)
    pygame.display.update()
    return start_button, quit_button

while running:

    # Limit the frame rate to 60 frames per second
    clock.tick(60)

    # Main Menu
    if not game_started:
        start_button, quit_button = main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if handle_button_click(start_button, "start") == "start":
            game_started = True
        if handle_button_click(quit_button, "quit") == "quit":
            running = False
        continue

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    if game_over:
        if score_value > high_score:
            high_score = score_value
        winner = 1 if player1_health > player2_health else 2
        restart_button, quit_button = game_over_screen(winner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if handle_button_click(restart_button, "restart") == "restart":
            # Restart the game
            game_over = False
            score_value = 0
            player1_health = 100
            player2_health = 100
            player1X = 370
            player1Y = 480
            player2X = 370
            player2Y = 100
            bullet1_state = "ready"
            bullet2_state = "ready"
        if handle_button_click(quit_button, "quit") == "quit":
            running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1X_change = -3
            if event.key == pygame.K_RIGHT:
                player1X_change = 3
            if event.key == pygame.K_j:
                if bullet1_state == "ready":
                    current_time = pygame.time.get_ticks()
                    if current_time - player1_last_fire_time > player1_fire_rate:
                        bullet1X = player1X
                        fire_bullet(bullet1X, bullet1Y, 1)
                        player1_last_fire_time = current_time
            if event.key == pygame.K_a:
                player2X_change = -3
            if event.key == pygame.K_d:
                player2X_change = 3
            if event.key == pygame.K_z:
                if bullet2_state == "ready":
                    current_time = pygame.time.get_ticks()
                    if current_time - player2_last_fire_time > player2_fire_rate:
                        bullet2X = player2X
                        fire_bullet(bullet2X, bullet2Y, 2)
                        player2_last_fire_time = current_time

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1X_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player2X_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    player1X += player1X_change
    player2X += player2X_change

    if player1X <= 0:
        player1X = 0
    elif player1X >= 736:
        player1X = 736

    if player2X <= 0:
        player2X = 0
    elif player2X >= 736:
        player2X = 736

    # Bullet Movement
    if bullet1Y <= 0:
        bullet1Y = 480
        bullet1_state = "ready"

    if bullet2Y >= 600:
        bullet2Y = 100
        bullet2_state = "ready"

    if bullet1_state == "fire":
        fire_bullet(bullet1X, bullet1Y, 1)
        bullet1Y -= bullet1Y_change

    if bullet2_state == "fire":
        fire_bullet(bullet2X, bullet2Y, 2)
        bullet2Y += bullet2Y_change

    # Collision between bullets
    if isCollision(player1X, player1Y, bullet2X, bullet2Y):
        bullet2Y = 100
        bullet2_state = "ready"
        player1_health -= 10  # Reduce player health by 10 on collision
        if player1_health <= 0:  # If player health is 0 or less
            game_over = True

    if isCollision(player2X, player2Y, bullet1X, bullet1Y):
        bullet1Y = 480
        bullet1_state = "ready"
        player2_health -= 10  # Reduce player health by 10 on collision
        if player2_health <= 0:  # If player health is 0 or less
            game_over = True

    player(player1X, player1Y, player1Img)
    player(player2X, player2Y, player2Img)
    show_health_bar(player1X, player1Y - 20, player1_health)
    show_health_bar(player2X, player2Y - 20, player2_health, is_player=False)

   
    pygame.display.update()
