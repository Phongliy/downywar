import pygame
import math
import random
import os

pygame.init()

# Cài đặt màn hình
WIDTH, HEIGHT = 1500, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DownyWar")
clock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (150, 150, 150)

# Khai báo font
font = pygame.font.Font(None, 50)

# Load ảnh items
heart_size = 50
heart_img = pygame.image.load("hp.png")
heart_img = pygame.transform.scale(heart_img, (heart_size, heart_size))
heart_img.set_colorkey(WHITE)

shield_size = 50
shield_img = pygame.image.load("shield.png")
shield_img = pygame.transform.scale(shield_img, (shield_size, shield_size))
shield_img.set_colorkey(WHITE)

bullets_size = 50
bullets_img = pygame.image.load("bullet.png")
bullets_img = pygame.transform.scale(bullets_img, (bullets_size, bullets_size))
bullets_img.set_colorkey(WHITE)

# Hàm tạo vị trí ngẫu nhiên
def random_pos(size):
    x = random.randint(0, WIDTH - size)
    y = random.randint(0, HEIGHT - size)
    return pygame.Rect(x, y, size, size)

# Load ảnh nhân vật theo loại súng (để trống đường dẫn cho bạn điền)
# Player 1
snake1_ak_img = pygame.image.load("nv1ak.png")  # Điền đường dẫn cho AK
snake1_ak_img = pygame.transform.scale(snake1_ak_img, (70,50))
snake1_sniper_img = pygame.image.load("nv1awm.png")  # Điền đường dẫn cho SNIPER
snake1_sniper_img = pygame.transform.scale(snake1_sniper_img, (70, 50))
snake1_shotgun_img = pygame.image.load("nv1shotgun.png")  # Điền đường dẫn cho SHOTGUN
snake1_shotgun_img = pygame.transform.scale(snake1_shotgun_img, (70, 50))

# Player 2
snake2_ak_img = pygame.image.load("nv2ak.png")  # Điền đường dẫn cho AK
snake2_ak_img = pygame.transform.scale(snake2_ak_img, (70, 50))
snake2_sniper_img = pygame.image.load("nv2awm.png")  # Điền đường dẫn cho SNIPER
snake2_sniper_img = pygame.transform.scale(snake2_sniper_img, (70, 50))
snake2_shotgun_img = pygame.image.load("nv2shotgun.png")  # Điền đường dẫn cho SHOTGUN
snake2_shotgun_img = pygame.transform.scale(snake2_shotgun_img, (70, 50))

# Lớp đạn
class Bullet:
    def __init__(self, x, y, angle, speed=9, damage=5):
        offset = 30
        self.x = x + math.cos(math.radians(angle)) * offset
        self.y = y - math.sin(math.radians(angle)) * offset
        self.dx = math.cos(math.radians(angle)) * speed
        self.dy = -math.sin(math.radians(angle)) * speed
        self.radius = 5
        self.damage = damage

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius)

# Các biến toàn cục
AK, SNIPER, SHOTGUN = 0, 1, 2
damage_values = {AK: 5, SNIPER: 50, SHOTGUN: 3}
max_ammo = {AK: 30, SNIPER: 5, SHOTGUN: 10}
reserve_ammo_max = {AK: 90, SNIPER: 15, SHOTGUN: 30}
reload_times = {AK: 2000, SNIPER: 3000, SHOTGUN: 2500}
shoot_delays = {AK: 100, SNIPER: 1000, SHOTGUN: 500}
step = 5
rotate_speed = 10

# Hàm vẽ text
def draw_text(text, x, y, size=30, color=BLACK):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Hàm reset game
def reset_game():
    global snake1_x, snake1_y, snake1_angle, snake1_health, snake1_ammo, snake1_reserve_ammo, snake1_reloading, snake1_reload_start, snake1_shield_on, snake1_last_shot
    global snake2_x, snake2_y, snake2_angle, snake2_health, snake2_ammo, snake2_reserve_ammo, snake2_reloading, snake2_reload_start, snake2_shield_on, snake2_last_shot
    global bullets, game_over
    snake1_x, snake1_y, snake1_angle, snake1_health = 699, 420, 0, 100
    snake2_x, snake2_y, snake2_angle, snake2_health = 250, 300, 0, 100
    snake1_ammo = {AK: max_ammo[AK], SNIPER: max_ammo[SNIPER], SHOTGUN: max_ammo[SHOTGUN]}
    snake2_ammo = {AK: max_ammo[AK], SNIPER: max_ammo[SNIPER], SHOTGUN: max_ammo[SHOTGUN]}
    snake1_reserve_ammo = {AK: reserve_ammo_max[AK], SNIPER: reserve_ammo_max[SNIPER], SHOTGUN: reserve_ammo_max[SHOTGUN]}
    snake2_reserve_ammo = {AK: reserve_ammo_max[AK], SNIPER: reserve_ammo_max[SNIPER], SHOTGUN: reserve_ammo_max[SHOTGUN]}
    snake1_reloading = snake2_reloading = False
    snake1_reload_start = snake2_reload_start = 0
    snake1_shield_on = snake2_shield_on = False
    snake1_last_shot = snake2_last_shot = 0
    bullets = []
    game_over = False

