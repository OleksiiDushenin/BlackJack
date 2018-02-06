import random


def play():
    player = register_player()
    while True:
        play_round(player)

        if player.amount < 1:
            print('Not enough money to continue. Bye!')
            break

        print('Your balance %s' % player.amount)

        if 'y' != input('Do you want to continue? (y - yes, otherwise - exit): '):
            break


def play_round(player):
    game_round = Round(make_bet(player))
    print(game_round)
    play_by_player(game_round)
    if game_round.is_player_over():
        print('Dealer won!')
        return
    play_by_dealer(game_round)
    winner = game_round.get_winner()
    if winner == 'Dealer':
        print('Dealer won!')
        return
    if winner == 'Player':
        print('Player won!')
        player.amount = player.amount + 2 * int(game_round.bet)
        return
    print('It is a draw!')
    player.amount = player.amount + int(game_round.bet)


def play_by_player(game_round):
    if not game_round.player_hand.is_21():
        while True:
            if 'y' != input('Do you want to take another card? (y - yes, otherwise - exit): '):
                break
            is_end = game_round.next_card_for_player()
            print(game_round)
            if is_end:
                break


def play_by_dealer(game_round):
    while True:
        is_end = game_round.next_card_for_dealer()
        print(game_round)
        if is_end:
            break


def register_player():
    print('Welcome to BlackJack')
    try:
        amount = int(input('Input your balance:   '))
        return Player(amount)
    except ValueError:
        print('Invalid balance!')


def make_bet(player):
    while True:
        try:
            return player.bet(int(input('Input your bet:   ')))
        except ValueError:
            print('Invalid bet!')


class Card(object):
    suits = ['club', 'diamond', 'heart', 'spade']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return '%s %s' % (self.value, self.suit)

    def get_value(self, total):
        try:
            return int(self.value)
        except ValueError:
            if 'ace' == self.value:
                if total + 11 > 21:
                    return 1
                else:
                    return 11
            else:
                return 10


class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in Card.suits:
            for value in Card.values:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def next_card(self):
        return self.cards.pop()


class Round(object):
    def __init__(self, bet):
        self.bet = bet
        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = Hand()
        self.player_hand.add_card(self.deck.next_card())
        self.player_hand.add_card(self.deck.next_card())

        self.dealer_hand = Hand()
        self.dealer_hand.add_card(self.deck.next_card())

    def __str__(self):
        return 'Player: %s \nDealer: %s' % (self.player_hand, self.dealer_hand)

    def next_card_for_player(self):
        self.player_hand.add_card(self.deck.next_card())
        if self.player_hand.is_21():
            print('Player has 21!')
            return True
        elif self.player_hand.is_over():
            print('Player has too many points!')
            return True
        else:
            return False

    def next_card_for_dealer(self):
        self.dealer_hand.add_card(self.deck.next_card())
        if self.dealer_hand.is_21():
            print('Dealer has 21!')
            return True
        elif self.dealer_hand.is_over():
            print('Dealer has too many points!')
            return True
        elif self.dealer_hand.is_dealer_limit():
            print('Dealer reached limit!')
            return True
        else:
            return False

    def is_player_over(self):
        return self.player_hand.is_over()

    def get_winner(self):
        if self.player_hand.is_over():
            return 'Dealer'
        if self.dealer_hand.is_over():
            return 'Player'
        if self.dealer_hand.result == self.player_hand.result:
            return 'Draw'
        if self.dealer_hand.result < self.player_hand.result:
            return 'Player'
        return 'Dealer'


class Hand(object):
    def __init__(self):
        self.cards = []
        self.result = 0

    def __str__(self):
        return 'Result: %s; Cards: %s' % (self.result, self.to_string())

    def to_string(self):
        return '; '.join(str(e) for e in self.cards)

    def add_card(self, card):
        self.cards.append(card)
        self.result += card.get_value(self.result)

    def is_21(self):
        return self.result == 21

    def is_over(self):
        return self.result > 21

    def is_dealer_limit(self):
        return self.result >= 17


class Player(object):
    def __init__(self, amount):
        if amount <= 0:
            raise ValueError('Amount should be positive!')
        self.amount = amount

    def bet(self, amount):
        if self.amount < amount:
            raise ValueError('Amount is too high')
        elif amount < 1:
            raise ValueError('Amount should be positive')
        else:
            self.amount -= amount
            return amount


class Dealer(object):
    pass


if __name__ == "__main__":
    play()
