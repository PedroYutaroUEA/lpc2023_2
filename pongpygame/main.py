import pygame
import random
punched_corner = False
pygame.init()

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

SCORE_MAX = 10
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

# player 1
player_1 = pygame.image.load("assets/player.png")
player_1_y = 300
player_1_move_up = False
player_1_move_down = False

# player 2 - AI
player_2 = pygame.image.load("assets/player.png")
player_2_y = 300

# ball
ball = pygame.image.load("assets/ball.png")
ball_x = VW / 2
ball_y = VH / 2
ball_dx = 5
ball_dy = 5

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
        # keystroke events
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

    # checking victory condition
    if score_1 < SCORE_MAX and score_2 < SCORE_MAX:
        screen.fill(COLOR_BLACK)

        # ball collision with the wall
        if ball_y >= VH - 20 or ball_y <= 0:
            ball_dy *= -1
            bounce_sound_effect.play()

        # ball collision with player 1
        if ball_x < 100:
            if ball_x > 90:
                # ball touches the paddle
                if player_1_y < ball_y + (ball_dx * ball_dy):
                    if player_1_y + PADDLE_HEIGHT > ball_y:
                        ball_dx *= -1
                    bounce_sound_effect.play()
            elif not punched_corner:
                if player_1_y < ball_y + (ball_dx * ball_dy):
                    if player_1_y + PADDLE_HEIGHT > ball_y:
                        ball_dy *= -1
                    bounce_sound_effect.play()
                    punched_corner = True

        # ball collision with player 2
        elif ball_x > 1160 and player_2_y < ball_y < player_2_y + PADDLE_HEIGHT:
            ball_dx *= -1
            bounce_sound_effect.play()

        # scoring points
        if ball_x < -50:
            ball_x = VW / 2
            ball_y = random.uniform(50, VH - 50)
            ball_dy = random.choice([6.5, -6.5])
            ball_dx *= -1
            score_2 += 1
            scoring_sound_effect.play()

        elif ball_x > VW + 50:
            ball_x = VW / 2
            ball_y = random.uniform(50, VH - 50)
            ball_dy = random.choice([6.5, -6.5])
            ball_dx *= -1
            score_1 += 1
            scoring_sound_effect.play()

        # ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # player 1 movement
        if player_1_move_up and player_1_y > 0:
            player_1_y -= 5.5
        elif player_1_move_down and player_1_y < VH - PADDLE_HEIGHT:
            player_1_y += 5.5

        # player 1 collides with upper wall
        if player_1_y <= 0:
            player_1_y = 0

        # player 1 collides with lower wall
        elif player_1_y >= 570:
            player_1_y = 570

        if ball_x > VW / 2:
            # making AI unpredictable
            target_y = ball_y + random.randint(-20, 20)
            if player_2_y + PADDLE_HEIGHT / 2 < target_y and player_2_y < VH - PADDLE_HEIGHT:
                player_2_y += random.uniform(3, 5)
            elif player_2_y + PADDLE_HEIGHT / 2 > target_y and player_2_y > 0:
                player_2_y -= random.uniform(3, 5)
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
