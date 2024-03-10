import numpy as np
from game_table import History, Pot
from utils import game_print, sample

# Play a round of Kuhn Poker
class Player:
    def __init__(self, chip, name=None):
        self.name = name
        if not name:
            self.name = self.__class__.__name__
        self.chip = chip
        self.card = None
        # self.chip_in_pot = 0  # don't need this, you can calculate it from pot - initial chip
        self.init_chip_size = self.chip
    def start_game(self, card, pot:Pot, blind=1, log=False):
        self.init_chip_size = self.chip
        self.card = card
        self.bet(blind,pot,log=log)

    def end_game(self):
        self.card = None

    def chip_in_pot(self):
        return self.init_chip_size - self.chip

    def grab_chip_from(self, pot:Pot):
        game_print(f"{self.name} wins pot {pot.chip}","yellow")
        self.chip += pot.chip
        pot.chip = 0

    def check_call(self, size, pot:Pot, history:History) -> int:
        """
        return call size, if check return 0
        """
        if history.get_prev_act() != "b":
            game_print(f"{self.card} check",'blue')
            return 0
        self.bet(size, pot, log=True, type="call")
        game_print(f"{self.card} calls {size}")
        return size

    def bet(self, size, pot:Pot, log=True, type="bet"):
        if log:
            game_print(f"{self.card} {type}s {size} chips", 'red')
        pot.chip += size
        self.chip -= size

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
    def get_hand_rank(self):
        return {"J":0, "Q":1, "K":2}[self.card]

class HumanPlayer(Player):
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
    def __init__(self, chip, name=None):
        super().__init__(chip, name=name)


class WeakGTOPlayer(Player):
    def __init__(self, chip, alpha=0,name=None):
        assert 0 <= alpha <= 1/3
        super().__init__(chip, name)
        # [check/call, bet, fold]
        self.tree = {
            "o": {
                "J":[  1 - alpha,   alpha, 0],
                "Q":[          1,       0, 0],
                "K":[1 - 3*alpha, 3*alpha, 0],
                },
            "oc": {
                "J":[2/3, 1/3, 0],
                "Q":[1, 0, 0],
                "K":[0,1,0],
                },
            "ob":{
                "J":[0,0,1],
                "Q":[1,0,0],
                "K":[1,0,0],
            },
            "ocb":{
                "J":[0,0,1],
                "Q":[alpha+1/3,0,2/3-alpha],
                "K":[1,0,0],
            },
        }
class GTOPlayer(Player):
    def __init__(self, chip, alpha=0,name=None):
        assert 0 <= alpha <= 1/3
        super().__init__(chip,name)

        # [check/call, bet, fold]
        self.tree = {
            "o": {
                "J":[  1 - alpha,   alpha, 0],
                "Q":[          1,       0, 0],
                "K":[1 - 3*alpha, 3*alpha, 0],
                },
            "oc": {
                "J":[2/3, 1/3, 0],
                "Q":[1, 0, 0],
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
