import random
import itertools
from termcolor import colored
from itertools import cycle
from dataclasses import dataclass
import numpy as np

VERBOSE = True
card_strength = {"J":0, "Q":1, "K":2}

def game_print(text, color="white"):
    if VERBOSE:
        print(colored(text, color))

def deal_cards():
    """Deal cards to players and leave one card unseen."""
    deck = ['J', 'Q', 'K']
    random.shuffle(deck)
    return deck[:2], deck[2]


ALL_CARD_PERMS = list(itertools.permutations( ['J', 'Q', 'K'], 2))
ALL_CARD_PERMS_CYCLE =  cycle(ALL_CARD_PERMS)

def sample(pdf):
    total = sum(pdf)
    rand_num = random.uniform(0, total)
    cumulative_sum = 0
    for i in range(len(pdf)):
        cumulative_sum += pdf[i]
        if rand_num < cumulative_sum:
            return i

def decision_action():
    pass


@dataclass
class Pot:
    chip:int = 0

class History:
    def __init__(self):
        self._acts = ["o"]
    def __len__(self):
        return len(self._acts)
    def append(self, act):
        self._acts.append(act)
    def to_string(self):
        return "".join(self._acts)
    def get_prev_act(self):
        return self._acts[-1]

# Play a round of Kuhn Poker
class Player:
    def __init__(self, chip):
        self.name = self.__class__.__name__
        self._chip = chip
        self.card = None

    def handle_act(self, idx, history:History) -> str:
        """
        id2act = ["c", "b", "f"]
        """
        pass

    def grab_chip_from(self, pot:Pot):
        game_print(f"{self.name} wins the pot {pot.chip}")
        self._chip += pot.chip
        pot.chip = 0

    def check_call(self, size, pot:Pot, history:History):
        if history.get_prev_act() != "b":
            game_print(f"{self.card} check",'blue')
            return
        game_print(f"{self.card} calls {size} chips into the pot {pot.chip} chips")
        pot.chip += size
        self._chip -= size

    def bet(self, size, pot:Pot):
        game_print(f"{self.card} bets {size} chips", 'red')
        pot.chip += size
        self._chip -= size
    def fold(self):
        game_print(f"{self.card} folds")
        return

    def act(self, hand, history: History, pot) -> bool:
        """
        If no more action, return False. This means end of the game
        """
        action_node = self.tree.get(history.to_string())
        if not action_node:
            return False
        pdf = action_node[hand]
        idx = sample(pdf)
        if idx == 0:
            # if the last action is bet, the player has to call
            self.check_call(1, pot, history)
            # otherwise, the player can check
            act = "c"
        elif idx == 1:
            self.bet(1, pot)
            act = "b"
        elif idx == 2:
            self.fold()
            act = "f"
        history.append(act)
        return True

    def print_chip(self):
        print(f"{self.name} has {self._chip} chips")

class Human(Player):
    # [check/call, bet, fold]
    alpha = 0
    tree = {
        "o": {
            "J":[1, 0, 0],
            "Q":[1, 0, 0],
            "K":[1, 0, 0],
            },
        "oc": {
            "J":[1, 0, 0],
            "Q":[1, 0, 0],
            "K":[0, 1, 0],
            },
        "ob":{ # if bet is made, the other player cannot bet
            "J":[0, 0, 1],
            "Q":[1, 0, 0],
            "K":[1, 0, 0],
        },
        "ocb":{
            "J":[0, 0, 1],
            "Q":[0, 0, 1],
            "K":[1, 0, 0],
        },
    }
    def __init__(self, chip):
        super().__init__(chip)

class GTOPlayer(Player):
    # [check/call, bet, fold]
    alpha = np.clip(0, a_min=0, a_max=1/3)
    tree = {
        "o": {
            "J":[1-alpha, alpha, 0],
            "Q":[1, 0, 0],
            "K":[1-3*alpha, 3*alpha, 0],
            },
        "oc": {
            "J":[1-alpha, alpha, 0],
            "Q":[2/3, 1/3, 0],
            "K":[0,1,0],
            },
        "ob":{
            "J":[0,0,1],
            "Q":[1/3,0,2/3],
            "K":[1,0,0],
        },
        "ocb":{
            "J":[0,0,1],
            "Q":[alpha+1/3,0,2/3-alpha],
            "K":[1,0,0],
        },
    }
    def __init__(self, chip):
        super().__init__(chip)


def play_round(p1:Player, p2:Player):
    pot = Pot()
    history = History()
    # (p1_card, p2_card), unseen_card = deal_cards()
    p1_card, p2_card = next(ALL_CARD_PERMS_CYCLE)
    p1.card = p1_card
    p2.card = p2_card
    game_print(f"{p1.name}: {p1_card}, {p2.name}: {p2_card}", "green")
    game_print("======== Place the ante 1 chip to the pot. =========")
    p1.bet(1,pot)
    p2.bet(1,pot)
    game_print("====================================================")
    hero = p1
    villian = p2
    while True:
        game_print(f"Pot: {pot.chip}, {hero.card} move")
        success = hero.act(hero.card, history, pot)
        if not success:
            """
            Compare the cards and give the pot to the winner
            """
            if p1.card > p2.card:
                p1.grab_chip_from(pot)
            else:
                p2.grab_chip_from(pot)
            break
        # if one player folds, the other gets the pot
        if history.get_prev_act() == "f":
            villian.grab_chip_from(pot)
            break
        else:
            pass
        hero, villian = villian, hero

p1 = Human(chip=0)
p2 = GTOPlayer(chip=0)

cycle = 1
for _ in range(len(ALL_CARD_PERMS) * cycle):
    play_round(p1, p2)
for _ in range(len(ALL_CARD_PERMS) * cycle):
    play_round(p2, p1)

p1.print_chip()
p2.print_chip()
