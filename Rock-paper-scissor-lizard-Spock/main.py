import random


def compare_num(player, computer):
    diff = player - computer
    if (diff > 2):
        player -= 5
    elif (diff < -2):
        player += 5
    if player > computer:
        winner = 'player'
    elif player < computer:

        winner = 'computer'
    else:
        winner = 'nobody'
    print(winner + ' wins!')


def compare_num_v2(player, computer):
    diff = player - computer
    diff = diff % 5
    if (diff == 1) or (diff == 2):
        winner = 'player'
    elif (diff == 3) or (diff == 4):
        winner = 'computer'
    else:
        winner = 'nobody'
    print(winner + ' wins!')


while True:
    print('please input the number you want:')
    print('''0 — rock
1 — Spock
2 — paper
3 — lizard
4 — scissors''')
    player = int(input())

    if player == -1:
        break

    computer = random.randint(0, 4)

    compare_num_v2(player, computer)
