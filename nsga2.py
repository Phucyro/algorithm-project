import chromosome
import random

class nsga2():

    def __init__(self, nombrePop):

        self.sizePop = nombrePop

        self.population = list()
        self.front = list()



    def init_population(self,seed):

        random.seed(seed)

        for i in range(self.sizePop):

            solution = chromosome.tour(random.randint(0,1000))
            self.population.append(solution)

        for ville in self.population:
            tot_dist, mean_risk = ville.get_total_dist()

    def non_dominated_sorting(self):

        firstFront = self.population.copy()

        finished = False
        frontIndex = 0

        self.front.append(firstFront)

        while (not finished):

            newFront = list()
            toMove = list()

            for i in range(len(self.front[frontIndex])):

                for j in range(i+1, len(self.front[frontIndex])):

                    firstChallenger = self.front[frontIndex][i]
                    secondChallenger = self.front[frontIndex][j]

                    if (firstChallenger.dominates(secondChallenger)):
                        firstChallenger.addDominated(secondChallenger)
                        secondChallenger.incrementDominationCount()


                    elif (secondChallenger.dominates(firstChallenger)):
                        secondChallenger.addDominated(firstChallenger)
                        firstChallenger.incrementDominationCount()


            finished = True

        for front in self.front:
            for solution in front:
                solution.print_domination()






test = nsga2(100)
test.init_population(100)
test.non_dominated_sorting()


