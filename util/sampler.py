import numpy as np

class StatSampler:
    def __init__(self, distr, store_rm=True):
        self.k, v = list(distr.keys()), list(distr.values())
        self.cum = np.cumsum(v)
        
        self.distr = distr
        self.sr = store_rm
        if store_rm:
            self.rm_ptrs = {}

        self.float_weights = self.cum / self.cum[-1]
    
    def __call__(self):
        return self.get()
    
    def fget(self, flot):
        return self.k[np.argmax(self.float_weights > flot)]

    def iget(self, iint):
        return self.k[np.argmax(self.cum > iint)]
    
    def get(self):
        sel = np.random.randint(self.cum[-1])
        # ix = np.argmax(self.cum > sel)
        return self.iget(sel)
    
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
