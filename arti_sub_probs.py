from artifact2 import substat
import math

class Frac:
    def __init__(self, a, b):
        gcd = math.gcd(a, b)
        self.p = a//gcd
        self.q = b//gcd
    
    def __add__(self, ot):
        if isinstance(ot, Frac):
            new_denom = self.q*ot.q
            return Frac(self.p*ot.q + ot.p*self.q, new_denom)
        elif ot == 0:
            return self
    
    def __mul__(self, ot):
        if isinstance(ot, Frac):
            return Frac(self.p*ot.p, self.q*ot.q)
        elif ot == 0:
            return 0
        elif ot == 1:
            return self
    
    def __radd__(self, ot):
        return self + ot

    def __repr__(self):
        return f'{self.p} / {self.q}'
    
def prob(distr, subs, depth=0):
    if len(subs) == 0:
        return 1
    elif depth == 4:
        return 0

    denom = int(distr.cum[-1])
    pps = []
    for k, v in distr.distr.items():
        dnext = distr.remove(k)
        p = Frac(v, denom)
        # p = v/denom
        nxtsub = subs.copy()
        if k in subs:
            nxtsub.remove(k)
        pz = prob(dnext, nxtsub, depth+1)
        pps.append(p * pz)
    
    return sum(pps, start=Frac(0,1))

import itertools
import sys

if len(sys.argv) > 1:
    mainstat = sys.argv[1]
else:
    mainstat = None

# feather
mainstat = 'ATK'
ss = substat.remove('ATK')
subs = {'CD'}
print(f'P(CD|ms=ATK) = {prob(ss, subs)}')

# ss = substat
# if mainstat is not None:
#     ss = substat.remove(mainstat)
# keys = substat.k
# for kk in itertools.combinations(keys, 4):
#     sel = set(kk)
#     # print(sel)
#     print(f'={prob(ss, sel)}')


# for ms in ['HP', 'DEF', 'ATK', 'HP%', 'DEF%', 'ATK%', 'ER', 'EM', 'CR', 'CD']:
#     kke = substat.remove(ms)