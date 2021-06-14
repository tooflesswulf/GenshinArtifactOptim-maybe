import random

import artifact
from common import statnames, statmap, slotnames

class Annealer:
    def __init__(self, t0, sched=None, s0=None):
        if s0 is None:
            s0 = [make_max_arti(i) for i in range(5)]
        self.s0 = s0
        self.t0 = t0
        self.t = t0
        self.stepnum = 0

        if sched is None:
            self.sched = lambda x: 1/x
        self.sched = lambda x: 1 if x == 0 else sched(x)

    def step(self):
        self.t = self.t0 * self.sched(self.stepnum)
        self.stepnum += 1
    



def make_max_arti(slot=None):
    if slot is None:
        slot = random.choice([0, 1, 2, 3, 4])
    ms = statmap[ random.choice(artifact.mainstat[slot].k) ]

    sub_distr = artifact.substat.remove(statnames[ms])
    subs = random.sample(sub_distr.k, k=4)

    preroll = [artifact.sub_roll_vals[s][-1] for s in subs]
    subvals = preroll.copy()

    # rolling process
    for _ in range(5):
        r = random.choice([0, 1, 2, 3])
        inc = subs[r]
        subvals[r] += artifact.sub_roll_vals[inc][-1]

    subs = tuple(sorted(map(statmap.__getitem__, subs)))
    return artifact.SArti(slot, ms, subs, tuple(subvals), tuple(preroll))

if __name__ == '__main__':
    z = make_max_arti()
    for b in z.get_neighbors():
        print(b)
