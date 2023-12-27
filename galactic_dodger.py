import pygame
from random import randrange


def draw_img():
    if start_game is False:
        WIN.blit(highscore_surf, highscore_rect)
        WIN.blit(play_button_surf, play_button_rect)
        WIN.blit(exit_button_surf, exit_button_rect)

    else:
        WIN.blit(score_surf, score_rect)
        WIN.blit(player_surf, player_rect)

        for i in range(NUM_OF_EMEMIES):
            WIN.blit(enemy_1[i], enemy_1_rect[i])
            WIN.blit(enemy_2[i], enemy_2_rect[i])
            WIN.blit(enemy_3[i], enemy_3_rect[i])

        for bullet in bullets:
            pygame.draw.rect(WIN, (255, 0, 0), bullet)


def enemy_movement():
    if start_game:
        enemy_speed = 6
        for j in range(NUM_OF_EMEMIES):
            enemy_1_rect[j].y += enemy_speed
            enemy_2_rect[j].y += enemy_speed
            enemy_3_rect[j].y += enemy_speed
            if enemy_1_rect[j].top > HEIGHT:
                enemy_1_rect[j].y = randrange(-4000, 0)

            if enemy_2_rect[j].top > HEIGHT:
                enemy_2_rect[j].y = randrange(-4000, 0)

            if enemy_3_rect[j].top > HEIGHT:
                enemy_3_rect[j].y = randrange(-4000, 0)

            player_mask = pygame.mask.from_surface(player_surf)
            enemy_1_mask = pygame.mask.from_surface(enemy_1[j])
            enemy_2_mask = pygame.mask.from_surface(enemy_2[j])
            enemy_3_mask = pygame.mask.from_surface(enemy_3[j])

            if player_mask.overlap(
                enemy_1_mask,
                (
                    int(enemy_1_rect[j].x - player_rect.x),
                    int(enemy_1_rect[j].y - player_rect.y),
                ),
            ):
                pass

            if player_mask.overlap(
                enemy_2_mask,
                (
                    int(enemy_2_rect[j].x - player_rect.x),
                    int(enemy_2_rect[j].y - player_rect.y),
                ),
            ):
                pass

            if player_mask.overlap(
                enemy_3_mask,
                (
                    int(enemy_3_rect[j].x - player_rect.x),
                    int(enemy_3_rect[j].y - player_rect.y),
                ),
            ):
                pass


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


def shoot_bullet():
    global bullets, bullet_cooldown

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    if keys[pygame.K_z] and bullet_cooldown == 0:
        bullet_rect = pygame.Rect(player_rect.centerx - 5, player_rect.top, 10, 20)
        bullets.append(bullet_rect)
        bullet_cooldown = 20

    if mouse[0] and bullet_cooldown == 0:
        bullet_rect = pygame.Rect(player_rect.centerx - 5, player_rect.top, 10, 20)
        bullets.append(bullet_rect)
        bullet_cooldown = 20

    for bullet in bullets:
        bullet.y -= 8

        if bullet.y < 0:
            bullets.remove(bullet)

    if bullet_cooldown > 0:
        bullet_cooldown -= 1


def bullet_collision():
    global bullets, enemy_1, enemy_2, enemy_3, enemy_1_rect, enemy_2_rect, enemy_3_rect
    global enemy_1_health, enemy_2_health, enemy_3_health

    bullets_copy = bullets.copy()
    bullets_to_keep = []

    for bullet in bullets_copy:
        hit_enemy = False

        for j in range(NUM_OF_EMEMIES):
            enemy_1_mask = pygame.mask.from_surface(enemy_1[j])
            enemy_2_mask = pygame.mask.from_surface(enemy_2[j])
            enemy_3_mask = pygame.mask.from_surface(enemy_3[j])
            bullet_mask = pygame.mask.from_surface(pygame.Surface((10, 20)))
            bullet_mask_rect = bullet_mask.get_rect(topleft=(bullet.x, bullet.y))

            if enemy_1_mask.overlap(
                pygame.mask.from_surface(player_surf),
                (
                    bullet_mask_rect.x - enemy_1_rect[j].x,
                    bullet_mask_rect.y - enemy_1_rect[j].y,
                ),
            ) and bullet_mask_rect.colliderect(enemy_1_rect[j]):
                enemy_1_health -= 1
                hit_enemy = True

                if enemy_1_health == 0:
                    enemy_1_rect[j].y = randrange(-2000, 0)
                    enemy_1_health = 3

            elif enemy_2_mask.overlap(
                pygame.mask.from_surface(player_surf),
                (
                    bullet_mask_rect.x - enemy_2_rect[j].x,
                    bullet_mask_rect.y - enemy_2_rect[j].y,
                ),
            ) and bullet_mask_rect.colliderect(enemy_2_rect[j]):
                enemy_2_health -= 1
                hit_enemy = True

                if enemy_2_health == 0:
                    enemy_2_rect[j].y = randrange(-3000, 0)
                    enemy_2_health = 2

            elif enemy_3_mask.overlap(
                pygame.mask.from_surface(player_surf),
                (
                    bullet_mask_rect.x - enemy_3_rect[j].x,
                    bullet_mask_rect.y - enemy_3_rect[j].y,
                ),
            ) and bullet_mask_rect.colliderect(enemy_3_rect[j]):
                enemy_3_health -= 1
                hit_enemy = True

                if enemy_3_health == 0:
                    enemy_3_rect[j].y = randrange(-4000, 0)
                    enemy_3_health = 1

        if not hit_enemy:
            bullets_to_keep.append(bullet)

    bullets = bullets_to_keep


