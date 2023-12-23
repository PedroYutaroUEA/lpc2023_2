import pygame
import random

from consts import (
    COLOR_BLACK,
    COLOR_WHITE,
    PADDLE_HEIGHT,
    VH,
    VW
)

# game settings
size = (VW, VH)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MyPong - PyGame Edition - 2022-12-12")
game_clock = pygame.time.Clock()

# score text
score_font = pygame.font.Font('assets/PressStart2P.ttf', 44)
score_text = score_font.render('00 x 00', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect = score_text.get_rect(center=(680, 50))

# victory text
victory_font = pygame.font.Font('assets/PressStart2P.ttf', 50)
victory_text_rect = score_text.get_rect(center=(400, 350))

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('assets/258020__kodack__arcade-bleep-sound.wav')

# players
player_1 = {"image": pygame.image.load("assets/player.png"), "y": 300, "move_up": False, "move_down": False}
player_2 = {"image": pygame.image.load("assets/player.png"), "y": 300}

# ball
ball = {
    "image": pygame.image.load("assets/ball.png"),
    "x": VW / 2,
    "y": VH / 2,
    "d_x": random.choice([6, -6]),
    "d_y": random.choice([6, -6])
}

# functions
def update_screen():
    pygame.display.flip()
    game_clock.tick(60)


def draw_objects():
    screen.blit(ball["image"], (ball["x"], ball["y"]))
    screen.blit(player_1["image"], (50, player_1["y"]))
    screen.blit(player_2["image"], (1180, player_2["y"]))
    screen.blit(score_font.render(
        f"{score_1} x {score_2}", True, COLOR_WHITE, COLOR_BLACK),
        score_text_rect
    )


def reset_ball():
    ball["x"] = VW / 2
    ball["y"] = random.uniform(50, VH - 50)
    ball["d_x"] = random.choice([6, -6])
    ball["d_y"] = random.choice([6, -6])


def scoring_points():
    if ball["x"] < -50:
        scoring_sound_effect.play()
        reset_ball()
        return 2
    elif ball["x"] > VW + 50:
        scoring_sound_effect.play()
        reset_ball()
        return 1
    return 0


def ball_collision_with_wall():
    if ball["y"] > 700 or ball["y"] <= 0:
        ball["d_y"] *= -1
        bounce_sound_effect.play()
        return True
    return False


def check_wall_collision(player):
    if player["y"] <= 0:
        player["y"] = 0
    elif player["y"] >= VH - PADDLE_HEIGHT:
        player["y"] = VH - PADDLE_HEIGHT


def ball_collision_with_paddle(player, acc_x):
    if player["y"] < ball["y"] + 25:
        if player["y"] + PADDLE_HEIGHT > ball["y"]:
            bounce_sound_effect.play()
            ball["d_y"] = random.choice([6, 7, 8, 9, -6, -7, -8, -9])
            if not acc_x:
                ball["d_x"] *= -1.05
            else:
                ball["d_x"] *= -1


def ball_collision_with_paddle_corner(player):
    if player["y"] < ball["y"] + 25:
        if player["y"] + PADDLE_HEIGHT > ball["y"]:
            ball["d_y"] *= -1
            bounce_sound_effect.play()
            return True
    return False

# ball conditionals
punched_corner = False
accelerated_x = False

# game loop
score_1, score_2 = 0, 0
game_loop = True

