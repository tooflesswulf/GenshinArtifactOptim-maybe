from common import statnames, statmap

class DamageFormula:
    def eval(self, stats=None) -> float:
        raise NotImplemented
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return ConstDamage(other) + self
        elif isinstance(other, DamageFormula):
            return SumDamage([self, other])
        else:
            raise NotImplemented
    
    def __radd__(self, other):
        return self + other


class ConstDamage(DamageFormula):
    def __init__(self, c):
        self.c = c
    
    def eval(self, stats=None):
        return self.c


class SumDamage(DamageFormula):
    def __init__(self, formulas):
        self.fs = list(formulas)
    
    def eval(self, stats=None):
        return sum([f.eval(stats) for f in self.fs])

    def __add__(self, other):
        self.fs.append(other)
        return self


class NormalDmg(DamageFormula):
    def __init__(self, mult=0, elem='Phys'):
        self.m = mult
        self.elem = statmap[elem]
    
    def eval(self, stats):
        s_atk = stats[statmap['ATK']]
        s_cr = stats[statmap['CR']]
        s_cd = stats[statmap['CD']]
        s_ele = stats[self.elem]

        dmg = self.m * s_atk * (1+s_ele)
        return dmg * (1 + s_cr * s_cd)


class DilucN(NormalDmg):
    # Normal multipliers, C6
    def __init__(self, i, q_infuse=False):
        mults = [1.3, 1.27, 1.44, 1.95]

        el = 'Pyro' if q_infuse else 'Phys'
        super().__init__(mults[i], el)

class DilucQ(NormalDmg):
    def __init__(self):
        super().__init__(mult=2.86, elem='Pyro')

class DilucE(NormalDmg):
    def __init__(self, i):
        mults = [1.32, 1.37, 1.80]
        super().__init__(mults[i], 'Pyro')

class DionaCharged(DamageFormula):
    def __init__(self, weak_prob=.5):
        self.p_weak = weak_prob

    def eval(self, stats=None):
        s_atk = stats[statmap['ATK']]
        s_cr = stats[statmap['CR']]
        s_cd = stats[statmap['CD']]
        s_cryo = stats[statmap['Cryo']]

        weakpoint_prob = self.p_weak
        wk_bonus = 1.48
        bolide = 1.4
        dmg = 2.11 * s_atk * (1+s_cryo) * bolide
        no_weak = dmg * (1 + s_cr * s_cd)
        weak = dmg * wk_bonus * (1 + s_cd)
        return weakpoint_prob*weak + (1-weakpoint_prob)*no_weak
