from collections.abc import Iterable
from functools import total_ordering
from typing import Union, Tuple
import numpy as np

from util.common import statnames, statmap
import artifact2


@total_ordering
class Loadout:
    artis: Tuple[artifact2.Artifact] = tuple([None for _ in range(5)])  # list of artifacts
    dmg: float = -1

    def __init__(self, artis=None):
        if artis is not None:
            init = [None, None, None, None, None]
            for a in artis:
                if a is None: continue
                init[a.slot] = a
            self.artis = tuple(init)

    def add(self, a):
        if a is None:
            return self
        a0 = list(self.artis)
        a0[a.slot] = a
        return Loadout(a0)

    def _bake(self):
        return sum(map(lambda a: a.tostat() if a is not None else 0, self.artis))

    def __eq__(self, ot):
        return self.artis == ot.artis

    def __lt__(self, ot):
        return self.dmg < ot.dmg

    def __hash__(self):
        return hash(self.artis)

    def __getitem__(self, i):
        return self.artis[i]


stat2ix = lambda l: list(map(statmap.__getitem__, l))
class Character:
    # flat = stat2ix(['HP',  'ATK',  'DEF'])
    # perc = stat2ix(['HP%', 'ATK%', 'DEF%'])
    # unscaled = stat2ix(['HP', 'ATK', 'DEF', 'ER', 'EM'])
    
    def __init__(self, basestats, dmgformula):
        self.base = basestats
        self.formula = dmgformula
        self.artis = Loadout()
    
    def _bake_stats(self):
        arti_stats = self.artis._bake()
        newstats = self.base + arti_stats
        newstats[statmap['CR']] = np.clip(newstats[statmap['CR']], 0, 1000)
        return newstats

        # newstats = (self.base + arti_stats) / 1000
        # for s in Character.unscaled:
        #     newstats[s] *= 1000

        # # Handle HP/ATK/DEF% increase
        # for f, p in zip(Character.flat, Character.perc):
        #     newstats[f] += self.base[f] * newstats[p]

        # Handle crit
        # newstats[statmap['CR']] = np.clip(newstats[statmap['CR']], 0, 1)
        # return newstats

    def eval(self, artifacts=None):
        self.equip(artifacts)
        if self.artis.dmg > 0:
            return self.artis.dmg
        stats = self._bake_stats()
        dmg = self.formula.eval(stats)
        self.artis.dmg = dmg
        return dmg

    def equip(self, arti: Union[Loadout, artifact2.Artifact, Iterable]):
        if isinstance(arti, Loadout):
            self.artis = arti
        elif isinstance(arti, artifact2.Artifact):
            self.artis = self.artis.add(arti)
        elif isinstance(arti, Iterable):
            self.artis = Loadout(arti)
