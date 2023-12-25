import pygame

def menu_screen():

    if start_game is False:
        WIN.blit(highscore_surf, highscore_rect)
        WIN.blit(play_button_surf, play_button_rect)
        WIN.blit(exit_button_surf, exit_button_rect)

    else:
        WIN.blit(score_surf, score_rect)
        WIN.blit(player_surf, player_rect)


def player_controls():
    
    keys = pygame.key.get_pressed()
    player_speed = 5

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= player_speed

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    if player_rect.left <= 0:
        player_rect.left = 0
    
    elif player_rect.right >= WIDTH:
        player_rect.right = WIDTH


def score():
    global highscore, current_score, start_game, score_surf, score_rect, highscore_surf, highscore_rect

    if start_game:
        current_score += 1
        round(current_score, 0)
        score_surf = FONT.render(f"{current_score}", False, "black")
        score_rect = score_surf.get_rect(center = (200, 25))
    
    else:
        highscore_surf = FONT.render(f"HIGHSCORE: {highscore}", False, "black")
        highscore_rect = highscore_surf.get_rect(bottomleft= (0, 600))


def high_score():
    global highscore, current_score

    if current_score > highscore:

        file = open("highscore.txt", "w")
        file.write(str(current_score))
        file.close()


pygame.init()

file = open("highscore.txt", "r")
highscore = int(file.read())
print(highscore)
file.close()

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge")
clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.Font("assets/joystix_monospace.otf", 25)

start_game = False
current_score = 0

play_button_surf = pygame.image.load("assets/play_button.png").convert_alpha()
play_button_rect = play_button_surf.get_rect(center= (WIDTH//2, HEIGHT//2))

exit_button_surf = pygame.image.load("assets/exit_button.png").convert_alpha()
exit_button_rect = exit_button_surf.get_rect(center= (WIDTH//2, HEIGHT//2 + 100))

player_surf = pygame.image.load("assets/ship_1.png").convert_alpha()
player_rect = player_surf.get_rect(center= (200, 575))

enemy_1 = pygame.image.load("assets/ship_2.png").convert_alpha()
enemy_1_rect = enemy_1.get_rect(center = (0, 0))

enemy_2 = pygame.image.load("assets/rock_1.png").convert_alpha()
enemy_2_rect = enemy_2.get_rect(center = (0, 50))

enemy_3 = pygame.image.load("assets/rock_2.png").convert_alpha()
enemy_3_rect = enemy_3.get_rect(center = (0, 100))

while True:

    WIN.fill((173, 216, 230))
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            high_score()
            pygame.quit()

        elif (event.type == pygame.MOUSEBUTTONDOWN):
            if (play_button_rect.collidepoint(mouse_pos) and start_game is False):
                start_game = True

            elif (exit_button_rect.collidepoint(mouse_pos) and start_game is False):
                pygame.quit()

    score()
    menu_screen()
    player_controls()

    pygame.display.update()