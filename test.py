from solvers.TopPerc import TopPerc
from solvers.Top1 import Top1

import numpy as np
import damage
import char2

print('Starting')

diona = [
    0, 0,
    0, 0,
    0, 0,
    50, 500 + 469,
    0, 0,
    0, 0, 0, 0, 240, 0, 0, 0, 0,
    9570, 601, 212 + 401
]
diona = np.array(diona)
formula = damage.NormalDmg(2, elem='Cryo') + damage.NormalDmg(.67, elem='Cryo') + damage.NormalDmg(.2)

# slv = TopPerc(diona, formula)
def proc():
    slv = Top1(diona, formula)
    for _ in range(100):
        slv.step()
        # print(slv.cur_dmg)
    return slv.cur_dmg

dmgs = []
for _ in range(20):
    dmgs.append(proc())
    print(dmgs[-1])
print(f'mean: {np.mean(dmgs)}')


# print(slv.dmg_record)
