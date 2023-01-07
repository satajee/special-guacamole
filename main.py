import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

# поплачь блядота

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            screen.blit(snail_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True



pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('AHAHAHAHAHAHAHA')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)  # place your font here
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('images/sky.png').convert_alpha()
ground_surface = pygame.image.load('images/ground.png').convert_alpha()

# obstacles
obstacle_rect_list = []
snail_surface = pygame.image.load('images/snail.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 340))
snail_x_pos = 600

player_surf = pygame.image.load('images/player_static.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 340))

player_gravity = 0

# intro screen

player_stand = pygame.image.load('images/player_static.png').convert_alpha()
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Runner game', False, 'White')
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to run', False, 'White')
game_message_rect = game_message.get_rect(center=(400, 320))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            # exit from sys not to get an error of video initializing

        if game_active:
            if player_rect.bottom == 335:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos):
                        player_gravity = -20

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 340)))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 0))
        # pygame.draw.rect(screen, 'Black', score_rect)
        # screen.blit(score_surf, score_rect)
        screen.blit(player_surf, player_rect)
        score = display_score()

        # because while we are in our main loop, every second here the main event is updating.

        # snail
        # snail_rect.left -= 5
        # if snail_rect.right <= -0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 335: player_rect.bottom = 335
        screen.blit(player_surf, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        game_active = collisions(player_rect, obstacle_rect_list)


    else:
        screen.fill('Violet')
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_gravity = 0
        player_rect.bottom = 335

        score_message = test_font.render(f'Your score: {score}', False, 'White')
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # update everything and forget about it forever...
    pygame.display.update()
    clock.tick(60)
