import random
import numpy as np
from typing import Tuple

import artifact
import stats
from common import statnames, statmap, slotnames

class SALoadout(stats.Loadout):
    artis: Tuple[artifact.SArti] = ()
    def get_neighbors(self):
        iters = [a.get_neighbors() for a in self.artis]

        while len(iters) > 0:
            i = random.randint(0, len(iters) - 1)
            try:
                ch_arti = next(iters[i])
                ret = self.add(ch_arti)
                yield SALoadout(artis=ret.artis)
            except StopIteration:
                del iters[i]
                continue


# TODO: same as above, but pool the substats.
class SALoadout2():
    mainstats: Tuple[int] = (None, None, None, None, None)
    substats: Tuple[int]
    def get_neighbors(self):
        pass
    
    def _bake(self):
        return 0


class Annealer:
    def __init__(self, char, kb=10, sched=None, s0=None):
        di = char.eval(stats.Loadout())
        self.norm = 1/di

        if s0 is None:
            s0 = SALoadout(artis=tuple([make_max_arti(i) for i in range(5)]))
        self.s = s0
        self.c = char
        self.stepnum = 0
        self.visits = 0

        self.kb = kb

        if sched is None:
            sched = lambda x: 1/x

        self.sched = lambda x: 1 if x == 0 else sched(x)
    
    def fermi_dirac(self, E, T):
        p = 1 / (np.exp(-E / self.kb / T) + 1)
        return p

    def step(self):
        temp = self.sched(self.stepnum)
        self.stepnum += 1

        d0 = self.c.eval(self.s)

        cach = []
        for neigh in self.s.get_neighbors():
            self.visits += 1
            dmg = self.c.eval(neigh)
            e = self.norm * (dmg - d0)
            p = self.fermi_dirac(e, temp)
            # print(e, p, temp)
            if random.random() > p:
                cach.append((dmg, p, neigh))
                continue
            self.s = neigh
            return dmg
        
        psel = []
        for _, p, _ in cach:
            psel.append(p)
        psel = np.array(psel) / np.sum(psel)
        ret_ix = np.random.choice(len(psel), p=psel)
        ret, _, nxt_s = psel[ret_ix]
        self.s = nxt_s
        print('Exhausted options. Probably near opt now')
        return ret
        



def make_max_arti(slot=None):
    if slot is None:
        slot = random.choice([0, 1, 2, 3, 4])
    ms = statmap[ random.choice(artifact.mainstat[slot].k) ]

    sub_distr = artifact.substat.remove(statnames[ms])
    subs = random.sample(sub_distr.k, k=4)

    preroll = [artifact.sub_roll_vals[s][-1] for s in subs]
    subvals = preroll.copy()

    # rolling process
    for _ in range(5):
        r = random.choice([0, 1, 2, 3])
        inc = subs[r]
        subvals[r] += artifact.sub_roll_vals[inc][-1]

    subs = tuple(sorted(map(statmap.__getitem__, subs)))
    return artifact.SArti(slot, ms, subs, tuple(subvals), tuple(preroll))
