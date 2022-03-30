import numpy as np
import json

import artifact2
from util.definitions import statnames, statmap
from dataclasses import dataclass, fields


def dataclass_from_dict(klass, d):
    try:
        if klass == artifact2.Artifact:
            return artifact2.from_good(d)
    except:
        raise ValueError(f'Artifact load failed: {d}')
    try:
        if klass.__origin__ == tuple:
            # class is tuple
            subklass, = klass.__args__
            return tuple(dataclass_from_dict(subklass, item) for item in d)
    except:
        pass

    try:
        fieldtypes = {f.name: f.type for f in fields(klass)}
        op = {}
        for f in d.keys():
            if f not in fieldtypes:
                continue
            op[f] = dataclass_from_dict(fieldtypes[f], d[f])
        return klass(**op)
    except:
        # print(f'LOADING FAILED: {d}')
        # raise ValueError(f'Loading failed for {d}')
        return d  # Not a dataclass field


@dataclass(order=True, frozen=True)
class Talent:
    auto: int
    skill: int
    burst: int


@dataclass(order=True, frozen=True)
class Character:
    key: str  # CharacterKey
    level: int
    constellation: int
    ascension: int
    talent: Talent

    def tostat(self):
        print(f'WARNING: characters stat load NOT IMPLEMENTED. Doing manual load.')
        print(f' - diona LVL90')
        diona_stats = np.zeros(len(statnames))
        diona_stats[statmap['hp']] = 9570
        diona_stats[statmap['base_atk']] = 212
        diona_stats[statmap['def']] = 601
        diona_stats[statmap['critRate_']] = .050
        diona_stats[statmap['critDMG_']] = .500
        diona_stats[statmap['enerRech_']] = 1.000
        diona_stats[statmap['cryo_dmg_']] = .240
        return diona_stats



@dataclass(order=True, frozen=True)
class Weapon:
    key: str  # WeaponKey
    level: int
    ascension: int
    refinement: int
    location: None = None
    lock: bool = False

    def tostat(self):
        print(f'WARNING: weapon stat load NOT IMPLEMENTED. Doing manual load.')
        print(f' - Prototype Crescent R5 LVL90 (passive on)')
        crescent_stats = np.zeros(len(statnames))
        crescent_stats[statmap['base_atk']] = 510
        crescent_stats[statmap['atk_']] = .413
        # passive on
        crescent_stats[statmap['atk_']] += .72
        return crescent_stats


@dataclass(order=True, frozen=True)
class GOODB:
    format: str
    source: str
    version: int
    characters: tuple[Character] = None
    weapons: tuple[Weapon] = None
    artifacts: tuple[artifact2.Artifact] = None

    def __repr__(self):
        return f'Imported DB from {self.source}\n' + \
            f' - {len(self.characters)} chars\n' + \
            f' - {len(self.weapons)} weapons\n' + \
            f' - {len(self.artifacts)} artis\n'


def load_chars(chars):
    out = {}
    print(f'CHARACTERS IMPORT NOT IMPLEMENTED. Doing manual load.')
    print(f' - diona LVL90')
    diona_stats = np.zeros(len(statnames))
    diona_stats[statmap['hp']] = 9570
    diona_stats[statmap['base_atk']] = 212
    diona_stats[statmap['def']] = 601
    diona_stats[statmap['critRate_']] = .050
    diona_stats[statmap['critDMG_']] = .500
    diona_stats[statmap['enerRech_']] = 1.000
    diona_stats[statmap['cryo_dmg_']] = .240
    out['diona'] = diona_stats

    return out


def load_weap(weaps):
    out = {}
    print(f'WEAPONS IMPORT NOT IMPLEMENTED. Doing manual load.')

    print(f' - Prototype Crescent R5 LVL90 (passive on)')
    crescent_stats = np.zeros(len(statnames))
    crescent_stats[statmap['base_atk']] = 510
    crescent_stats[statmap['atk_']] = .413
    # passive on
    crescent_stats[statmap['atk_']] += .72

    out['PrototypeCrescent'] = crescent_stats
    return [crescent_stats]


def load_json(file) -> GOODB:
    with open(file, 'r') as f:
        # f.read()
        out = json.loads(f.read())
    return dataclass_from_dict(GOODB, out)

if __name__ == '__main__':
    db = load_json('good1.json')
    print(db)
