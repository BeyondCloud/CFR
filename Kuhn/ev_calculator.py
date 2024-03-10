import numpy as np
from player import Player, GTOPlayer, HumanPlayer
from game_table import ALL_CARD_PERMS, Pot

def _calc_ev_card(hero:Player, villian:Player, hero_bet = 0 , villian_bet = 0, hist = "o"):
    assert hist.count("b") <= 1
    val = 0
    if not hero.tree.get(hist):
        if hero.get_hand_rank() > villian.get_hand_rank():
            return villian_bet
        else:
            return -hero_bet
    for act, prob in enumerate(hero.tree[hist][hero.card]):
        if prob == 0:
            continue
        if act == 0:
            if hist[-1] == "b":
                val -= prob * _calc_ev_card(hero=villian, villian=hero,
                                            hero_bet=villian_bet,
                                            villian_bet=hero_bet+1,
                                            hist=hist + "c")
            else:
                val -= prob * _calc_ev_card(hero=villian, villian=hero,
                                            hero_bet=villian_bet,
                                            villian_bet=hero_bet,
                                            hist=hist + "c")
        elif act == 1:
            val -= prob * _calc_ev_card(hero=villian, villian=hero,
                                            hero_bet=villian_bet,
                                            villian_bet=hero_bet+1,
                                            hist=hist + "b")
        elif act == 2:
            val -= prob * hero_bet

    # print(val, hist)
    return val


def calc_ev_card(p1:Player, p2:Player, p1_card, p2_card):
    res = 0
    pot = Pot()
    p1.start_game(p1_card,pot)
    p2.start_game(p2_card,pot)
    ev = _calc_ev_card(p1, p2, 1, 1)
    res  += ev
    return  res


def calc_ev(hero:Player, villian:Player):
    res = 0
    for p1_card, p2_card in ALL_CARD_PERMS:
        ev = calc_ev_card(p1, p2, p1_card, p2_card)
        res  += ev
        print(p1_card,p2_card, ev)
    return  res / len(ALL_CARD_PERMS)

if __name__ == "__main__":
    alpha = 0
    p1 = HumanPlayer(chip=0, name="p1")
    # p1 = GTOPlayer(chip=0,alpha=alpha, name="p1")

    p2 = GTOPlayer(chip=0,alpha=alpha, name="p2")
    ev = calc_ev(p1, p2)
    ev2 = calc_ev(p2, p1)
    print(ev)
    print(ev2)
    # assert ev == -0.055555555555555615

    # alpha = 1
    # assert np.allclose([
    #     calc_ev_card(p1, p2, "J", "Q"),
    #     calc_ev_card(p1, p2, "J", "K"),
    #     calc_ev_card(p1, p2, "Q", "J"),
    #     calc_ev_card(p1, p2, "Q", "K"),
    #     calc_ev_card(p1, p2, "K", "J"),
    #     calc_ev_card(p1, p2, "K", "Q"),
    # ],
    # [-1,-1,0.6666666666666666, -1.3333333333333333,1.3333333333333333,1]
    # )
