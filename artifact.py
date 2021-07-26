from dataclasses import dataclass, field
from typing import Tuple
import numpy as np
import random

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
    _stats: field(init=False, hash=False, compare=False)

    def tostat(self):
        import stats
        s = np.zeros(len(statnames))
        s[self.main_stat] = main_vals[statnames[self.main_stat]]
        s[np.array(self.subs)] += self.subvals
        return stats.Stats(s)

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


# Generates neighbors list, since its all symmetric. Done to speed up get_neighbors() in future.
neighbors = []
for slot in range(5):
    ns = []
    for mv in map(statmap.__getitem__, mainstat[slot].k):
        ns.append(('mainstat', mv))
    
    svs = []
    for a in range(6):
        for b in range(6-a):
            for c in range(6-a-b):
                svs.append((a, b, c, 5-a-b-c))
    for sub in map(statmap.__getitem__, substat.k):
        for i in range(4):
            sub_repl = (i, sub)
            for sv in svs:
                ns.append(('substat', (sub_repl, sv)))
    neighbors.append(ns)
    

# SA artifact. Implements a transition function.
# Three types of transitions:
#  - Main stat becomes `ms` ('mainstat', ms)         
#  - ith sub deleted, replaced by `sv` and new subval distr
#        ('substat', [(i, sv), (a, b, c, d)])
class SArti(Artifact):
    def get_neighbors(self):
        ns = neighbors[self.slot]
        ixs = list(range(len(ns)))
        random.shuffle(ixs)
        for i in ixs:
            a = ns[i]
            # if a[0] == 'mainstat' and a[1] == self.main_stat: continue
            # if a[0] == 'substat' and a[1][1] in self.subs: continue

            if a[0] == 'mainstat':
                new_ms = a[1]
                if new_ms == self.main_stat: continue
                yield SArti(self.slot, new_ms, self.subs, self.subvals, self.preroll)
            
            elif a[0] == 'substat':
                (i, sv), new_rolls = a[1]
                if sv == self.main_stat: continue
                if sv in self.subs and self.subs[i] != sv: continue
                new_subs = list(self.subs) + [sv]
                del new_subs[i]
                new_subs = tuple(sorted(new_subs))

                pr = [sub_roll_vals[statnames[s]][-1] for s in new_subs]
                new_svals = [sub_roll_vals[statnames[s]][-1] * (r+1) for s, r in zip(new_subs, new_rolls)]

                yield SArti(self.slot, self.main_stat, new_subs, new_svals, pr)
