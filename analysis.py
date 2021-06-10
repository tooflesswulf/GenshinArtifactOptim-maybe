import numpy as np

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
