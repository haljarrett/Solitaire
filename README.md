# Python Solitaire

This program implements Solitaire as command line game in Python. It has no external dependencies other than
the standard python libraries.

## Use
The program is called with `python Solitaire.py`.
Upon launch, the program will present the state of the board, and a prompt for a move.

Moves are called in the form `[Source] [Target] [Number of Cards]`, where the source and target are specified as
`[(T)ableau/(F)oundation/[(W)aste] [Stack Number]]`.

For instance, moving 2 cards from Tableau 1 to Foundation 0 is called as `T 1 F 0 2`.
The command `cycle` reveals three new cards from the stockpile, `restart` starts a new game, and `quit` quits the
program.

## Rules

The rules are the same as in standard solitaire - you win when all the cards are in the foundations.

## Design

### Data Structures

The fundamental class type in this game is Stack, which is a list of cards, and some functions for moving cards
between them. Its subclasses, TableauStack, FoundationStack, etc, define their own rules for what circumstances allow
cards to be moved to and from them (overriding the give, can_give, take, and can_take methods).

There is a Card class, which defines each card as having a number, suit, and color.

There are a series of Enums which define the suits and colors, and a series of dicts which define the representation
each of these Enum states in a card.

### Program flow

The program has two main flow points - moving and rendering. The Stack classes define what moves are and aren't allowed,
so the move commands are passed directly too them in the form `source.give(target, n)`.

Rendering is done by defining the __str__ method for each of the classes, which cascade when called on the overall
Solitaire class. For instance, we define how each cards are rendered, then each type of stack has an `__str__` method
allowing it to be rendered on one line, and the Solitaire class's __str__ method calls __str__ on each of its constituent
stacks. What this means is that the final rendering is as simple as `print(my_solitaire)`

### Design choices
I chose to implement this game in python for the speed and ease of development. It's OO features are plenty powerful
for the way that I wanted to design classes, and the powerful interactive debugging that it is subject to with pycharm
allow for easy introspection on issues as I developed.

I didn't implement unit tests or use any testing tooling other than interactive debugging in-editor(PyCharm), for the
sake of time and simplicity.
