from dataclasses import dataclass
from typing import Tuple
import numpy as np
import random

import char
from common import slotnames, statnames, statmap
from sampler import StatSampler

mainstat = (
    StatSampler({'HP': 1}),
    StatSampler({'ATK': 1}),
    StatSampler({'HP%': 80, 'ATK%': 80, 'DEF%': 80, 'EM': 30, 'ER': 30}),
    StatSampler({'HP%': 85, 'ATK%': 85, 'DEF%': 80, 'EM': 10,
     'Phys': 20, 'Hydro': 20, 'Pyro': 20, 'Cryo': 20, 'Electro': 20, 'Anemo': 20, 'Geo': 20}),
    StatSampler({'HP%': 22, 'ATK%': 22, 'DEF%': 22, 'EM': 4, 'CR': 10, 'CD': 10, 'Heal': 10}),
)
substat = StatSampler({
    'HP': 6, 'DEF': 6, 'ATK': 6,
    'HP%': 4, 'DEF%': 4, 'ATK%': 4, 'ER': 4, 'EM': 4,
    'CR': 3, 'CD': 3
})

main_vals = {
    'HP': 4780, 'ATK': 311, 'DEF': -1,
    'HP%': 466, 'ATK%': 466, 'DEF%': 583,
    'EM': 187, 'ER': 518,
    'CR': 311, 'CD': 622,
    'Heal': 359, 'Phys': 583,
    'Hydro': 466, 'Pyro': 466, 'Cryo': 466, 'Electro': 466, 'Anemo': 466, 'Geo': 466, 'Dendro': 466
}
sub_roll_vals = {
    'HP':   [209, 239, 269, 299],
    'DEF':  [16, 19, 21, 23],
    'ATK':  [14, 16, 18, 19],
    'HP%':  [41, 47, 53, 58],
    'DEF%': [51, 58, 66, 73],
    'ATK%': [41, 47, 53, 58],
    'EM':   [16, 19, 21, 23],
    'ER':   [45, 52, 58, 65],
    'CR':   [27, 31, 35, 39],
    'CD':   [54, 62, 70, 78],
}

@dataclass(order=True, frozen=True)
class Artifact:
    slot: int
    main_stat: int
    subs:    Tuple[int]  # Fixed length tuples (4), collection of 14 integers.
    subvals: Tuple[int]
    preroll: Tuple[int]

    def tostat(self):
        s = np.zeros(len(statnames), dtype=int)
        s[self.main_stat] = main_vals[statnames[self.main_stat]]
        s[np.array(self.subs)] += self.subvals
        return char.Stats(s)

    def __add__(self, other):
        if isinstance(other, Artifact):
            return self.tostat() + other.tostat()
        raise NotImplemented

    def __repr__(self):
        sub_lst = [f'{statnames[s]}:{vi}>{vf}' for s, vf, vi in zip(self.subs, self.subvals, self.preroll)]
        sub_str = ', '.join(sub_lst)
        return f'{statnames[self.main_stat]} {slotnames[self.slot]}@({sub_str})'

class ArtifactFactory:
    def __init__(self, slot=None):
        if slot is None:
            slot = random.choice([0, 1, 2, 3, 4])
        self.slot = slot
        self.main_stat = statmap[ mainstat[slot].get() ]
        
        self.pick_subs()
        self.init_substat_vals()
        
        self.rollup()
        self.fix_sub_order()
    
    def pick_subs(self):
        nodup_distr = substat.remove(statnames[self.main_stat])
        
        subs = []
        for _ in range(4):
            ssi = nodup_distr()
            subs.append(statmap[ssi])
            nodup_distr = nodup_distr.remove(ssi)
        self.subs = tuple(subs)
        
    def init_substat_vals(self):
        four_sub = (random.random() > .8)
        subvals = []
        for s in self.subs[:-1]:
            ssi = statnames[s]
            subvals.append(random.choice(sub_roll_vals[ssi]))
        if four_sub:
            ssi = statnames[self.subs[-1]]
            subvals.append(random.choice(sub_roll_vals[ssi]))
        else:
            subvals.append(0)
        self.preroll = tuple(subvals)
        
    # rolls up artifact to lvl 20. Num rolls = 5
    def rollup(self):
        subvals = list(self.preroll)
        
        nroll = 5
        if self.preroll[-1] == 0:
            nroll -= 1
            subvals[-1] += random.choice(sub_roll_vals[statnames[self.subs[-1]]])
        
        for _ in range(nroll):
            r = random.choice([0, 1, 2, 3])
            inc = statnames[self.subs[r]]
            subvals[r] += random.choice(sub_roll_vals[inc])
        self.subvals = tuple(subvals)
        
    def fix_sub_order(self):
        paired = sorted(zip(self.subs, self.preroll, self.subvals))
        self.subs, self.preroll, self.subvals = list(zip(*paired))


def make_arti():
    a = ArtifactFactory()
    return Artifact(a.slot, a.main_stat, a.subs, a.subvals, a.preroll)
