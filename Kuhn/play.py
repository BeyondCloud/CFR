import random
import itertools
from itertools import cycle
from config import VERBOSE
from game_table import History, Pot
from utils import game_print
from player import Player, Human, GTOPlayer, WeakGTOPlayer



def deal_cards():
    """Deal cards to players and leave one card unseen."""
    deck = ['J', 'Q', 'K']
    random.shuffle(deck)
    return deck[:2], deck[2]

ALL_CARD_PERMS = list(itertools.permutations( ['J', 'Q', 'K'], 2))
ALL_CARD_PERMS_CYCLE =  cycle(ALL_CARD_PERMS)

def play_round(p1:Player, p2:Player):
    pot = Pot()
    history = History()
    # (p1_card, p2_card), unseen_card = deal_cards()
    p1_card, p2_card = next(ALL_CARD_PERMS_CYCLE)
    p1.card = p1_card
    p2.card = p2_card
    game_print(f"{p1.name}: {p1_card}, {p2.name}: {p2_card}", "green")
    # game_print("======== Place the ante 1 chip to the pot. =========")
    p1.bet(1,pot,log=False)
    p2.bet(1,pot,log=False)
    game_print("===============  GAME START ===============")
    hero = p1
    villian = p2
    while True:
        success = hero.act(hero.card, history, pot)
        if not success:
            """
            Compare the cards and give the pot to the winner
            """
            card_strength = {"J":0, "Q":1, "K":2}
            if card_strength[p1.card] > card_strength[p2.card]:
                p1.grab_chip_from(pot)
            else:
                p2.grab_chip_from(pot)
            break
        # if one player folds, the other gets the pot
        if history.get_prev_act() == "f":
            villian.grab_chip_from(pot)
            break
        hero, villian = villian, hero
    if VERBOSE:
        game_print(f"{p1.name} has {p1.chip} chips","blue")
        game_print(f"{p2.name} has {p2.chip} chips","blue")

human = Human(chip=0)
gto_player = GTOPlayer(chip=0,alpha=1/3)
weak_gto_player = WeakGTOPlayer(chip=0, alpha=1/3)


cycle = 1000
p1 = gto_player
p2 = weak_gto_player
for _ in range(len(ALL_CARD_PERMS) * cycle):
    play_round(p1, p2)
for _ in range(len(ALL_CARD_PERMS) * cycle):
    play_round(p2, p1)

print(f"{p1.name} has {p1.chip} chips")
print(f"{p2.name} has {p2.chip} chips")
