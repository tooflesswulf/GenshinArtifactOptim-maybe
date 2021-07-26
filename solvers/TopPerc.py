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
        self.loadouts = []
        for l in rec:
            d = l.dmg
            if d < thresh:
                break
            self.loadouts.append((d, l))
        return maxdmg


if __name__ == '__main__':
    import numpy as np
    import damage

    diona = [
        0, 9570,
        0, 601,
        0, 212 + 401,
        50, 500 + 469,
        0, 0,
        0, 0, 0, 0, 240, 0, 0, 0, 0,
    ]
    diona = np.array(diona)
    formula = damage.NormalDmg(2, elem='Cryo') + damage.NormalDmg(.67, elem='Cryo') + damage.NormalDmg(.2)
    c = char2.Character(diona, formula)

    slv = TopPerc(c, formula)
    slv.step()
    