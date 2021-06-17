import numpy as np
from typing import Union

from common import statnames, statmap
import artifact
import stats

class Character:
    def __init__(self, basestats, dmgformula):
        self.base = basestats
        self.formula = dmgformula
        self.artis = stats.Loadout()

    def _bake_stats(self):
        newstats = stats.Stats()
        arti_stats = self.artis._bake()

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
        dmg = self.formula.eval(stats)
        self.artis.dmg = dmg
        # self.artis.dmgCache[0] = dmg #  Cache the dmg. TODO: hashable formula
        return dmg
    
    def equip(self, arti: Union[stats.Loadout, artifact.Artifact]):
        if isinstance(arti, stats.Loadout):
            self.artis = arti
        elif isinstance(arti, artifact.Artifact):
            self.artis = self.artis.add(arti)

if __name__ == '__main__':
    import damage
    import solver
    import random

    diluc = [
        0, 11453,
        0, 692,
        0 + 276, 295 + 565,
        194, 500,
        0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    diluc_stats = stats.Stats(np.array(diluc, dtype=np.float32))
    formula = sum([damage.DilucN1(i) for i in range(4)])

    slv = solver.TopPerc(diluc_stats, formula)

    for _ in range(20):
        slv.step()
