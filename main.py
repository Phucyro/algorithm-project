from nsga2 import nsga2

if __name__ =="__main__":
    mainSolver = nsga2(100, 30, 5)
    mainSolver.execute()