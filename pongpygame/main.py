import pygame
import random

pygame.init()

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

MAX_SCORE = 10
# view height/width screen
VW = 1280
VH = 720
size = (VW, VH)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MyPong - PyGame Edition - 2022-12-12")

# score text
score_font = pygame.font.Font('assets/PressStart2P.ttf', 44)
score_text = score_font.render('00 x 00', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect = score_text.get_rect()
score_text_rect.center = (680, 50)

# victory text
victory_font = pygame.font.Font('assets/PressStart2P.ttf', 100)
victory_text = victory_font.render('VICTORY', True, COLOR_WHITE, COLOR_BLACK)
victory_text_rect = score_text.get_rect()
victory_text_rect.center = (450, 350)

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')

# paddle's layout
PADDLE_HEIGHT = 150
paddle_image = pygame.image.load("assets/player.png")

# player 1
player_1 = paddle_image
player_1_y = 300  # paddle position
player_1_move_up = False
player_1_move_down = False

# player 2 - robot
player_2 = paddle_image
player_2_y = 300  # paddle position

# ball
ball = pygame.image.load("assets/ball.png")
ball_x = VW / 2  # ball position vw
ball_y = VH / 2  # ball position vh
ball_dx = random.choice([6, -6])
ball_dy = random.choice([6, -6])
punched_corner = False
accelerated_x = False

# score
score_1 = 0
score_2 = 0

# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        #  keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1_move_up = True
            if event.key == pygame.K_DOWN:
                player_1_move_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_1_move_up = False
            if event.key == pygame.K_DOWN:
                player_1_move_down = False

    # checking the victory condition
    if score_1 < MAX_SCORE and score_2 < MAX_SCORE:
        # clear screen
        screen.fill(COLOR_BLACK)

        # ball collision with the wall
        if ball_y > 700 or ball_y <= 0:
            ball_dy *= -1
            bounce_sound_effect.play()
            # updates punched corner stats
            punched_corner = False

        # ball collision with the player 1 's paddle
        if ball_x < 100:
            if ball_x > 90:
                if player_1_y < ball_y + 25:
                    if player_1_y + PADDLE_HEIGHT > ball_y:
                        if not accelerated_x:
                            ball_dx *= random.choice([-1, -1.5, -2])
                            accelerated_x = True
                        else:
                            ball_dx *= -1
                        ball_dy = random.choice([6, 7, 8, -6, -7, -8])
                        bounce_sound_effect.play()
            # if ball punches the corner
            elif not punched_corner:
                if player_1_y < ball_y + 25:
                    if player_1_y + PADDLE_HEIGHT > ball_y:
                        ball_dy *= -1
                        bounce_sound_effect.play()
                        punched_corner = True

        # ball collision with the player 2's paddle
        if ball_x > 1160:
            if ball_x < 1170:
                if player_2_y < ball_y + 25:
                    if player_2_y + PADDLE_HEIGHT > ball_y:
                        if not accelerated_x:
                            ball_dx *= random.choice([-1, -1.5, -2])
                            accelerated_x = True
                        else:
                            ball_dx *= -1
                        ball_dy = random.choice([6, 7, 8, -6, -7, -8])
                        bounce_sound_effect.play()
            # if ball punches the corner
            elif not punched_corner:
                if player_2_y < ball_y + 25:
                    if player_2_y + PADDLE_HEIGHT > ball_y:
                        ball_dy *= -1
                        bounce_sound_effect.play()
                        punched_corner = True

        # scoring points
        if ball_x < -50:
            scoring_sound_effect.play()
            ball_x = VW / 2
            ball_y = random.uniform(50, VH - 50)
            ball_dx = random.choice([6, -6])
            ball_dy = random.choice([6, -6])
            accelerated_x = False
            score_2 += 1

        elif ball_x > VW + 50:
            scoring_sound_effect.play()
            ball_x = VW / 2
            ball_y = random.uniform(50, VH - 50)
            ball_dx = random.choice([6, -6])
            ball_dy = random.choice([6, -6])
            accelerated_x = False
            score_1 += 1

        # ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # player 1 movement
        if player_1_move_up and player_1_y > 0:
            player_1_y -= 10
        elif player_1_move_down and player_1_y < VH - PADDLE_HEIGHT:
            player_1_y += 10

        # player 1 wall collision
        if player_1_y <= 0:
            player_1_y = 0
        elif player_1_y >= 570:
            player_1_y = 570

        # player 2 "Artificial Intelligence"
        if ball_x > VW / 2:
            # making AI unpredictable
            target_y = ball_y + random.randint(-20, 20)
            if player_2_y + PADDLE_HEIGHT / 2 < target_y and player_2_y < VH - PADDLE_HEIGHT:
                player_2_y += random.uniform(4, 7)
            elif player_2_y + PADDLE_HEIGHT / 2 > target_y and player_2_y > 0:
                player_2_y -= random.uniform(4, 7)

        # update score hud
        score_text = score_font.render(str(score_1) + ' x ' + str(score_2), True, COLOR_WHITE, COLOR_BLACK)

        # drawing objects
        screen.blit(ball, (ball_x, ball_y))
        screen.blit(player_1, (50, player_1_y))
        screen.blit(player_2, (1180, player_2_y))
        screen.blit(score_text, score_text_rect)
    else:
        # drawing victory
        screen.fill(COLOR_BLACK)
        screen.blit(score_text, score_text_rect)
        screen.blit(victory_text, victory_text_rect)

    # update screen
    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()
