from dataclasses import dataclass, field
from functools import total_ordering
from typing import Tuple, Dict
import numpy as np

from common import statnames, statmap
import artifact

class Stats:
    def __init__(self, x: np.ndarray=None):
        if isinstance(x, np.ndarray):
            self.stats = x
        elif isinstance(x, list):
            self.stats = np.array(x)
        elif isinstance(x, Stats):
            self.stats = x.stats.copy()
        else:
            self.stats = np.zeros(len(statnames), dtype=np.float32)
    
    def __add__(self, other):
        if other is None:
            return self
        elif isinstance(other, artifact.Artifact):
            return Stats(self.stats + other.tostat().stats)
        elif isinstance(other, Stats):
            return Stats(self.stats + other.stats)
        else:
            raise NotImplemented
    
    def __radd__(self, left):
        return self + left

    def __repr__(self):
        return str(self.stats)
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.stats[statmap[key]]
        elif isinstance(key, int):
            return self.stats[key]
    
    def __setitem__(self, key, nv):
        if isinstance(key, str):
            self.stats[statmap[key]] = nv
        elif isinstance(key, int):
            self.stats[key] = nv

@dataclass
@total_ordering
class Loadout:
    artis: Tuple[artifact.Artifact] = tuple([None for _ in range(5)])  # list of artifacts
    # dmgCache: Dict[int, float] = field(default_factory=dict)
    dmg: int = -1

    def _bake(self):
        s = Stats()
        for a in self.artis:
            s += a
        return s

    def add(self, a):
        if a is None:
            return self
        a0 = list(self.artis)
        a0[a.slot] = a
        return Loadout(artis=tuple(a0))
    
    def __eq__(self, ot):
        return self.artis == ot.artis
    
    def __lt__(self, ot):
        return self.dmg < ot.dmg
    
    def __hash__(self):
        return hash(self.artis)


if __name__ == '__main__':
    print(Loadout())
