from itertools import cycle
from config import VERBOSE
from game_table import History, Pot, ALL_CARD_PERMS
from utils import game_print
from player import Player, HumanPlayer, GTOPlayer, WeakGTOPlayer

def play_round(p1:Player, p2:Player, p1_card=None, p2_card=None):
    """
    P1 moves first
    """
    pot = Pot()
    history = History()
    p1.start_game(p1_card, pot) # blind + deal cards
    p2.start_game(p2_card, pot)
    game_print(f"{p1.name}: {p1.card}, {p2.name}: {p2.card}", "green")
    game_print("===============  GAME START ===============")
    hero = p1
    villian = p2
    while True:
        success = hero.act(hero.card, history, pot)
        if not success:
            """
            Compare the cards and give the pot to the winner
            """
            if p1.get_hand_rank() > p2.get_hand_rank():
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

    # reset
    p1.end_game()
    p2.end_game()


human = HumanPlayer(chip=0)
gto_player = GTOPlayer(chip=0,alpha=1/3)
weak_gto_player = WeakGTOPlayer(chip=0, alpha=1/3)


cycle = 1
p1 = gto_player
p2 = human
for _ in range(cycle):
    for p1_card, p2_card in ALL_CARD_PERMS:
        play_round(p1, p2, p1_card, p2_card)
    for p1_card, p2_card in ALL_CARD_PERMS:
        play_round(p2, p1, p2_card, p1_card)

print(f"{p1.name} has {p1.chip} chips")
print(f"{p2.name} has {p2.chip} chips")
