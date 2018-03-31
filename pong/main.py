import simplegui
import random


WIDTH = 600
HEIGHT = 400
r = 20
p = [WIDTH / 2, HEIGHT / 2]
v = [0, 0]
delta_v = 2
paddle_width = 10
paddle_height = 60
paddle1_pos = [paddle_width / 2, HEIGHT / 2 - paddle_height / 2]
paddle2_pos = [WIDTH - paddle_width / 2, HEIGHT / 2 - paddle_height / 2]


def draw(canvas):
    p[0] += v[0]
    p[1] += v[1]
    if(p[0] <= r):
        v[0] = -v[0]
    elif(p[0] >= WIDTH - r):
        v[0] = -v[0]
    elif(p[1] <= r):
        v[1] = -v[1]
    elif(p[1] >= HEIGHT - r):
        v[1] = -v[1]
    canvas.draw_circle(p, r, 2, "Red", 'White')
    canvas.draw_line([paddle_width, 0], [paddle_width, HEIGHT], 2, 'White')
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 2, 'White')
    canvas.draw_line([WIDTH - paddle_width, 0],
                     [WIDTH - paddle_width, HEIGHT], 2, 'White')
    canvas.draw_line(
        paddle1_pos, [paddle1_pos[0], paddle1_pos[1] + paddle_height], 10, 'White')
    canvas.draw_line(
        paddle2_pos, [paddle2_pos[0], paddle2_pos[1] + paddle_height], 10, 'White')


def keydown(key):

    if key == simplegui.KEY_MAP['left']:
        v[0] -= delta_v
    elif key == simplegui.KEY_MAP['right']:
        v[0] += delta_v
    elif key == simplegui.KEY_MAP['down']:
        v[1] += delta_v
    elif key == simplegui.KEY_MAP['up']:
        v[1] -= delta_v


def keyup(key):

    if key == simplegui.KEY_MAP['left']:
        v[0] += delta_v
    elif key == simplegui.KEY_MAP['right']:
        v[0] -= delta_v
    elif key == simplegui.KEY_MAP['down']:
        v[1] -= delta_v
    elif key == simplegui.KEY_MAP['up']:
        v[1] += delta_v


frame = simplegui.create_frame('Pong', WIDTH, HEIGHT)

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.start()
