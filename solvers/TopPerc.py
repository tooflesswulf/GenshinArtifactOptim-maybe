from functools import total_ordering
from solvers.solverbase import CumSolver
import char2

class TopPerc(CumSolver):
    def __init__(self, *args, perc=0.8):
        super().__init__(*args)

        self.p = perc
        self.loadouts = [self.c.artis]
    
    def solve(self, a):
        replace = self.c.artis[a.slot] is None

        totry = set()
        for loadout in self.loadouts:
            totry.add(loadout.add(a))

        rec = [] if replace else self.loadouts
        for l in totry:
            self.c.eval(l)
            rec.append(l)

        rec = sorted(rec, reverse=True)
        maxdmg = rec[0].dmg
        thresh = maxdmg * self.p

        self.c.equip(rec[0])

        self.loadouts = []
        for l in rec:
            d = l.dmg
            if d < thresh:
                break
            self.loadouts.append(l)
        return maxdmg
