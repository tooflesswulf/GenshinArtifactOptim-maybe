from typing import Sequence

import artifact2
import damage2
from GOOD_importer import Weapon, Character, load_json
from util.lookup_fns import mu, sigma, p_subs
from util.definitions import slotnames, slotmap
from query_handle import QueryHandle


def char_lookup(chars: Sequence[Character], chKey: str):
    for c in chars:
        if c.key == chKey:
            return c
    raise KeyError(f'Key not found: {chKey}')


def weapon_lookup(weaps: Sequence[Weapon], chKey: str):
    for w in weaps:
        if w.location == chKey:
            return w
    raise KeyError(f'Key not found: {chKey}')


def arti_lookup(artis: Sequence[artifact2.Artifact], chKey: str) -> list[artifact2.Artifact]:
    out = []
    for a in artis:
        if a.location == chKey:
            out.append(a)
    return out

if __name__ == '__main__':
    info_str = """
    ############################################################
    ##                  DEMO 2.                               ##
    ##    Given a character and a single dmg objective,       ##
    ##   estimate the probability that randomly farming       ##
    ##   a new flower/feather/etc will improve the objective  ##
    ############################################################
    """
    print(info_str)
    db = load_json('good1.json')

    diona = char_lookup(db.characters, 'Diona')
    weap = weapon_lookup(db.weapons, diona.key)
    artis = arti_lookup(db.artifacts, diona.key)

    base_stat = diona.tostat() + weap.tostat()
    print('WARNING: damage formula loading NOT IMPLEMENTED. Manually entered')
    print(' - Diona Charge shot (no headshot) melt')
    print('WARNING: no set bonuses for this demo')
    dmg = damage2.NormalDmg(2.23) * damage2.CritMult() * damage2.VapeMelt(1.5) * damage2.DmgBonus(['cryo_dmg_', 'ca_dmg_'])
    qh = QueryHandle(base_stat, artis, dmg)

    print('\n\n')

    print('Diona\'s current equipment:')
    artis = sorted(artis, key=lambda x: slotmap[x.slotKey])
    lines = []
    for a in artis:
        lines.append([f'{l:30s}' for l in str(a).splitlines()])
    # lines = [repr(a) for a in artis]
    for l in zip(*lines):
        print(*l, sep='')

    print(f'\navg DMG: {qh.dmg0}\n\n')

    print(f'Probability that a new XXX will improve the objective')
    probs = []
    for s in slotnames:
        p = qh.eval_slot(s)
        print(f'{s}\t{p:.05f}')
        probs.append(p)

    exp = 5 / sum(probs)
    print(f'\n\nExpected # artifacts farmed to improve objective: {exp}')


    # evals = []
    # for a in db.artifacts:
    #     # print(a)
    #     evals.append((qh.eval_arti(a), a))

    # evals = sorted(evals)
    # for p, a in sorted(evals)[:-5:-1]:
    #     print(f'P ≈ {p:.03f}\n{repr(a)}\n')

