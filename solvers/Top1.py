from solvers.solverbase import CumSolver

class Top1(CumSolver):
    def solve(self, a):
        replaced = self.c.artis[a.slot]
        self.c.equip(a)
        new_dmg = self.c.eval()

        if new_dmg < self.cur_dmg:
            self.c.equip(replaced)

        return max(new_dmg, self.cur_dmg)
