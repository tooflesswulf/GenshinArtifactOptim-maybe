import sympy as sym

from util.common import statnames, statmap

HP, HPp, DEF, DEFp, ATK, ATKp = sym.symbols('hp hpp def defp atk atkp')
EM, ER, Cr, Cd = sym.symbols('em er cr cd')
phys, pyro, hydro, electro, cryo, geo, anemo = sym.symbols('ph py hy el cy geo an')
heal, dendro = sym.symbols('heal de')
bhp, bdef, batk = sym.symbols('bhp bdef batk')

txt2var = {'HP%': HPp, 'HP': HP, 'DEF%': DEFp, 'DEF': DEF, 'ATK%': ATKp, 'ATK': ATK, 'CR': Cr, 'CD': Cd, 'ER': ER, 'EM': EM, 'Heal': heal,
'Phys': phys, 'Hydro': hydro, 'Pyro': pyro, 'Cryo': cryo, 'Electro': electro, 'Anemo': anemo, 'Geo': geo, 'Dendro': dendro,
'BaseATK': batk, 'BaseHP': bhp, 'BaseDEF': bdef}

class DamageFormula:
    def __init__(self, f0=sym.sympify('0')) -> None:
        self.formula = sym.simplify(f0)
        self.compile()

    def compile(self):
        statorder = [txt2var[n] for n in statnames]
        cmp = sym.lambdify(statorder, self.formula)
        self.compiled = cmp
        return cmp

    def eval(self, stats) -> float:
        return self.compiled(*stats)
    
    def __add__(self, other):
        # new_form = DamageFormula(self.formula + other)
        if isinstance(other, DamageFormula):
            return DamageFormula(self.formula + other.formula)
        return DamageFormula(self.formula + other)
    
    def __radd__(self, other):
        return self + other


class NormalDmg(DamageFormula):
    def __init__(self, mult=0, elem='Phys'):
        tru_atk = batk*(1 + ATKp/1000) + ATK
        formula = mult * tru_atk * (1 + txt2var[elem]/1000) * (1 + Cr/1000 * Cd/1000)
        super().__init__(formula)
