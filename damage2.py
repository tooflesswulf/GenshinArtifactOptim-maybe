import numpy as np

from util.common import statnames, statmap


class DamageFormula:
    def __init__(self, funcs=None) -> None:
        # gradient and hessians required.
        if funcs is None:
            self.formulae = []
        else:
            self.formulae = funcs

    def eval(self, stats) -> float:
        dmg = 0
        grad = 0
        hess = 0
        for f in self.formulae:
            v, g, h = f(stats)
            dmg += v
            grad += g
            hess += h
        return dmg, grad, hess

    def __add__(self, other):
        if isinstance(other, DamageFormula):
            newfs = self.formulae.copy()
            newfs.extend(other.formulae)
            return DamageFormula(newfs)

        raise TypeError(f'Cannot add types [{type(self)}] and [{type(other)}]')

    def __mul__(self, other):
        if isinstance(other, DamageFormula):
            def newf(st):
                f1, g1, h1 = self.eval(st)
                f2, g2, h2 = other.eval(st)

                fprime = f1 * f2
                gprime = f1 * g2 + f2 * g1
                hprime = f1 * h2 + f2 * h1 + \
                    np.outer(g1, g2) + np.outer(g2, g1)
                return fprime, gprime, hprime
            return DamageFormula([newf])

        if type(other) == int or type(other) == float:
            def newf(st):
                f, g, h = self.eval(st)
                return other * f, other * g, other * h

            return DamageFormula([newf])

        raise TypeError(f'Cannot mul types [{type(self)}] and [{type(other)}]')

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other


class NormalDmg(DamageFormula):
    def __init__(self, mult=1):
        def f(stats):
            i1 = statmap['BaseATK']
            i2 = statmap['ATK']
            i3 = statmap['ATK%']

            batk = stats[i1]
            atk = stats[i2]
            atkp = stats[i3]
            dmg = batk * (1 + atkp/1000) + atk

            gr = np.zeros(len(statnames))
            gr[i1] = 1 + atkp/1000
            gr[i2] = 1
            gr[i3] = batk / 1000

            Hh = np.zeros([len(statnames), len(statnames)])
            Hh[i1, i3] = Hh[i3, i1] = 1/1000
            return mult * dmg, mult * gr, mult * Hh

        super().__init__([f])


class CritMult(DamageFormula):
    def __init__(self):
        def f(stats):
            # 1 + cr * cd
            i1 = statmap['CR']
            i2 = statmap['CD']

            cr = stats[i1] / 1000
            cd = stats[i2] / 1000
            if cr > 1:
                mult = 1 + cd
                gr = np.zeros(len(statnames))
                gr[i2] = 1/1000
                Hh = np.zeros([len(statnames), len(statnames)])
                return mult, gr, Hh

            mult = 1 + cr * cd
            gr = np.zeros(len(statnames))
            gr[i1] = cd / 1000
            gr[i2] = cr / 1000

            Hh = np.zeros([len(statnames), len(statnames)])
            Hh[i1, i2] = Hh[i2, i1] = 1 / 1000 / 1000
            return mult, gr, Hh
        super().__init__([f])


class VapeMelt(DamageFormula):
    def __init__(self, mult=2, bonus=0):
        def f(stats):
            i = statmap['EM']
            em = stats[i]

            div = 1 / (em + 1400)
            m = mult * (1 + 2.78 * em * div + bonus)
            gr = np.zeros(len(statnames))
            gr[i] = mult * 2.78 * 1400 * (div**2)
            Hh = np.zeros([len(statnames), len(statnames)])
            Hh[i, i] = -mult * 2.78 * 2800 * (div**3)
            return m, gr, Hh
        super().__init__([f])

class DmgBonus(DamageFormula):
    def __init__(self, elem, bonus=0):
        def f(stats):
            i = statmap[elem]
            bon = stats[i] / 1000
            gr = np.zeros(len(statnames))
            gr[i] = 1 / 1000
            Hh = np.zeros([len(statnames), len(statnames)])
            return 1 + bon + bonus, gr, Hh
        super().__init__([f])
