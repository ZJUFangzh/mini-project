# http://py3.codeskulptor.org

import simplegui
import random

secret_number = -1  # 被猜测数
allowed_guesses = -1  # 允许次数
last_time_range = -1  # 当前所选范围
last_time_allowed_guess = -1  # 保存当前局允许次数


def new_game(number_range):
    random_number = random.randrange(0, number_range, 1)
    return random_number


def compare_number(input_number):
    global secret_number
    global allowed_guesses
    if (secret_number > input_number):
        result = 'Higher!'
        allowed_guesses -= 1
    elif (secret_number < input_number):
        result = 'Lower!'
        allowed_guesses -= 1
    else:
        result = 'Correct!'
    return result


def choice_100():

    global last_time_range
    global secret_number
    global allowed_guesses
    global last_time_allowed_guess
    last_time_range = 100
    secret_number = new_game(100)

    print('The secret number has been set! (range: 0~100) ')
    allowed_guesses = 7
    last_time_allowed_guess = 7


def choice_1000():

    global last_time_range
    global secret_number
    global allowed_guesses
    global last_time_allowed_guess
    last_time_range = 1000
    secret_number = new_game(1000)

    print('The secret number has been set! (range: 0~1000) ')
    allowed_guesses = 7
    last_time_allowed_guess = 7


def input_guess(guess):
    global last_time_range
    global secret_number
    global allowed_guesses
    global last_time_allowed_guess

    if (secret_number == -1):  # 初次进入游戏时，应检测是否选择范围
        print("The secret number hasn't been set, please choose a button to set the secret number.")

    elif (guess.isdigit() == False):
        print('please input a valid number')
    elif (int(guess) < 0) or (int(guess) >= last_time_range):
        print('out of range')
    else:
        input_number = int(guess)
        result = compare_number(input_number)
    if (result == "Correct!"):
        print("The number you guess is: " + guess + ", " + result +
              "\n\n" + "You win! A new game in the same range is start...")
        secret_number = new_game(last_time_range)  # 以当前范围为下一局游戏范围
    elif (allowed_guesses != 0):
        print("The number you guess is: " + guess + ", " + result +
              "\n" + str(allowed_guesses) + " chances left.")
    else:
        print("The number you guess is: " + guess + ", " + result +
              "\n\n" + "You lost. A new game in the same range is start...")
        allowed_guesses = last_time_allowed_guess
        secret_number = new_game(last_time_range)


frame = simplegui.create_frame("Guess the number!", 200, 200)
frame.add_button('Range is 0_100', choice_100, 200)

frame.add_button('Range is 0_1000', choice_1000, 200)

frame.add_input('enter a guess', input_guess, 200)

frame.start()
