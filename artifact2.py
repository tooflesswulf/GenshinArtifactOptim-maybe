from dataclasses import dataclass, field
from typing import Tuple, Iterator
import numpy as np
import random
import itertools

from util.common import slotnames, slotmap, statnames, statmap, mainstat, main_vals, substat, sub_vals, to_stat
from util.common import SetKey, StatKey, SlotKey


@dataclass(order=True, frozen=True)
class ISubstat:
    key: StatKey
    value: int

    def __iter__(self) -> Iterator[StatKey|int]:
        return iter((self.key, self.value))


@dataclass(order=True, frozen=True)
class Artifact:
    setKey: SetKey
    slotKey: SlotKey
    mainStatKey: StatKey
    substats: Tuple[ISubstat] = ()
    level: int = 1
    rarity: int = 5
    lock: bool = False
    location: None = None
    exclude: None = None
    _stats: np.ndarray = field(
        init=False, hash=False, compare=False, default=None)
    rolls_left: int = 5

    def __post_init__(self):
        object.__setattr__(self, 'rolls_left', (23-self.level)//4)
        s = np.zeros(len(statnames))
        # s[self.main_stat] = main_vals[statnames[self.main_stat]]
        for k, v in self.substats:
            if k == '':
                object.__setattr__(self, 'rolls_left', self.rolls_left - 1)
                continue
            s[statmap[k]] = v/10 * sub_vals[k]
        object.__setattr__(self, '_stats', s)

    def tostat(self, sub_only=False) -> np.ndarray:
        if sub_only:
            return self._stats
        # Imma just assume lvl 20 everything
        main = to_stat({self.mainStatKey: main_vals[self.mainStatKey]})
        return self._stats + main
        
    def __add__(self, other):
        if isinstance(other, Artifact):
            return self.tostat() + other.tostat()
        if isinstance(other, np.ndarray):
            return self.tostat() + other
        raise NotImplemented
    
    def __radd__(self, other):
        print(f'ther: {other}')
        return self + other

    def __repr__(self):
        out = f'LVL{self.level} {self.setKey} {self.slotKey} @ {self.mainStatKey}'
        for k, v in self.substats:
            if k == '':
                continue
            val_disp = v/10*sub_vals[k]
            if val_disp < 1:
                out += f'\n - {val_disp*100:.1f} {k}'
            else:
                out += f'\n - {val_disp:.0f} {k}'
        return out


def make_arti(setKey='MaidenBeloved', slot=None, upgrade=True, foursub_prob=.8, sort=True) -> Artifact:
    if slot is None:
        slot = random.choice([0, 1, 2, 3, 4])
    slotKey = slot
    if slot in slotnames:
        slot = slotmap[slot]
    else:
        slotKey = slotnames[slot]
    main_stat = mainstat[slot].get()

    # Pick substats.
    nodup_distr = substat.remove(main_stat)
    subs = []
    for _ in range(4):
        ssi = nodup_distr.get()
        subs.append(ssi)
        nodup_distr = nodup_distr.remove(ssi)

    # Initialize the substats. First upgrade is pulled up to avoid 4-sub logic
    subvals = [random.choice([7, 8, 9, 10]) for _ in range(4)]
    foursub = random.random() > foursub_prob

    if not upgrade:
        # If not upgrade, then we can generate the artifact now.
        if not foursub:
            subs[-1] = ''
            subvals[-1] = 0
        lvl = 1

    else:
        lvl = 20
        # Otherwise, upgrade the artifact.
        nroll = 5 if foursub else 4
        vv = [random.choice([7, 8, 9, 10]) for _ in range(nroll)]
        dst = [random.choice([0, 1, 2, 3]) for _ in range(nroll)]
        for i, v in zip(dst, vv):
            subvals[i] += v
    paired = zip(subs, subvals)
    if sort:
        paired = sorted(zip(subs, subvals))
    substats = tuple(ISubstat(s, sv) for s, sv in paired)
    return Artifact(setKey=setKey, slotKey=slotKey, level=lvl, rarity=5, mainStatKey=main_stat, substats=substats)


class ArtifactGenerator:
    def __init__(self) -> None:
        pass

    def __iter__(self):
        while True:
            yield make_arti()


def cvt_good_isubtat(isub):
    k, v = isub['key'], isub['value']
    if k == '':
        return ISubstat(k, 0)

    int_val = int(np.round(10 * v / sub_vals[k]))
    # GOOD does x% as 10.3%, I use 0.103
    if int_val > 650:
        int_val = int(np.round(int_val / 100))
    return ISubstat(k, int_val)

# From GOOD object description format (v2)
def from_good(good_arti):
    good_arti['substats'] = tuple(map(cvt_good_isubtat, good_arti['substats']))
    return Artifact(**good_arti)

if __name__ == '__main__':
    tst = {"setKey": "Thundersoother", "rarity": 5, "level": 1, "slotKey": "flower", "mainStatKey": "hp", "substats": [{"key": "def", "value": 23}, {
        "key": "atk", "value": 18}, {"key": "critRate_", "value": 3.9}, {"key": "", "value": 0}], "location": "", "exclude": False, "lock": False}
    a = from_good(tst)
    print(a)
    print(a.rolls_left)

    a = make_arti(upgrade=False)
    print(a)
    print(a.rolls_left)
