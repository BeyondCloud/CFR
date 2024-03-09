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
