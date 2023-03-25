import pygame
from pygame.constants import QUIT, K_w, K_s, K_d, K_a
from random import randint, choice


pygame.init()

FPS = pygame.time.Clock()

width = 800
heigth = 600
screen = width, heigth

FACK = 155,155,155
RED = 255, 0, 0
RUBY = 125, 0, 0
GREEN = 0, 155, 50
YELLOW = 255, 255, 0
GOLDEN = 255, 215, 0
PURPLE = 100, 50, 200


def rand_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))


main_wind = pygame.display.set_mode(screen)

ball = pygame.Surface((25, 25))
ball.fill(rand_color())
ball_rect = ball.get_rect()
ball_speed = 5.0
ball_hp = 100
score = 0


def create_enemy():
    enemy_type = [{"name": "loh", "hp": 10, "color": RED, "size": (15, 15), "speed": 4.0, "damage": 10, "punch": 20}, 
                {"name": "tank", "hp": 25, "color": RUBY, "size": (20, 20), "speed": 2.0, "damage": 25, "punch": 30}]
    
    enemy_stats = choice(enemy_type)
    enemy = pygame.Surface(enemy_stats["size"])
    enemy.fill(enemy_stats["color"])
    enemy_rect = pygame.Rect(width, randint(0, heigth), *enemy.get_size())
    return [enemy, enemy_rect, enemy_stats]


def create_bonus():
    bonus_type = [{"name": "heal", "color": GREEN, "size": (16, 16), "speed": 4.0, "exp": 0, "damage": 25},
                  {"name": "xp", "color": YELLOW, "size": (10, 10), "speed": 4.0, "exp": 15, "damage": 0}, 
                    {"name": "xp", "color": GOLDEN, "size": (14, 14), "speed": 4.0, "exp": 30, "damage": 0}]
    
    bonus_stats = choice(bonus_type)
    bonus = pygame.Surface(bonus_stats["size"])
    bonus.fill(bonus_stats["color"])
    bonus_rect = pygame.Rect(randint(0, width), 0, *bonus.get_size())
    return [bonus, bonus_rect, bonus_stats]


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, color, x, y, size):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

enemys = []
bonuses = []

is_working = True


while is_working:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY and len(enemys) < 20:
            enemys.append(create_enemy()) 

        if event.type == CREATE_BONUS and len(bonuses) < 5:
            bonuses.append(create_bonus()) 

    main_wind.fill(FACK)
    main_wind.blit(ball, ball_rect)

    for enemy in enemys:
        main_wind.blit(enemy[0], enemy[1])
        enemy[1] = enemy[1].move(-enemy[2]["speed"], 0)

        if enemy[1].right <= 0:
            enemys.remove(enemy)

        if ball_rect.colliderect(enemy[1]):
            if ball_rect.x < enemy[1].x and ball_rect.y < enemy[1].y:
                # столкновение с левой верхней стороны
                ball_rect = ball_rect.move(-enemy[2]["punch"], -enemy[2]["punch"])

            elif ball_rect.x < enemy[1].x and ball_rect.y > enemy[1].y:
                # столкновение с левой нижней стороны
                ball_rect = ball_rect.move(-enemy[2]["punch"], enemy[2]["punch"])

            elif ball_rect.x > enemy[1].x and ball_rect.y < enemy[1].y:
                # столкновение с правой верхней стороны
                ball_rect = ball_rect.move(enemy[2]["punch"], -enemy[2]["punch"])

            elif ball_rect.x > enemy[1].x and ball_rect.y > enemy[1].y:
                # столкновение с правой нижней стороны
                ball_rect = ball_rect.move(-enemy[2]["punch"], enemy[2]["punch"])
            
            ball_hp -= enemy[2]["damage"]


    for bonus in bonuses:
        main_wind.blit(bonus[0], bonus[1])
        bonus[1] = bonus[1].move(0, bonus[2]["speed"])

        if bonus[1].top >= heigth:
            bonuses.remove(bonus)

        if ball_rect.colliderect(bonus[1]):

            if ball_hp + bonus[2]["damage"] > 100: 
                ball_hp = 100
            else:
                ball_hp += bonus[2]["damage"]

            score += bonus[2]["exp"]
            bonuses.remove(bonus)

    draw_text(main_wind, f"HP: {int(ball_hp)}", PURPLE, 75, 5, 18)
    draw_text(main_wind, f"Score: {score}", PURPLE, 200, 5, 18)

    if ball_hp <= 0:
        draw_text(main_wind, f"GAME OWER", RED, 400, 260, 40)

    pressed_key = pygame.key.get_pressed()

    if pressed_key[K_w] and ball_rect.top >= 10 and ball_hp > 0:
        ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_key[K_s] and ball_rect.bottom <= heigth - 10 and ball_hp > 0:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_key[K_d] and ball_rect.right <= width - 10 and ball_hp > 0:
        ball_rect = ball_rect.move(ball_speed, 0)

    if pressed_key[K_a] and ball_rect.left >= 10 and ball_hp > 0:
        ball_rect = ball_rect.move(-ball_speed, 0)
        
    pygame.display.flip()