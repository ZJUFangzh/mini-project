import simplegui
import random

CARD_SIZE = (72, 96)
CARD_CENTR = (36, 48)
card_images = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
          '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


outcome = []
score = []
deck = None
dealer = None
players = []
player_num = 1
current_player = -1
max_player = 3
count = 0
message = 'New Game ?'
round_num = 0


class Card(object):
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print('Invalid card:', suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = ((CARD_CENTR[0] + CARD_SIZE[0] * RANKS.index(self.rank)),
                    CARD_CENTR[1] + CARD_SIZE[1] * SUITS.index(self.suit))

        canvas.draw_image(card_images, card_loc, CARD_SIZE, [
                          pos[0] + CARD_CENTR[0], pos[1] + CARD_CENTR[1]], CARD_SIZE)


class Hand(object):
    def __init__(self, role=''):
        self.clear()
        self.role = role

    def __str__(self):
        return [card.__str__() for card in self.cardlist]

    def clear(self):
        self.cardlist = []
        self.aceNum = 0
        self.status = 'PLAY'

    def add_card(self):
        self.cardlist.append(card)
        if card.get_rank() == 'A':
            self.aceNum += 1

    def get_value(self):
        val = sum([VALUES[card.get_rank()] for card in self.cardlist])
        if self.aceNum > 0 and val < 12:
            return val + 10
        else:
            return val

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def draw(self, canvas, pos):
        for card in self.cardlist:
            card.draw(
                canvas, [pos[0] + self.cardlist.index(card) * CARD_SIZE[0], pos[1]])
        if self.role == 'dealer' and self.status == 'PLAY':
            canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [
                              pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


class Deck(object):
    def __init__(self):
        self.cardbox = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.remain = len(SUITS) * len(RANKS)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cardbox)

    def deal_card(self):
        self.remain -= 1
        return self.cardbox.pop(0)

    def get_remain(self):
        return self.remain

    def draw(self, canvas, pos):
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [
                          pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

    def __str__(self):
        # return a string representing the deck
        return "remains: " + str(self.remain) + "\n" + [card.__str__() for card in self.cardbox]


def init():
    global player_num, outcome, deck, dealer, players, score, round_num, current_player
    round_num = 0
    deck = Deck()
    dealer = Hand('dealer')
    dealer.set_status('PLAY')

    players = [Hand() for i in range(player_num)]
    outcome = ['enjoy your Blackjack' for i in range(player_num)]
    score = [[0, 0] for i in range(player_num)]
    current_player = -1


def set_player_num(input_str):
    global player_num, max_player, score
    if 0 < int(input_str) <= max_player:
        player_num = int(input_str)
    init()
    deal()


# 发牌


def deal():
    global deck, dealer, players, current_player, count, message, round_num, outcome
    if deck.get_remain() - 2 * (len(players) + 1) < 0:
        deck = Deck()
        current_player = -1
    if current_player == -1:
        round_num += 1
        dealer.clear()

        for player in players:
            player.clear()
            outcome[players.index(player)] = 'enjoy your Blackjack'

        for i in range(2):
            dealer.add_card(deck.deal_card())
            for player in players:
                player.add_card(deck.deal_card())

        count = 0
        current_player = 0
        message = "It's player" + str(current_player + 1) + "'s turn now !"
    else:
        outcome[current_player] = 'you lose !'
        players[current_player].set_status('LOSE')
        score[current_player][0] -= 1
        count += 1
        next()
        if current_player == -1:
            dealer.set_status('WIN')
            message = 'New Game ?'
            outcome = [outcome[i] + 'new deal ?' for i in range(len(outcome))]
    if deck.get_remain() == 0:
        message = 'No card ! New deal ?'
        outcome = [message for i in range(len(outcome))]


def next():
    global count, player_num, current_player, players
    lose_num = 0
    while not players[count % player_num].get_status() == 'PLAY' and lose_num < player_num:
        count += 1
        lose_num += 1
    current_player = -1 if lose_num == player_num else count % player_num


def dealer_add():
    global outcome, players, current_player, dealer, deck, message
    for player in players:
        if player.get_status() == 'STAND':
            while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
            if dealer.get_value() > 21 or dealer.get_value() < player.get_value():
                player.set_status('WIN')
                outcome[players.index(player)] = 'you win !'
                score[players.index(player)][0] += 1
                if score[players.index(player)][0] > score[players.index(player)][1]:
                    score[players.index(
                        player)][1] = score[players.index(player)][0]
            else:
                player.set_status('LOSE')
                outcome[players.index(player)] = 'you lose !'
                score[players.index(player)][0] -= 1
    dealer.set_status('OVER')
    message = 'New Game ?'
    outcome = [outcome[i] + ' new deal ?' for i in range(len(outcome))]


# 继续发牌


def hit():
    global outcome, players, current_player, deck, message, count, deck
    if deck.get_remain() > 0 and current_player > -1:
        players[current_player].add_card(deck.deal_card())
        if players[current_player].get_value() > 21:
            outcome[current_player] = 'you lose!'
            players[current_player].set_status('LOSE')
            score[current_player][0] -= 1
        else:
            outcome[current_player] = 'you hit ! hit or stand?'
        count += 1
        next()
        message = "It's player" + str(current_player + 1) + "'s turn now !"
        if deck.get_remain() == 0:
            message = 'No card ! New deal ?'
            outcome = [message for i in range(len(outcome))]
    if deck.get_remain() > 0 and current_player == -1:
        dealer_add()


# 停牌了


def stand():
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global outcome, players, current_player, dealer, deck, message
    if deck.get_remain() > 0 and current_player > -1:
        players[current_player].set_status('STAND')
        outcome[current_player] = 'you stand !'
        next()
        message = "It's player" + str(current_player + 1) + "'s turn now !"
    if deck.get_remain() > 0 and current_player == -1:
        dealer_add()


def draw():
    global dealer, players, outcome, score, message, deck, round_num, current_player
    canvas.draw_text('Blackjack', [220, 30], 20, 'Black')
    canvas.draw_text('Dealer', [20, 50], 15, 'Black')
    canvas.draw_text(message, [130, 50], 15, "Red")
    dealer.draw(canvas, [45, 55])

    canvas.draw_text("Deck:", [400, 50], 15, "Black")
    canvas.draw_text("Round:" + str(round_num), [500, 50], 15, "Black")
    deck.draw(canvas, [420, 55])
    canvas.draw_text("Remains:", [500, 90], 15, "Black")
    canvas.draw_text(str(deck.get_remain()), [520, 110], 15, "Black")

    for player in players:
        canvas.draw_text("Player" + str(players.index(player) + 1) +
                         ":", [20, 200 + 150 * players.index(player)], 15, "Black")
        canvas.draw_text("Score: " + str(score[players.index(player)][0]), [
                         120, 200 + 150 * players.index(player)], 15, "Black")
        canvas.draw_text("Best Score: " + str(score[players.index(player)][1]), [
                         230, 200 + 150 * players.index(player)], 15, "Black")
        canvas.draw_text(outcome[players.index(player)], [
                         380, 200 + 150 * players.index(player)], 15, "Red")
        player.draw(canvas, [45, 205 + 150 * players.index(player)])

    turn_pos = [30, 250 + 150 * current_player]
    canvas.draw_circle(turn_pos, 10, 1, 'Red', 'Red')


frame = simplegui.create_frame('Blackjack', 600, 600)
frame.set_canvas_background("Green")
num_input = frame.add_input("Player number (1 to 3): ", set_player_num, 50)
num_input.set_text('1')


frame.add_button('Deal', deal, 200)
frame.add_button('Hit', hit, 200)
frame.add_button('Stand', stand, 200)
frame.set_draw_handler(draw)
init()
deal()
frame.start()
