import stats
import char
import artifact

class CumSolver:
    def __init__(self, basestats, dmg):
        self.c = char.Character(basestats, dmg)
        self.artis = []

        self.cur_dmg = self.c.eval()
        self.i = 0

    def step(self, next_arti=None):
        if next_arti is None:
            next_arti = artifact.make_arti()
        self.artis.append(next_arti)
        max_dmg = self.solve(next_arti)

        self.i += 1
        self.cur_dmg = max_dmg
        return max_dmg
    
    def solve(self, new_arti) -> float:
        raise NotImplemented


# O(N) runtime
class Top1(CumSolver):
    top1 = stats.Loadout()

    def solve(self, a):
        nl = self.top1.add(a)
        new_dmg = self.c.eval(nl)
        if new_dmg > self.cur_dmg:
            self.top1 = nl
        else:
            nl = self.top1
        return nl.dmg

# O(N) runtime
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

# O(N^2) runtime
class TopPerc(CumSolver):
    def __init__(self, *args, perc=0.8):
        super().__init__(*args)

        self.p = perc
        self.loadouts = [self.c.artis]

        # Tracks when each config was added
        self.history = []
        # tracks self.combos wrt iteration number. Sorted by dmg.
        self.history_full = []
    
    def solve(self, a):
        remove_nones = False

        to_try = set()
        for loadout in self.loadouts:
            to_add = loadout.add(a)
            to_try.add(to_add)
            if loadout.artis[a.slot] is None:
                remove_nones = True

        self.history.append(to_try)

        for l in to_try:
            self.c.eval(l)
        
        to_add = sorted(to_try, reverse=True)
        if remove_nones:
            self.loadouts = to_add
        else:
            replace = sorted(to_add + self.loadouts, reverse=True)
            maxi = replace[0].dmg
            self.loadouts = [r for r in replace if r.dmg > self.p*maxi]
        self.history_full.append(self.loadouts.copy())

        return self.loadouts[0].dmg

# O(N^5) runtime
class BruteForce(CumSolver):
    def __init__(self, *args):
        super().__init__(*args)
        self.combos = {self.c.artis}

        # Tracks when each config was added
        self.history = []
        # tracks self.combos wrt iteration number. Sorted by dmg.
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
        self.history.append(to_try.copy())
        
        newmax = max([self.c.eval(l) for l in to_try])

        if remove_nones:
            self.combos = to_try
        else:
            self.combos |= to_try
        self.history_full.append(sorted(self.combos, reverse=True))

        return max(newmax, self.cur_dmg)
