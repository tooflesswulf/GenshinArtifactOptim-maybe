import numpy as np

class StatSampler:
    def __init__(self, distr, store_rm=True):
        self.k, v = list(distr.keys()), list(distr.values())
        self.cum = np.cumsum(v)
        
        self.distr = distr
        self.sr = store_rm
        if store_rm:
            self.rm_ptrs = {}
    
    def __call__(self):
        sel = np.random.randint(self.cum[-1])
        ix = np.argmax(self.cum > sel)
        return self.k[ix]
    
    def get(self):
        return self()
    
    # Removes a key, returning a new Sampler object w/o that key.
    def remove(self, key, prop_rm=False):        
        if key not in self.distr:
            return self
        
        if self.sr and key in self.rm_ptrs:
            return self.rm_ptrs[key]

        dnew = self.distr.copy()
        del dnew[key]
        newsamp = StatSampler(dnew, store_rm=prop_rm)
        if self.sr:
            self.rm_ptrs[key] = newsamp
        return newsamp
