import pygame
import random
from consts import MAX_SCORE
from objects import (
    draw_objects,
    reset_ball,
    scoring_points,
    ball_collision_with_wall,
    check_wall_collision,
    ball_collision_with_paddle,
    ball_collision_with_paddle_corner,
)