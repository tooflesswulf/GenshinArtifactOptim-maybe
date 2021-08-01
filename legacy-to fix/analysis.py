import numpy as np

from common import slotnames, statnames, statmap
import artifact

class ArtifactNB2():
    def __init__(self):
        self.norm = 1
        
        self.main_data = []
        self.sub_data = []
        self.num_arti = []
        for i in range(5):
            mi = {}
            for ms in map(statmap.__getitem__, artifact.mainstat[i].k):
                mi[(ms, True)] = 0
                mi[(ms, False)] = 0
            self.main_data.append(mi)

            si = {}
            for ss in map(statmap.__getitem__, artifact.substat.k):
                si[(ss, True)] = 0
                si[(ss, False)] = 0
            self.sub_data.append(si)

            self.num_arti.append(0)
    
    def summarize(self, a: artifact.Artifact, incl: bool):
        s = a.slot
        main_key = (a.main_stat, incl)
        self.main_data[s][main_key] += 1

        self.num_arti[s] += 1
        if s == 0 and self.main_data[s][(a.main_stat, True)] != 0:  # Flower defines norm
            self.norm = self.num_arti[s] / self.main_data[0][(a.main_stat, True)]

        for ss, p in zip(a.subs, a.preroll):
            if p == 0:
                continue

            sub_key = (ss, incl)
            self.sub_data[s][sub_key] += 1
    
    def __repr__(self):
        retstr = ''
        nn = self.norm
        for s, sn in enumerate(slotnames):

            retstr += f'{sn}:\n  Main:'
            dat = self.main_data[s]
            dsum = []
            for msn in artifact.mainstat[s].k:
                ms = statmap[msn]
                a, b = dat[(ms, True)], dat[(ms, False)]
                dsum.append( (a/(b+1), -b, a, b, msn) )
            dsum = sorted(dsum, reverse=True)
            
            for _, _, a, b, msn in dsum:
                if a + b == 0: continue
                retstr += f' {msn} ({nn * a/(a+b):.02f})'

            retstr += '\n  Subs:'
            dat = self.sub_data[s]
            dsum = []
            for ssn in artifact.substat.k:
                ss = statmap[ssn]
                a, b = dat[(ss, True)], dat[(ss, False)]
                dsum.append( (a/(b+1), -b, a, b, ssn))
            dsum = sorted(dsum, reverse=True)
            for _, _, a, b, ssn in dsum:
                if a + b == 0: continue
                retstr += f' {ssn} ({nn * a/(a+b):.02f})'
            retstr += '\n'
        
        return retstr

class ArtifactNB(dict):
    def __init__(self, default=0):
        self.default = default
        super().__init__()
    
    def __getitem__(self, k):
        if k in self:
            return super().__getitem__(k)
        return self.default
    
    def slic(self, slot=None, stat=None, incl=None):
        def matches(k):
            if slot is not None and k[0] != slot: return False
            if stat is not None and k[1] != stat: return False
            if incl is not None and k[2] != incl: return False
            return True
        
        return {k: self[k] for k in self.keys() if matches(k)}
    
    def summarize(self, a, incl):
        raise NotImplemented
    
class MainstatNB(ArtifactNB):
    def summarize(self, a, incl):
        self[(a.slot, a.main_stat, incl)] += 1

class SubstatNB(ArtifactNB):
    def __init__(self):
        super().__init__(default={})

    def summarize(self, a, incl):
        for s, p in zip(a.subs, a.preroll):
            if p == 0:
                continue

            key = (a.slot, s, incl)
            if key not in self:
                self[key] = {}
            
            if p in self[key]:
                self[key][p] += 1
            else:
                self[key][p] = 1

class SubCountNB(ArtifactNB):
    def summarize(self, a, incl):
        cnt = np.count_nonzero(a.preroll)
        self[(a.slot, cnt, incl)] += 1
