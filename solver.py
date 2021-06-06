import stats
import char
import artifact

class CumSolver:
    def __init__(self, basestats, dmg):
        self.c = char.Character(basestats, dmg)
        self.artis = []

        self.cur_dmg = self.c.eval()
        self.i = 0

    def step(self):
        self.i += 1
        a = artifact.make_arti()
        self.artis.append(a)
        max_dmg = self.solve(a)
        self.cur_dmg = max_dmg
        return max_dmg
    
    def solve(self, new_arti) -> float:
        raise NotImplemented


class Top1(CumSolver):
    top1 = stats.Loadout()

    def solve(self, a):
        nl = self.top1.add(a)
        self.c.equip(nl)

        new_dmg = self.c.eval()
        if new_dmg > self.cur_dmg:
            self.top1 = nl
        else:
            self.c.equip(self.top1)
            nl = self.top1
        return nl.dmg


class Top2(CumSolver):
    top1 = stats.Loadout()
    top2 = stats.Loadout()

    def solve(self, a):
        prop1 = self.top1.add(a)
        prop2 = self.top2.add(a)

        self.c.eval(prop1)
        self.c.eval(prop2)

        self.top1, self.top2 = sorted([prop1, prop2, self.top1, self.top2], reverse=True)[:2]
        return self.top1.dmg


class BruteForce(CumSolver):
    def __init__(self, *args):
        super().__init__(*args)
        self.combos = {self.c.artis}

        # Tracks when each config was added
        self.history = []
        # tracks self.combos wrt iteration number
        self.history_full = []

        # Tracks which prior config (v) leads to config (k)
        self.config_prior = {}
        # hashmap config -> iteration number
        self.config_itern = {}
    
    def solve(self, a):
        remove_nones = False

        to_try = set()
        for loadout in sorted(self.combos, reverse=True):
            to_add = loadout.add(a)
            if to_add not in to_try:
                self.config_prior[to_add] = loadout
                self.config_itern[to_add] = self.i
            to_try.add(to_add)
            if loadout.artis[a.slot] is None:
                remove_nones = True
        self.history.append(to_try)
        
        newmax = max([self.c.eval(l) for l in to_try])

        if remove_nones:
            self.combos = to_try
        else:
            self.combos |= to_try
        self.history_full.append(self.combos)

        return max(newmax, self.cur_dmg)
