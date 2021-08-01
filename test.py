from solvers.TopPerc import TopPerc

import numpy as np
import damage
import char2

print('Starting')

diona = [
    0, 9570,
    0, 601,
    0, 212 + 401,
    50, 500 + 469,
    0, 0,
    0, 0, 0, 0, 240, 0, 0, 0, 0,
]
diona = np.array(diona)
formula = damage.NormalDmg(2, elem='Cryo') + damage.NormalDmg(.67, elem='Cryo') + damage.NormalDmg(.2)

slv = TopPerc(diona, formula)
for _ in range(200):
    slv.step()
    print(slv.cur_dmg)

print(slv.dmg_record)
