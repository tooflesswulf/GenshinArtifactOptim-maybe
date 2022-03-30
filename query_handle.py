from typing import Sequence
import numpy as np
import itertools
import scipy.special
import scipy.stats
import numpy as np
import util.lookup_fns as lookup_fns

from util.definitions import statnames, statmap, slotnames, slotmap
import artifact2
import damage2


def coeff2normal(ks, N: int = 5, b: int = 1) -> tuple[float, float]:
    # Get Gaussian approximation from Ai coefficients
    ks = np.array(ks)
    n4b = N + 4*b
    mu = 17/8*n4b * np.sum(ks)
    var = (5/16*n4b + N*289/16)*np.sum(ks**2) - N*(17/8*np.sum(ks))**2
    return mu, var


def prob_gt(x, mu, var):
    if np.isclose(var, 0):
        if mu > x:
            return 1
        return 0
    return scipy.special.erfc((x - mu) / np.sqrt(2 * var)) / 2


def probdmg_gt(x, mu, var):
    if np.isclose(var, 0):
        if mu > x:
            return np.array([1, mu - x])
        return np.array([0, 0])
    p = scipy.special.erfc((x - mu) / np.sqrt(2 * var)) / 2
    if np.isclose(p, 0):
        return np.array([p, 0])
    phi = np.exp(-(x-mu)**2 / var/2)/np.sqrt(2*np.pi)
    return np.array([p, mu + np.sqrt(var) * phi / p - x])


def appx_hessian2(H, k=1):
    # Finds linear approximation of 4x4 Hessian
    a = np.sum(H) + np.trace(H)
    b = np.sum(H, axis=0) + np.diag(H)

    lhs = np.zeros(5)
    lhs[1:] = k / 7 * (a + 2*b)
    lhs[0] = k / 6 * a

    rhs_inv = 1 + np.eye(5)
    rhs_inv[:, 0] = -6
    rhs_inv[0, :] = -k
    rhs_inv[0, 0] = 5*k
    gv = rhs_inv @ lhs
    return gv[0], gv[1:]


class QueryHandle:
    def __init__(self, char_stats: np.ndarray, artis: Sequence[artifact2.Artifact], dmg: damage2.DamageFormula):
        self.dmg = dmg
        self.ch = char_stats
        self.a = artis

        self.query: artifact2.Artifact = None
        self.dmg0, _, _ = self.dmg.eval(
            self.ch + sum([a.tostat() for a in self.a]))

    def _set_query(self, query_arti: artifact2.Artifact):
        self.query = query_arti
        self.vgh = self.dmg.eval(self._stat())

    def _stat(self):
        ret = self.ch
        for a in self.a:
            if a.slotKey == self.query.slotKey:
                ret = ret + self.query.tostat()
                continue
            ret = ret + a.tostat()

        # TODO: handle set bonus and other conditionals
        return ret

    def linearize(self, subs: Sequence[artifact2.ISubstat], rolls=5):
        if self.query is None:
            raise RuntimeError('Need a query first!')
        hg_ixs = [statmap[k] for k, v in subs if k != '']

        # TODO: do taylor expansion around mean substat upgrade?
        #  Currently expanding about upgrade=0
        v, g, h = self.vgh

        scale = np.array([artifact2.sub_vals[k]/10 for k, v in subs if k != ''])

        gnorm = g[hg_ixs] * scale
        hnorm = h[hg_ixs][:, hg_ixs] * np.outer(scale, scale)
        if len(hg_ixs) == 3:
            # force the thing to be 4x4.
            gnorm = np.append(gnorm, 0)
            hnorm = np.pad(hnorm, [0, 1])

        c0, h_lin = appx_hessian2(hnorm, k=10*rolls)
        return v + c0, gnorm + h_lin / 2

    def eval_arti(self, a: artifact2.Artifact, est_dmg=False):
        self._set_query(a)

        c, m = self.linearize(a.substats, a.rolls_left)
        mu, var = coeff2normal(m, N=a.rolls_left, b=0)
        if est_dmg:
            return probdmg_gt(self.dmg0 - c, mu, var)
        return prob_gt(self.dmg0 - c, mu, var)

    def _resolve_lpd(self, lpd, est_dmg=False):
        if est_dmg:
            ptot, dtot = 0, 0
            for l, (p, d) in lpd:
                ptot += l*p
                dtot += l*p*d
            if np.isclose(ptot, 0):
                return 0, 0
            return ptot, dtot/ptot
        return np.sum(np.prod(lpd, axis=1))

    def eval_sub(self, subs: Sequence[artifact2.ISubstat], p3sub=.8, est_dmg=False):
        rolls_left = 5 + 4
        c, m = self.linearize(subs, rolls_left)

        def pd(mu, var):
            if est_dmg:
                return probdmg_gt(self.dmg0 - c, mu, var)
            return prob_gt(self.dmg0 - c, mu, var)

        lpd = []
        mu3, var3 = coeff2normal(m, N=4, b=1)
        lpd.append([p3sub, pd(mu3, var3)])

        mu4, var4 = coeff2normal(m, N=4, b=1)
        lpd.append([1-p3sub, pd(mu4, var4)])
        return self._resolve_lpd(lpd, est_dmg)

    def eval_slot(self, slot, setKey=None, p3sub=.8, est_dmg=False):
        if slot in slotnames:
            slot = slotmap[slot]
        main_distr = artifact2.mainstat[slot].distr
        main_denom = sum(main_distr.values())

        lpd = []
        for main, v_main in main_distr.items():
            p_main = v_main / main_denom
            self._set_query(artifact2.Artifact(
                setKey=setKey, slotKey=slotnames[slot], mainStatKey=main))

            sub_distr = artifact2.substat
            sub_distr = sub_distr.remove(main)
            for c in itertools.combinations(sub_distr.k, 4):
                prb = p_main * lookup_fns.p_subs(c, main)
                c2 = tuple(artifact2.ISubstat(cc, 0) for cc in c)
                lpd.append(
                    [prb, self.eval_sub(c2, p3sub=p3sub, est_dmg=est_dmg)])
        return self._resolve_lpd(lpd, est_dmg)

    # def dmg_per_arti(self, p3sub=.8):
    #     lpd = []
    #     for i in range(5):
    #         lpd.append([1/5, self.eval_slot(i, p3sub=p3sub, E=True)])
    #     p, d = self._resolve_lpd(lpd, E=True)
    #     return -d * p * np.log(p) / (1-p)


