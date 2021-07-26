import char2
import artifact2

class CumSolver:
    def __init__(self, basestats, dmg):
        self.c = char2.Character(basestats, dmg)
        self.artis = []
        self.dmg_record = []

        self.cur_dmg = self.c.eval()
        self.i = 0

    def step(self, next_arti=None) -> float:
        if next_arti is None:
            next_arti = artifact2.make_arti()
        self.artis.append(next_arti)

        self.i += 1
        self.solve(next_arti)
        self.cur_dmg = self.c.eval()

        self.dmg_record.append(self.cur_dmg)
        
        return self.cur_dmg
    
    # given a new artifact, find a configuration that maximizes the dmg value, returning the dmg.
    def solve(self, new_arti) -> float:
        raise NotImplemented
