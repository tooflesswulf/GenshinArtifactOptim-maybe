from common import statnames, statmap

import numpy as np
import artifact

class Stats:
    def __init__(self, x: np.ndarray=None):
        if isinstance(x, np.ndarray):
            self.stats = x
        else:
            self.stats = np.zeros(len(statnames), dtype=int)
    
    def __add__(self, other):
        if other is None:
            return self
        elif isinstance(other, artifact.Artifact):
            return self + other.tostat()
        elif isinstance(other, Stats):
            return Stats(self.stats + other.stats)
        else:
            raise NotImplemented
    
    def __radd__(self, left):
        return self + left

    def __repr__(self):
        return str(self.stats)


class Character:
    def __init__(self, basestats, dmgformula):
        self.base = basestats
        self.formula = dmgformula
        self.artis = [None for _ in range(5)]
    
    def _bake_stats(self):
        newstats = np.zeros(len(statnames))

        # aggregate all the artifacts first
        arti_stats = Stats()
        for a in self.artis:
            arti_stats += a

        # bake all the %-stats pls
        weird = [('HP', 'HP%'), ('ATK', 'ATK%'), ('DEF', 'DEF%')]
        for f, p in weird:
            base = self.base[statmap[f]]
            flat = arti_stats[statmap[f]]
            perc = self.base[statmap[p]] + arti_stats[statmap[p]]
            newstats[statmap[f]] = base * (1 + perc/1000) + flat
        
        notweird = ['CR', 'CD', 'ER', 'Heal', 'Phys', 'Hydro',
         'Pyro', 'Cryo', 'Electro', 'Anemo', 'Geo', 'Dendro']
        for s in notweird:
            newstats[statmap[s]] = (self.base[statmap[s]] + arti_stats[statmap[s]]) / 1000
        
        # EM is not like the others :smile:
        newstats[statmap['EM']] = self.base[statmap['EM']] + arti_stats[statmap['EM']]
        return newstats
