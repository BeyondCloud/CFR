import random
import itertools
from itertools import cycle
from dataclasses import dataclass

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


@dataclass
class Pot:
    chip:int = 0


def deal_cards():
    """Deal cards to players and leave one card unseen."""
    deck = ['J', 'Q', 'K']
    random.shuffle(deck)
    return deck[:2], deck[2]

ALL_CARD_PERMS = list(itertools.permutations( ['J', 'Q', 'K'], 2))
