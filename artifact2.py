from dataclasses import dataclass, field
from typing import Tuple
import numpy as np
import random
import itertools

from util.common import slotnames, statnames, statmap
from util.sampler import StatSampler

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
sub_vals = {
    'HP': 298.75, 'ATK': 19.45, 'DEF': 23.15, 'HP%': 58.3, 'ATK%': 58.3, 'DEF%': 72.9,
    'EM': 23.31, 'ER': 6.48, 'CR': 38.9, 'CD': 77.7
}

@dataclass(order=True, frozen=True)
class Artifact:
    slot: int
    main_stat: int
    subs:    Tuple[int]  # Fixed length tuples (4), collection of 14 integers.
    subvals: Tuple[int]
    preroll: Tuple[int]
    _stats: np.ndarray = field(init=False, hash=False, compare=False, default=None)

    def __post_init__(self):
        s = np.zeros(len(statnames))
        s[self.main_stat] = main_vals[statnames[self.main_stat]]
        for sub, subv in zip(self.subs, self.subvals):
            s[sub] += subv/10 * sub_vals[statnames[sub]]
        object.__setattr__(self, '_stats', s)

    def tostat(self) -> np.ndarray:
        return self._stats

    def __add__(self, other):
        if isinstance(other, Artifact):
            return self.tostat() + other.tostat()
        raise NotImplemented

    def __repr__(self):
        sub_lst = [f'{statnames[s]}:{vi}>{vf}' for s, vf, vi in zip(self.subs, self.subvals, self.preroll)]
        sub_str = ', '.join(sub_lst)
        return f'{statnames[self.main_stat]} {slotnames[self.slot]}@({sub_str})'

def make_arti(slot=None, sort=True):
    # Pick the slot & main stat first
    if slot is None:
        slot = random.choice([0, 1, 2, 3, 4])
    main_stat = statmap[ mainstat[slot].get() ]

    # Pick substats.
    nodup_distr = substat.remove(statnames[main_stat])
    subs = []
    for _ in range(4):
        ssi = nodup_distr.get()
        subs.append(statmap[ssi])
        nodup_distr = nodup_distr.remove(ssi)

    # Initialize the substats. First upgrade is pulled up to avoid 4-sub logic
    subvals = [random.choice([7,8,9,10]) for _ in range(4)]
    foursub = random.random() > .8
    preroll = subvals.copy()
    if not foursub: preroll[-1] = 0  # 80% chance for 3 subs

    # Roll the substats up; add 5 rolls.
    nroll = 5 if foursub else 4
    vv = [random.choice([7,8,9,10]) for _ in range(nroll)]
    dst = [random.choice([0,1,2,3]) for _ in range(nroll)]
    for i, v in zip(dst, vv):
        subvals[i] += v
    
    if sort:
        # Sort by sub for nicer printing. ~10% increase in runtime
        paired = sorted(zip(subs, preroll, subvals))
        subs, preroll, subvals = list(zip(*paired))
    
    return Artifact(slot=slot, main_stat=main_stat,
            subs=tuple(subs), preroll=tuple(preroll), subvals=tuple(subvals))

keyset = {}
for i in range(5):
    for ks in itertools.combinations(sorted(substat.k), i):
        subsub = substat
        for k in ks:
            subsub = subsub.remove(k)
        keyset[ks] = subsub
improtant = set(substat.k)
def make_from_rvec(v, sort=True):
    slot = int(v[0] * 5) # [0-5] inclusive
    ms = mainstat[slot].fget(v[1])
    disc = {ms} if ms in improtant else set()
    subs = []
    for i in range(2,2+4):
        next_sub = keyset[tuple(sorted(disc))].fget(v[i])
        disc.add(next_sub)
        subs.append(statmap[next_sub])
    foursub = v[6] > .8
    r_pre = int(v[7]*256)
    preroll = [7+r_pre%4, 7+(r_pre//4)%4, 7+(r_pre//16)%4, 7+(r_pre//64)%4]
    
    nroll = 5 if foursub else 4
    subvals = preroll.copy()
    for i in range(8, 8+nroll):
        sbval = int(v[i]*16)
        subvals[sbval%4] += 7+(sbval//4)%4
    if not foursub:
        preroll[-1] = 0

    if sort:
        paired = sorted(zip(subs, preroll, subvals))
        subs, preroll, subvals = list(zip(*paired))
    return Artifact(slot=slot, main_stat=statmap[ms], subs=tuple(subs),
                    subvals=tuple(subvals), preroll=tuple(preroll))

class ArtifactGenerator:
    def __init__(self) -> None:
        pass

    def __iter__(self):
        while True:
            yield make_arti()