if __name__ == '__main__':
    # Stats of lvl 90 Diona w/ protype crescent
    diona_stats = np.zeros(len(statnames))
    diona_stats[statmap['hp']] = 9570
    diona_stats[statmap['base_atk']] = 722
    diona_stats[statmap['atk_']] = .413
    diona_stats[statmap['def']] = 601
    diona_stats[statmap['critRate_']] = .050
    diona_stats[statmap['critDMG_']] = .500
    diona_stats[statmap['enerRech_']] = 1.000
    diona_stats[statmap['cryo_dmg_']] = .240

    flower = artifact2.Artifact(setKey='RetracingBolide', slotKey='flower', mainStatKey='hp',
                                level=20, substats=(
                                    artifact2.ISubstat('atk', 17),
                                    artifact2.ISubstat('def', 7),
                                    artifact2.ISubstat('eleMas', 35),
                                    artifact2.ISubstat('critDMG_', 18),)
                                )
    feather = artifact2.Artifact(setKey='RetracingBolide', slotKey='plume', mainStatKey='atk',
                                 level=20, substats=(
                                     artifact2.ISubstat('enerRech_', 25),
                                     artifact2.ISubstat('def', 16),
                                     artifact2.ISubstat('critRate_', 8),
                                     artifact2.ISubstat('critDMG_', 25),)
                                 )
    sands = artifact2.Artifact(setKey='RetracingBolide', slotKey='sands', mainStatKey='eleMas',
                               level=20, substats=(
                                   artifact2.ISubstat('hp', 18),
                                   artifact2.ISubstat('def', 17),
                                   artifact2.ISubstat('critRate_', 32),
                                   artifact2.ISubstat('critDMG_', 10),)
                               )
    cup = artifact2.Artifact(setKey='RetracingBolide', slotKey='goblet', mainStatKey='cryo_dmg_',
                             level=20, substats=(
                                 artifact2.ISubstat('hp_', 8),
                                 artifact2.ISubstat('atk_', 19),
                                 artifact2.ISubstat('enerRech_', 34),
                                 artifact2.ISubstat('eleMas', 7),)
                             )
    hat = artifact2.Artifact(setKey='RetracingBolide', slotKey='circlet', mainStatKey='critRate_',
                             level=20, substats=(
                                 artifact2.ISubstat('hp', 10),
                                 artifact2.ISubstat('critDMG_', 20),
                                 artifact2.ISubstat('atk_', 18),
                                 artifact2.ISubstat('eleMas', 24),
                             ))

    dmg = damage2.NormalDmg(2.23) * damage2.CritMult() * \
        damage2.VapeMelt(1.5) * damage2.DmgBonus('cryo_dmg_')
    stats = diona_stats + flower.tostat() + feather.tostat() + sands.tostat() + \
        cup.tostat() + hat.tostat()

    q1 = artifact2.Artifact(setKey='GladiatorsFinale', slotKey='sands', mainStatKey='eleMas',
                            level=1,  substats=(
                                   artifact2.ISubstat('critDMG_', 7),
                                   artifact2.ISubstat('hp', 9),
                                   artifact2.ISubstat('atk_', 8),
                                   artifact2.ISubstat('atk', 7),
                            ))
    q2 = artifact2.Artifact(setKey='GladiatorsFinale', slotKey='sands', mainStatKey='eleMas',
                            level=1,  substats=(
                                   artifact2.ISubstat('critDMG_', 8),
                                   artifact2.ISubstat('critRate_', 9),
                                   artifact2.ISubstat('hp', 10),
                                   artifact2.ISubstat('atk', 7),
                            ))

    curr_loadout = [flower, feather, sands, cup, hat]
    qh = QueryHandle(diona_stats, curr_loadout, dmg)
    # print(qh.dmg0)

    tot = 0
    for z in range(1000):
        tot += qh.eval_arti(artifact2.make_arti(slot='plume'))
    print(tot / 1000)

    print(qh.eval_slot('plume'))