# Load và scale map
def load_map(path):
    if os.path.exists(path):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (WIDTH, HEIGHT))
    return None

map1_img = load_map("map1.png")
map1_background = load_map("map1bg.png")
map2_img = load_map("map2.png")
map2_background = load_map("map2bg.png")
title_img = pygame.image.load("title.png")
title_img = pygame.transform.scale(title_img, (1145, 508))
map1_mask = pygame.mask.from_surface(map1_img) if map1_img else None
map1_background_mask = pygame.mask.from_surface(map1_background) if map1_background else None
map2_mask = pygame.mask.from_surface(map2_img) if map2_img else None
map2_background_mask = pygame.mask.from_surface(map2_background) if map2_background else None

# Kiểm tra va chạm với map
def check_map_collision(x, y, map_mask):
    if 0 <= int(x) < WIDTH and 0 <= int(y) < HEIGHT:
        return map_mask.get_at((int(x), int(y)))
    return True

# Kiểm tra va chạm với đạn
def check_collision(bullet, x, y):
    return math.hypot(bullet.x - x, bullet.y - y) < 25

# Game loop
def game_loop(selected_map):
    global snake1_x, snake1_y, snake1_angle, snake1_health, snake1_ammo, snake1_reserve_ammo, snake1_reloading, snake1_reload_start, snake1_shield_on, snake1_last_shot
    global snake2_x, snake2_y, snake2_angle, snake2_health, snake2_ammo, snake2_reserve_ammo, snake2_reloading, snake2_reload_start, snake2_shield_on, snake2_last_shot
    global bullets, game_over

    reset_game()
    player1_gun = player2_gun = AK

    # Khởi tạo items
    heart = random_pos(heart_size)
    shield = random_pos(shield_size)
    bullets_item = random_pos(bullets_size)
    heart_active = shield_active = bullets_active = True
    snake1_shield_timer = snake2_shield_timer = 0
    heart_timer = bullets_timer = 0
    spawn_delay = 400

    while True:
        current_map_mask = map1_mask if selected_map == "map1" else map2_mask
        screen.blit(map1_background if selected_map == "map1" else map2_background, (0, 0))
        screen.blit(map1_img if selected_map == "map1" else map2_img, (0, 0))

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    main_menu()
                if event.key in (pygame.K_b, pygame.K_n, pygame.K_m):
                    player1_gun = {pygame.K_b: AK, pygame.K_n: SNIPER, pygame.K_m: SHOTGUN}[event.key]
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    player2_gun = {pygame.K_1: AK, pygame.K_2: SNIPER, pygame.K_3: SHOTGUN}[event.key]
                if event.key == pygame.K_l and not snake1_reloading and snake1_ammo[player1_gun] < max_ammo[player1_gun] and snake1_reserve_ammo[player1_gun] > 0:
                    snake1_reloading = True
                    snake1_reload_start = current_time
                if event.key == pygame.K_q and not snake2_reloading and snake2_ammo[player2_gun] < max_ammo[player2_gun] and snake2_reserve_ammo[player2_gun] > 0:
                    snake2_reloading = True
                    snake2_reload_start = current_time

        # Xử lý bắn đạn khi giữ phím cho Player 1
        if not game_over and not snake1_reloading and snake1_ammo[player1_gun] > 0:
            if keys[pygame.K_SPACE] and current_time - snake1_last_shot >= shoot_delays[player1_gun]:
                if player1_gun == AK:
                    bullets.append(Bullet(snake1_x, snake1_y, snake1_angle, speed=30, damage=damage_values[AK]))
                    snake1_ammo[player1_gun] -= 1
                elif player1_gun == SNIPER:
                    bullets.append(Bullet(snake1_x, snake1_y, snake1_angle, speed=100, damage=damage_values[SNIPER]))
                    snake1_ammo[player1_gun] -= 1
                elif player1_gun == SHOTGUN:
                    for _ in range(6):
                        bullets.append(Bullet(snake1_x, snake1_y, snake1_angle + random.randint(-10, 10), speed=20, damage=damage_values[SHOTGUN]))
                    snake1_ammo[player1_gun] -= 1
                snake1_last_shot = current_time

        # Xử lý bắn đạn khi giữ phím cho Player 2
        if not game_over and not snake2_reloading and snake2_ammo[player2_gun] > 0:
            if keys[pygame.K_j] and current_time - snake2_last_shot >= shoot_delays[player2_gun]:
                if player2_gun == AK:
                    bullets.append(Bullet(snake2_x, snake2_y, snake2_angle, speed=30, damage=damage_values[AK]))
                    snake2_ammo[player2_gun] -= 1
                elif player2_gun == SNIPER:
                    bullets.append(Bullet(snake2_x, snake2_y, snake2_angle, speed=100, damage=damage_values[SNIPER]))
                    snake2_ammo[player2_gun] -= 1
                elif player2_gun == SHOTGUN:
                    for _ in range(6):
                        bullets.append(Bullet(snake2_x, snake2_y, snake2_angle + random.randint(-10, 10), speed=20, damage=damage_values[SHOTGUN]))
                    snake2_ammo[player2_gun] -= 1
                snake2_last_shot = current_time

        # Xử lý nạp đạn
        if snake1_reloading and current_time - snake1_reload_start >= reload_times[player1_gun]:
            snake1_reloading = False
            ammo_needed = max_ammo[player1_gun] - snake1_ammo[player1_gun]
            ammo_to_take = min(ammo_needed, snake1_reserve_ammo[player1_gun])
            snake1_ammo[player1_gun] += ammo_to_take
            snake1_reserve_ammo[player1_gun] -= ammo_to_take

        if snake2_reloading and current_time - snake2_reload_start >= reload_times[player2_gun]:
            snake2_reloading = False
            ammo_needed = max_ammo[player2_gun] - snake2_ammo[player2_gun]
            ammo_to_take = min(ammo_needed, snake2_reserve_ammo[player2_gun])
            snake2_ammo[player2_gun] += ammo_to_take
            snake2_reserve_ammo[player2_gun] -= ammo_to_take

        # Điều khiển nhân vật
        if not game_over:
            if keys[pygame.K_LEFT]: snake1_angle += rotate_speed
            if keys[pygame.K_RIGHT]: snake1_angle -= rotate_speed
            if keys[pygame.K_UP]:
                move_vector = pygame.math.Vector2(step, 0).rotate(-snake1_angle)
                new_x = snake1_x + move_vector.x
                new_y = snake1_y + move_vector.y
                if not check_map_collision(new_x, new_y, current_map_mask):
                    snake1_x, snake1_y = new_x, new_y
            if keys[pygame.K_DOWN]:
                move_vector = pygame.math.Vector2(-step, 0).rotate(-snake1_angle)
                new_x = snake1_x + move_vector.x
                new_y = snake1_y + move_vector.y
                if not check_map_collision(new_x, new_y, current_map_mask):
                    snake1_x, snake1_y = new_x, new_y

            if keys[pygame.K_a]: snake2_angle += rotate_speed
            if keys[pygame.K_d]: snake2_angle -= rotate_speed
            if keys[pygame.K_w]:
                move_vector = pygame.math.Vector2(step, 0).rotate(-snake2_angle)
                new_x = snake2_x + move_vector.x
                new_y = snake2_y + move_vector.y
                if not check_map_collision(new_x, new_y, current_map_mask):
                    snake2_x, snake2_y = new_x, new_y
            if keys[pygame.K_s]:
                move_vector = pygame.math.Vector2(-step, 0).rotate(-snake2_angle)
                new_x = snake2_x + move_vector.x
                new_y = snake2_y + move_vector.y
                if not check_map_collision(new_x, new_y, current_map_mask):
                    snake2_x, snake2_y = new_x, new_y

        # Xử lý đạn
        for bullet in bullets[:]:
            bullet.update()
            if check_collision(bullet, snake1_x, snake1_y) and not snake1_shield_on:
                snake1_health -= bullet.damage
                bullets.remove(bullet)
            elif check_collision(bullet, snake2_x, snake2_y) and not snake2_shield_on:
                snake2_health -= bullet.damage
                bullets.remove(bullet)
            elif check_map_collision(bullet.x, bullet.y, current_map_mask):
                bullets.remove(bullet)
            else:
                bullet.draw(screen)

        # Xử lý va chạm với items
        snake1_rect = pygame.Rect(snake1_x - 22.5, snake1_y - 25, 45, 50)
        snake2_rect = pygame.Rect(snake2_x - 22.5, snake2_y - 25, 45, 50)

        if heart_active and (snake1_rect.colliderect(heart) or snake2_rect.colliderect(heart)):
            heart_active = False
            if snake1_rect.colliderect(heart):
                snake1_health = min(snake1_health + 30, 100)
                heart_timer = spawn_delay
            elif snake2_rect.colliderect(heart):
                snake2_health = min(snake2_health + 30, 100)
                heart_timer = spawn_delay

        if shield_active and (snake1_rect.colliderect(shield) or snake2_rect.colliderect(shield)):
            shield_active = False
            if snake1_rect.colliderect(shield):
                snake1_shield_on = True
                snake1_shield_timer = 300
            elif snake2_rect.colliderect(shield):
                snake2_shield_on = True
                snake2_shield_timer = 300

        if bullets_active and (snake1_rect.colliderect(bullets_item) or snake2_rect.colliderect(bullets_item)):
            bullets_active = False
            if snake1_rect.colliderect(bullets_item):
                snake1_reserve_ammo[AK] = reserve_ammo_max[AK]
                snake1_reserve_ammo[SNIPER] = reserve_ammo_max[SNIPER]
                snake1_reserve_ammo[SHOTGUN] = reserve_ammo_max[SHOTGUN]
                bullets_timer = spawn_delay
            elif snake2_rect.colliderect(bullets_item):
                snake2_reserve_ammo[AK] = reserve_ammo_max[AK]
                snake2_reserve_ammo[SNIPER] = reserve_ammo_max[SNIPER]
                snake2_reserve_ammo[SHOTGUN] = reserve_ammo_max[SHOTGUN]
                bullets_timer = spawn_delay

        # Cập nhật timer cho items
        if not heart_active:
            heart_timer -= 1
            if heart_timer <= 0:
                heart = random_pos(heart_size)
                heart_active = True
        if not shield_active:
            if snake1_shield_on:
                snake1_shield_timer -= 1
                if snake1_shield_timer <= 0:
                    snake1_shield_on = False
            if snake2_shield_on:
                snake2_shield_timer -= 1
                if snake2_shield_timer <= 0:
                    snake2_shield_on = False
            if not snake1_shield_on and not snake2_shield_on:
                shield = random_pos(shield_size)
                shield_active = True
        if not bullets_active:
            bullets_timer -= 1
            if bullets_timer <= 0:
                bullets_item = random_pos(bullets_size)
                bullets_active = True

        # Vẽ items
        if heart_active:
            screen.blit(heart_img, (heart.x, heart.y))
        if shield_active:
            screen.blit(shield_img, (shield.x, shield.y))
        if bullets_active:
            screen.blit(bullets_img, (bullets_item.x, bullets_item.y))

        # Hiệu ứng items
        if snake1_shield_on:
            pygame.draw.circle(screen, GREY, (int(snake1_x), int(snake1_y)), 60, 3)
        if snake2_shield_on:
            pygame.draw.circle(screen, GREY, (int(snake2_x), int(snake2_y)), 60, 3)

        # Vẽ thanh máu, đạn và nhân vật
        pygame.draw.rect(screen, RED, (50, 50, 200, 20))
        pygame.draw.rect(screen, GREEN, (50, 50, 2 * max(snake2_health, 0), 20))
        draw_text("Player 2", 50, 25)
        draw_text(f"Ammo: {snake2_ammo[player2_gun]}/{snake2_reserve_ammo[player2_gun]}", 50, 75)
        if snake2_reloading:
            draw_text("Reloading...", 50, 100, 20, RED)

        pygame.draw.rect(screen, RED, (1250, 50, 200, 20))
        pygame.draw.rect(screen, GREEN, (1250, 50, 2 * max(snake1_health, 0), 20))
        draw_text("Player 1", 1260, 25)
        draw_text(f"Ammo: {snake1_ammo[player1_gun]}/{snake1_reserve_ammo[player1_gun]}", 1250, 75)
        if snake1_reloading:
            draw_text("Reloading...", 1250, 100, 20, RED)

        # Chọn hình ảnh nhân vật dựa trên loại súng
        if player1_gun == AK:
            snake1_img = snake1_ak_img
        elif player1_gun == SNIPER:
            snake1_img = snake1_sniper_img
        elif player1_gun == SHOTGUN:
            snake1_img = snake1_shotgun_img

        if player2_gun == AK:
            snake2_img = snake2_ak_img
        elif player2_gun == SNIPER:
            snake2_img = snake2_sniper_img
        elif player2_gun == SHOTGUN:
            snake2_img = snake2_shotgun_img

        rotated_snake1_img = pygame.transform.rotate(snake1_img, snake1_angle)
        rotated_snake2_img = pygame.transform.rotate(snake2_img, snake2_angle)
        screen.blit(rotated_snake1_img, rotated_snake1_img.get_rect(center=(snake1_x, snake1_y)).topleft)
        screen.blit(rotated_snake2_img, rotated_snake2_img.get_rect(center=(snake2_x, snake2_y)).topleft)

        # Kiểm tra game over
        if snake1_health <= 0 or snake2_health <= 0:
            game_over = True
            winner = "Player 2 win!" if snake1_health <= 0 else "Player 1 win!"
            draw_text(winner, WIDTH // 2 - 100, HEIGHT // 2 - 100, 50, RED)
            draw_text("Press R to restart", WIDTH // 2 - 100, HEIGHT // 2 - 50)

        pygame.display.update()
        clock.tick(500)

# Menu chính
def main_menu():
    menu_items = ["1 Player(Not avaible now)", "2 Players", "Quit"]
    state = "main_menu"
    selected_item = None
    map_preview_size = (600, 450)
    map1_preview = pygame.transform.scale(map1_img, map_preview_size) if map1_img else None
    map1bg_preview = pygame.transform.scale(map1_background, map_preview_size) if map1_background else None
    map2_preview = pygame.transform.scale(map2_img, map_preview_size) if map2_img else None
    map2bg_preview = pygame.transform.scale(map2_background, map_preview_size) if map2_background else None

    while True:
        screen.fill(WHITE)
        screen.blit(title_img, (200, -60))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        selected_item = None

        if state == "main_menu":
            for i, text in enumerate(menu_items):
                label = font.render(text, True, BLACK)
                x = WIDTH // 2 - label.get_width() // 2
                y = 200 + i * 60 + 300
                rect = label.get_rect(topleft=(x, y))
                if rect.collidepoint(mouse_x, mouse_y):
                    selected_item = i
                    pygame.draw.rect(screen, RED, rect, 3)
                screen.blit(label, (x, y))

        elif state == "map_selection":
            draw_text("Select Map", WIDTH // 2 - 70, 50, 50)
            if map1_preview:
                map1_rect = map1_preview.get_rect(topleft=(WIDTH // 4 - 300, 150))
                map1bg_rect = map1bg_preview.get_rect(topleft=(WIDTH // 4 - 300, 150))
                screen.blit(map1bg_preview, map1bg_rect)
                screen.blit(map1_preview, map1_rect)
                if map1_rect.collidepoint(mouse_x, mouse_y):
                    selected_item = "map1"
                    pygame.draw.rect(screen, RED, map1_rect, 3)
            if map2_preview:
                map2_rect = map2_preview.get_rect(topleft=(3 * WIDTH // 4 - 300, 150))
                map2bg_rect = map2bg_preview.get_rect(topleft=(3 * WIDTH // 4 - 300, 150))
                screen.blit(map2bg_preview, map2bg_rect)
                screen.blit(map2_preview, map2_rect)
                if map2_rect.collidepoint(mouse_x, mouse_y):
                    selected_item = "map2"
                    pygame.draw.rect(screen, RED, map2_rect, 3)
            back_label = font.render("Back", True, BLACK)
            back_rect = back_label.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(back_label, back_rect)
            if back_rect.collidepoint(mouse_x, mouse_y):
                selected_item = "back"
                pygame.draw.rect(screen, RED, back_rect, 3)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and selected_item is not None:
                if state == "main_menu":
                    if selected_item in (0, 1):
                        state = "map_selection"
                    elif selected_item == 2:
                        pygame.quit()
                        exit()
                elif state == "map_selection":
                    if selected_item in ("map1", "map2"):
                        game_loop(selected_item)
                    elif selected_item == "back":
                        state = "main_menu"

if __name__ == "__main__":
    main_menu()