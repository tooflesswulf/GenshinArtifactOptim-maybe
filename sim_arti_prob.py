import artifact2
import util.common as c
import numpy as np

# Target information
arti_slot = 1  # Feather
mainstat = c.statmap['ATK']
subtargs = {
    'CD': 26  # CD >= 20.2%
}

print(f'{c.slotnames[arti_slot]} @ {c.statnames[mainstat]}')
for k,v in subtargs.items():
    print(f'{k} >= {v*artifact2.sub_vals[k]/10}')

def predicate(a: artifact2.Artifact):
    if a.slot != arti_slot:
        return False

    if a.main_stat != mainstat:
        return False
    for k, v in subtargs.items():
        k2 = c.statmap[k]
        if k2 not in a.subs:
            return False
        ki = a.subs.index(k2)
        if a.subvals[ki] < v:
            return False

    return True

def sim(n=1_000_000, pred=predicate, return_artis=False):
    c = 0
    artis = []
    for _ in range(n):
        if _ % 100 == 0:
            print(f'Making {_}/{n}...', end='\r')
        a = artifact2.make_arti()
        if return_artis:
            artis.append(a)
        if pred(a):
            c += 1

    if return_artis:
        return c/n, artis

    return c / n


if __name__ == '__main__':
    print('\n')
    print(sim())
