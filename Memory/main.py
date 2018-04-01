import simplegui
import random


def new_game():
    global list_2, exposed, t, state
    state = 0
    t = 0
    list_1 = list(range(0, 8))
    list_2 = list_1 * 2
    random.shuffle(list_2)
    label.set_text("Turns = " + str(t))
    exposed = [False] * 16


def mouseclick(pos):
    global t, state, click1, click2
    choice = pos[0] // 50
    if state == 0:
        state = 1
        click1 = choice
        exposed[click1] = True
    elif state == 1:
        state = 2
        click2 = choice
        exposed[click2] = True
    elif state == 2:
        if not exposed[choice]:
            state = 1
            if not list_2[click1] == list_2[click2]:
                exposed[click1] = exposed[click2] = False
            click1 = choice
            exposed[click1] = True
            t += 1
    label.set_text("Turns = " + str(t))


def draw(canvas):
    global exposed
    for i in range(16):
        if exposed[i]:
            canvas.draw_polygon([(50 * i, 0), (50 * i + 50, 0),
                                 (50 * i + 50, 100), (50 * i, 100)], 3, "White", 'Gray')
            canvas.draw_text(str(list_2[i]), (50 * i + 20, 60), 30, "White")
        else:
            canvas.draw_polygon([(50 * i, 0), (50 * i + 50, 0),
                                 (50 * i + 50, 100), (50 * i, 100)], 3, 'White', 'Green')


frame = simplegui.create_frame('Memory', 800, 100)
frame.add_button('Restart', new_game)
label = frame.add_label('Turns = 0')

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()
