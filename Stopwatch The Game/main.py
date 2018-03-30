import simplegui

message = '0:00.0'
minute = int(0)
seconds = float(0.0)
interval = 100
game_win = 0
game_stop = 0


def format():
    global message
    global minute, seconds
    if(seconds >= 10.0):
        message = str(minute) + ':' + str(seconds)
    else:
        message = str(minute) + ':0' + str(seconds)


def draw(canvas):
    game = str(game_win) + "/" + str(game_stop)
    canvas.draw_text(message, [60, 100], 30, 'White')
    canvas.draw_text(game, [120, 30], 30, "Red")


def tick():
    global minute, seconds
    if seconds < 60.0:
        seconds += 0.1
    else:
        seconds = 0.0
        minute += 1
    format()


def is_win():
    global game_stop, game_win

#    second = seconds * 10

#    print(seconds,second,second % 50)
    if (seconds % 5) < 0.001:
        game_stop += 1
        game_win += 1
    else:
        game_stop += 1


def start():
    timer.start()


def stop():
    timer.stop()
    is_win()


def reset():
    global message
    global game_stop, game_win
    timer.stop()
    message = '0:00.0'
    game_stop = 0
    game_win = 0


frame = simplegui.create_frame('stopwatch:the game', 200, 200)

frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)
frame.add_button('start', start, 100)
frame.add_button('stop', stop, 100)
frame.add_button('reset', reset, 100)

frame.start()
