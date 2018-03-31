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
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
delta_paddle_v = 2
score1 = 0
score2 = 0


def is_inrange(paddle_pos, paddle_vel):
    if (paddle_pos[1] < 0):  # paddle1
        paddle_pos[1] = 0
    elif (paddle_pos[1] > 340):
        paddle_pos[1] = 340
    else:
        paddle_pos[1] += paddle_vel[1]


def new_game():
	global p
	p = [WIDTH / 2, HEIGHT / 2]
    v[0] = random.randint(-10, 10)
    v[1] = random.randint(-10, 10)

def score(posision):

	posision += 1
	new_game()

def restart():
	global score1,score2
	score2 = 0
	score1 = 0
	new_game()


def draw(canvas):

    p[0] += v[0]
    p[1] += v[1]

    is_inrange(paddle1_pos, paddle1_vel)
    is_inrange(paddle2_pos, paddle2_vel)
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

    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] -= delta_paddle_v
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] += delta_paddle_v
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] += delta_paddle_v
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] -= delta_paddle_v


def keyup(key):

    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0


frame = simplegui.create_frame('Pong', WIDTH, HEIGHT)

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('restart',restart,20)
frame.start()