def score():
    global current_score, score_surf, score_rect, highscore_surf, highscore_rect

    if start_game:
        current_score += 1
        score_surf = FONT.render(f"{current_score}", False, "black")
        score_rect = score_surf.get_rect(center=(200, 20))

    else:
        highscore_surf = FONT.render(f"HIGHSCORE: {highscore}", False, "black")
        highscore_rect = highscore_surf.get_rect(bottomleft=(0, 600))


def high_score():
    if current_score > highscore:
        file = open("highscore.txt", "w")
        file.write(str(current_score))
        file.close()


# ! Implement restarting game logic
def restart_game():
    global start_game, current_score, player_rect, bullets, bullet_cooldown
    global enemy_1_rect, enemy_2_rect, enemy_3_rect, enemy_1_health, enemy_2_health, enemy_3_health

    start_game = False
    current_score = 0

    player_rect = player_surf.get_rect(center=(200, 575))

    bullets = []
    bullet_cooldown = 0

    for i in range(NUM_OF_EMEMIES):
        enemy_1_rect[i].y = randrange(-2000, 0)
        enemy_2_rect[i].y = randrange(-3000, 0)
        enemy_3_rect[i].y = randrange(-4000, 0)

    enemy_1_health = 3
    enemy_2_health = 2
    enemy_3_health = 1


pygame.init()

file = open("highscore.txt", "r")
highscore = int(file.read())
file.close()

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge")
clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.Font("assets/joystix_monospace.otf", 20)

start_game = False
current_score = 0

play_button_surf = pygame.image.load("assets/play_button.png").convert_alpha()
play_button_rect = play_button_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

exit_button_surf = pygame.image.load("assets/exit_button.png").convert_alpha()
exit_button_rect = exit_button_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

player_surf = pygame.image.load("assets/ship_1.png").convert_alpha()
player_rect = player_surf.get_rect(center=(200, 575))

bullets = []
bullet_cooldown = 0

NUM_OF_EMEMIES = 5
enemy_1 = []
enemy_1_rect = []

enemy_2 = []
enemy_2_rect = []

enemy_3 = []
enemy_3_rect = []

enemy_1_health = 3
enemy_2_health = 2
enemy_3_health = 1

for i in range(NUM_OF_EMEMIES):
    enemy_1_x = randrange(WIDTH)
    enemy_1_y = randrange(-2000, 0)
    enemy_1.append(pygame.image.load("assets/ship_2.png").convert_alpha())
    enemy_1_rect.append(enemy_1[i].get_rect(topleft=(enemy_1_x, enemy_1_y)))

    enemy_2_x = randrange(WIDTH)
    enemy_2_y = randrange(-3000, 0)
    enemy_2.append(pygame.image.load("assets/rock_1.png").convert_alpha())
    enemy_2_rect.append(enemy_2[i].get_rect(topleft=(enemy_2_x, enemy_2_y)))

    enemy_3_x = randrange(WIDTH)
    enemy_3_y = randrange(-4000, 0)
    enemy_3.append(pygame.image.load("assets/rock_2.png").convert_alpha())
    enemy_3_rect.append(enemy_3[i].get_rect(topleft=(enemy_3_x, enemy_3_y)))

while True:
    WIN.fill((173, 216, 230))
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            high_score()
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(mouse_pos) and start_game is False:
                start_game = True

            elif exit_button_rect.collidepoint(mouse_pos) and start_game is False:
                pygame.quit()

    score()
    enemy_movement()
    draw_img()
    player_controls()
    shoot_bullet()
    bullet_collision()

    pygame.display.update()
