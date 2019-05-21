from nsga2 import nsga2
from recuit_simule import recuit_solver

if __name__ =="__main__":
#    mainSolver = nsga2(100, 30, 5)
#    mainSolver.execute()
    recuitSolver = recuit_solver(150,0.3)
    recuitSolver.solve()
