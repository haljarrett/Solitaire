from enum import Enum
import random

""" 
This script implements a basic CLI Solitaire. It presents the status of the cards, and a prompt for action.
    Author: Hal Jarrett
    Email: haljarrett AT gmail DOT com
    License: MIT
    Date: Sept. 30, 2018 

"""

card_values = {1: "A",
               2: "2",
               3: "3",
               4: "4",
               5: "5",
               6: "6",
               7: "7",
               8: "8",
               9: "9",
               10: "10",
               11: "J",
               12: "Q",
               13: "K"}


class Suits(Enum):
    Club = 1
    Spade = 2
    Heart = 3
    Diamond = 4


suit_symbol = {Suits.Club: "C",
               Suits.Spade: "S",
               Suits.Heart: "H",
               Suits.Diamond: "D"}


class Colors(Enum):
    Red = 1
    Black = 2


color_symbol = {Colors.Red: "r",
                Colors.Black: "b"}

suit_colors = {
    Suits.Club: Colors.Black,
    Suits.Spade: Colors.Black,
    Suits.Diamond: Colors.Red,
    Suits.Heart: Colors.Red
}


class Card:
    def __init__(self, suit, number):
        self.color = suit_colors[suit]
        self.suit = suit
        self.number = number
        self.visible = False

    def __str__(self):
        if self.visible:
            return "[{}{}({})]".format(card_values[self.number], suit_symbol[self.suit], color_symbol[self.color])
        else:
            return "[XX]"


class Deck:
    def __init__(self):
        self.cards = list()
        for suit in Suits:
            for number in range(1, 14):
                self.cards.append(Card(suit, number))
        random.shuffle(self.cards)

    def next_card(self):
        return self.cards.pop()


class Stack:
    """Defines a base class for the many stacks of cards in solitaire, and the semantics for moving cards between
    them"""
    def __init__(self):
        self.cards = list()

    def can_give(self, n):
        return len(self.cards) >= n

    def can_take(self, cards):
        return True

    def give(self, other, n):
        if self.can_give(n):
            if other.take(self.cards[-n:]):
                self.cards = self.cards[:-n]
                if len(self.cards) > 0:
                    self.cards[-1].visible = True

    def take(self, cards):
        if self.can_take(cards):
            self.cards.extend(cards)
            return True  # left off here


class TableauStack(Stack):
    def __init__(self, deck, number):
        super().__init__()
        for n in range(number):
            self.cards.append(deck.next_card())
        self.cards[-1].visible = True

    def can_give(self, n):
        # Tableau Stacks can only give cards that are face up
        return self.cards[-n].visible

    def can_take(self, cards):
        # Tableau Stacks can only take cards of the opposite color and next number
        if len(self.cards) == 0:
            return True
        return self.cards[-1].color != cards[0].color and self.cards[-1].number - cards[0].number == 1

    def __str__(self):
        if len(self.cards) > 0:
            outstr = ""
            for card in self.cards:
                outstr += str(card)
            return outstr
        else:
            return "[]"


class FoundationStack(Stack):
    def __init__(self, suit):
        super().__init__()
        self.suit = suit

    def can_take(self, cards):
        if len(cards) != 1:
            return False
        elif cards[0].suit == self.suit:
            if len(self.cards) == 0:
                if cards[0].number == 1:
                    return True
                else:
                    return False
            elif cards[0].number - self.cards[-1].number == 1:
                return True
        else:
            return False

    def can_give(self, n):
        return n == 1 and len(self.cards) > 0

    def __str__(self):
        if len(self.cards) == 0:
            return "[{}]".format(suit_symbol[self.suit])
        else:
            return str(self.cards[-1])


class StockStack(Stack):
    def __init__(self, deck):
        super().__init__()
        self.cards = deck.cards

    def __str__(self):
        if len(self.cards) == 0:
            return "[]"
        else:
            return "[XX]"


class WasteStack(Stack):
    def take(self, cards):
        for card in cards:
            card.visible = True
        super().take(cards)
        return True

    def __str__(self):
        if len(self.cards) == 0:
            return "[]"
        elif len(self.cards) < 3:
            outstr = ""
            for card in self.cards:
                outstr += str(card)
            return outstr
        else:
            outstr = ""
            for card in self.cards[-3:]:
                outstr += str(card)
            return outstr


class Solitaire:
    def __init__(self):
        self.deck = Deck()
        self.foundations = [
            FoundationStack(Suits.Diamond),
            FoundationStack(Suits.Club),
            FoundationStack(Suits.Heart),
            FoundationStack(Suits.Spade),
        ]
        self.tableau = [TableauStack(self.deck, n) for n in range(1, 8)]
        for t in self.tableau:
            t.cards[-1].visible = True
        self.stock = StockStack(self.deck)
        self.waste = [WasteStack()]
        self.move_targets = {"T": self.tableau,
                             "W": self.waste,
                             "F": self.foundations}
        self.stock.give(self.waste[0], 3)

    def __str__(self):
        if len(self.foundations[0].cards) + len(self.foundations[1].cards) + len(self.foundations[2].cards) \
                + len(self.foundations[3].cards) == 52:
            print("You Win!\n")
            quit()

        outstr = ""
        outstr += "Foundations:"
        for f in self.foundations:
            outstr += str(f)
        outstr += "\n"
        outstr += "Tableau:\n"
        for n, t in enumerate(self.tableau):
            outstr += str(n) + ": " + str(t) + "\n"
        outstr += "Stock and Waste: "
        outstr += str(self.stock) + str(self.waste[0])
        return outstr


def test_args(tokens):
    if len(tokens) == 1 and (tokens[0] in ["restart", "cycle", "quit"]):
        return True
    elif len(tokens) != 5:
        return False
    else:
        for (x, n) in [(tokens[0], tokens[1]),(tokens[2], tokens[3])]:
            if x not in "FTW" or int(n) < 0:
                return False
            if x == "F":
                if int(n) > 3:
                    return False
            if x == "T":
                if int(n) > 6:
                    return False
            if x == "W":
                if int(n) != 0:
                    return False
        if int(tokens[4]) < 1:
            return False
        return True


if __name__ == "__main__":
    s = Solitaire()
    while True:
        print(str(s))
        print("\nCommand Structure: [F/T/W] <number> [F/T/W] <number> <cards-to-move>\n"
              "OR: cycle (cycle waste)\n"
              "OR: restart / quit")
        text = input("Command?: ")
        tokens = text.split()
        if test_args(tokens):
            if tokens[0] == "cycle":
                if len(s.stock.cards) > 2:
                    s.stock.give(s.waste[0], 3)
                else:
                    s.waste[0].give(s.stock, len(s.waste[0].cards))
            elif tokens[0] == "restart":
                print("Restarting!")
                s = Solitaire()
                continue
            elif tokens[0] == "quit":
                quit()
            else:
                (s.move_targets[tokens[0]])[int(tokens[1])].give(
                    (s.move_targets[tokens[2]])[int(tokens[3])], int(tokens[4]))
        else:
            print("Bad Argument!\n")
