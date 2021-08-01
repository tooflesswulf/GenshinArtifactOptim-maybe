import numpy as np

slotnames = ['Flower', 'Feath', 'Sands', 'Cup', 'Hat']
# statnames = ['CR', 'CD', 'ER', 'EM', 'ATK%', 'ATK', 'HP%', 'HP', 'DEF%', 'DEF', 'Heal',
statnames = ['HP%', 'HP', 'DEF%', 'DEF', 'ATK%', 'ATK', 'CR', 'CD', 'ER', 'EM', 'Heal',
          'Phys', 'Hydro', 'Pyro', 'Cryo', 'Electro', 'Anemo', 'Geo', 'Dendro',
          'BaseHP', 'BaseDEF', 'BaseATK']
statmap = {n: i for i, n in enumerate(statnames)}

def make_stats(stat_inp: dict):
    global_dmg_bonus = ['Phys', 'Hydro', 'Pyro', 'Cryo', 'Electro', 'Anemo', 'Geo', 'Dendro']

    stats = np.zeros(len(statnames))
    for k, v in stat_inp.items():
        if k == 'Dmg%':
            for k2 in global_dmg_bonus:
                stats[statmap[k2]] += v
            continue
        stats[statmap[k]] += v
    return stats
