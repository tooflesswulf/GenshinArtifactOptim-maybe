from common import statnames, statmap

import numpy as np
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

class Character:
    def __init__(self, basestats, dmgformula):
        self.base = basestats
        self.formula = dmgformula
        self.artis = [None for _ in range(5)]

    def _arti_stats(self):
        # aggregate all the artifacts first
        arti_stats = Stats()
        for a in self.artis:
            arti_stats += a
        return arti_stats

    def _bake_stats(self):
        newstats = Stats()
        arti_stats = self._arti_stats()

        # bake all the %-stats pls
        weird = [('HP', 'HP%'), ('ATK', 'ATK%'), ('DEF', 'DEF%')]
        for f, p in weird:
            base = self.base[f]
            flat = arti_stats[f]
            perc = self.base[p] + arti_stats[p]
            newstats[f] = base * (1 + perc/1000) + flat
        
        notweird = ['CR', 'CD', 'ER', 'Heal', 'Phys', 'Hydro',
         'Pyro', 'Cryo', 'Electro', 'Anemo', 'Geo', 'Dendro']
        for s in notweird:
            newstats[s] = (self.base[s] + arti_stats[s]) / 1000

        # Crit rate limit is 100%
        if newstats['CR'] >= 1:
            newstats['CR'] = 1
        
        # EM is not like the others :smile:
        newstats['EM'] = self.base['EM'] + arti_stats['EM']
        return newstats
    
    def eval(self, artifacts=None):
        self.equip(artifacts)
        stats = self._bake_stats()
        return self.formula.eval(stats)
    
    def equip(self, arti):
        if isinstance(arti, artifact.Artifact):
            self.artis[arti.slot] = arti
        elif isinstance(arti, list):
            for a in arti:
                self.equip(a)


if __name__ == '__main__':
    import damage
    import random

    diluc = [
        0, 11453,
        0, 692,
        0 + 276, 295 + 565,
        194, 500,
        0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    diluc_stats = Stats(np.array(diluc, dtype=np.float32))
    formula = sum([damage.DilucN1(i) for i in range(4)])

    c = Character(diluc_stats, formula)

    np.random.seed(42)
    random.seed(41)
    artis = [artifact.make_arti() for _ in range(2)]

    e1 = c.eval()
    c.equip(artis)
    e2 = c.eval()

    c.artis = [None, None, None, None, None]
    e3 = c.eval()

    print(e1, e2, e3)
