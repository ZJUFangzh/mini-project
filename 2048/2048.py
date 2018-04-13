import random
from random import randrange
import msvcrt
import os
# os.system('cls')
# v[:] = map(list, zip(*v[::-1]))

v = [[0 for i in range(4)] for i in range(4)]


actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions_dict = dict(zip(letter_codes, actions * 2))


# 获得键盘输入
def get_action():
    char = 'N'
    while char not in actions_dict:
        char = ord(msvcrt.getch())
    return actions_dict[char]

# 开始的输入


def init():
    global v
    v = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        v[i] = [random.choice([0, 0, 0, 2, 2, 4]) for x in v[i]]
    display()
    return 'Game'


def is_zero(s):
    if s == 0:
        return ''
    else:
        return s


# 显示窗口

def display():
    os.system('cls')
    for i in range(4):
        print('|{:^4}|{:^4}|{:^4}|{:^4}|'.format(
            is_zero(v[i][0]), is_zero(v[i][1]), is_zero(v[i][2]), is_zero(v[i][3])))
        print('-' * 21)
    print('score:')


def creat_random_num():
    new_num = 4 if randrange(101) > 80 else 2
    try:
        (i, j) = random.choice([(i, j) for i in range(4)
                                for j in range(4) if v[i][j] == 0])
        v[i][j] = new_num
    except:
        pass


def move(action, matrix):
    def move_left():

        def remove_zero():
            for i in range(4):
                lis = []
                for j in range(4):
                    if matrix[i][j] != 0:
                        lis.append(matrix[i][j])
                lis += [0 for i in range(4 - len(lis))]
                matrix[i] = list(lis)
# 合并

        def merge():
            for i in range(4):
                for j in range(3):
                    if matrix[i][j] == matrix[i][j + 1]:
                        matrix[i][j] *= 2
                        matrix[i][j + 1] = 0
                        continue
        remove_zero()
        merge()
        remove_zero()

    def rotate_90(str):
        if str == 'turn_r':
            matrix[:] = map(list, zip(*matrix[::-1]))
        elif str == 'turn_l':
            matrix[:] = map(list, list(zip(*matrix))[::-1])

    def move_down():
        rotate_90('turn_r')
        move_left()
        rotate_90('turn_l')

    def move_up():
        rotate_90('turn_l')
        move_left()
        rotate_90('turn_r')

    def move_right():
        rotate_90('turn_l')
        rotate_90('turn_l')
        move_left()
        rotate_90('turn_r')
        rotate_90('turn_r')

    if action == 'Left':
        move_left()
    elif action == 'Right':
        move_right()
    elif action == 'Up':
        move_up()
    elif action == 'Down':
        move_down()
    else:
        pass


def game():
    action = get_action()
    if action == 'Restart':
        return 'Init'
    if action == 'Exit':
        return 'Exit'
    else:
        if not is_gameover():
            return 'Gameover'
        move(action, v)
        creat_random_num()
        display()

        return 'Game'


def is_gameover():

    if check('Left'):
        return True
    elif check('Right'):
        return True
    elif check('Up'):
        return True
    elif check('Down'):
        return True
    else:
        return False


def check(action):
    v_t = list(v)
    move(action, v_t)
    if v_t == v:
        return False
    else:
        return True


def gameover():
    print('Gameover! R or E')
    action = get_action()
    if action == 'Restart':
        return 'Init'
    if action == 'Exit':
        return 'Exit'
    else:
        return 'Gameover'


state_actions = {
    'Init': init,
    'Game': game,
    'Gameover': gameover

}

# move('Right', v)
# move('Up', v)
# display()
state = 'Init'
while state != 'Exit':
    state = state_actions[state]()
