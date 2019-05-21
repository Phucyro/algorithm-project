import chromosome
import random
import copy
from matplotlib import pyplot as plt
from matplotlib import style


class nsga2():

    def __init__(self, seed, nombrePop, iterationNumber):

        self.seed = seed
        self.popSize = nombrePop
        self.iterationNumber = iterationNumber
        self.population = list()
        self.front = list()

    def init_population(self):
        """" Init random population solutions with size popSize """

        random.seed(self.seed)

        for i in range(self.popSize):
            solution = chromosome.tour(random.randint(0, 1000))
            self.population.append(solution)

    def non_dominated_sorting(self):
        """ Trie les solutions stockees dans front en fonction du principe de dominance """

        frontIndex = 0

        # Pour tous les elements deux a deux, on regarde qui domine qui

        for i in range(len(self.front[frontIndex])):
            for j in range(i + 1, len(self.front[frontIndex])):

                firstChallenger = self.front[frontIndex][i]
                secondChallenger = self.front[frontIndex][j]

                if (firstChallenger.dominates(secondChallenger)):
                    firstChallenger.addDominated(secondChallenger)
                    secondChallenger.incrementDominationCount()


                elif (secondChallenger.dominates(firstChallenger)):
                    secondChallenger.addDominated(firstChallenger)
                    firstChallenger.incrementDominationCount()

        # On a donc chaque "tour" qui a dominationCount (nombre de solutions qui le dominent)
        # et dominatedList : la liste des solutions qu'il domine

        # liste qui va garder les solutions a deplacer au rank suivant (car dominationCount != 0)

        toMove = list()

        while frontIndex < 3:

            newFront = list()

            # Debut deplacement solution

            for solution in list(self.front[frontIndex]):

                if solution.getDominationCount() != 0:

                    newFront.append(solution)  # ajout dans le nouveau front
                    self.front[frontIndex].remove(solution)  # on le retire du front precedent

                else:

                    # On garde la solution dans le front courant
                    # On regarde dans le front en frontIndex pour voir les villes que ses solutions dominent
                    # par exemple si la solution non dominee A domine la solution B,C
                    # on va decrementer B,C de 1 au niveau du dominationCount

                    listeDomines = solution.getDominatedList()

                    for domines in listeDomines:
                        domines.decrementDominationCount()


            # on rajoute le front dans self.front et on reitere
            self.front.append(newFront)
            frontIndex += 1
            toMove.clear()

        print("Fin dominated sorting:")
        k = 0
        for rank in self.front:
            k += 1
            print("Rank {} :".format(k))
            for solution in rank:
                tot_dist, tot_risk = solution.get_total_dist()
                print("Solution avec tot dist {} et tot risk {}".format(tot_dist, tot_risk))

    def createOffsprings(self):
        """ create offsprings through crossover and population solutions """

        self.front.clear()

        firstFront = copy.deepcopy(self.population)
        self.front.append(firstFront)

        for i in range(len(self.population)):
            for j in range(i + 1, len(self.population)):

                newSolution = copy.deepcopy(self.population[i])
                toCross = copy.deepcopy(self.population[j])

                newSolution.crossover_type_1(toCross)

                if self.findDuplicate(newSolution, self.front[0]):
                    print("Impossible, duplicate found")

                else:
                    print("Solution ajoutee au front [0]")
                    self.front[0].append(newSolution)

                if len(self.front[0]) >= self.popSize:
                    break
                else:
                    continue

            if len(self.front[0]) >= self.popSize:
                break

    def findDuplicate(self, solution, front):
        """ return True if solution already in front """

        duplicate = False

        dist, risk = solution.get_total_dist()

        for sol in front:
            sol_dist, sol_risk = sol.get_total_dist()

            if dist == sol_dist and risk == sol_risk:
                duplicate = True

        return duplicate

    def combineAndSort(self):
        """ combine population and front and use the non dominated sorting """

        for pop in self.population:
            self.front[0].append(copy.deepcopy(pop))

        self.non_dominated_sorting()

    def choosePopulation(self):
        """ choose next generation population (no duplicate) """

        self.population.clear()

        for rank in self.front:

            for solution in rank:
                # check if the current solution is already in population
                if not self.findDuplicate(solution, self.population):   
                    if len(self.population) < self.popSize:
                        self.population.append(solution)
                    else:
                        return None


    def showResultPareto(self):
        """ print pareto frontier results """

        print("End result :")

        k = 0
        risk_p = []
        dist_p = []

        for rank in self.front:
            k += 1

            if k != 1:
                print("Rank {} non parreto :".format(k))
            else:
                print("Rank Parreto!")

            risk_p.append([])
            dist_p.append([])
            for solution in rank:
                tot_dist, tot_risk = solution.get_total_dist()
                if k == 1:
                    risk_p[0].append(tot_risk)
                    dist_p[0].append(tot_dist)
                else:
                    risk_p[k-1].append(tot_risk)
                    dist_p[k-1].append(tot_dist)
                print("Solution avec tot dist {} et tot risk {}".format(tot_dist, tot_risk))
        self.createPlot(risk_p, dist_p)

    def createPlot(self, risk_p, dist_p):
        
        """text_file = open(str(self.popSize)+"_"+str(TIME_PER_SOL)+".txt", "w")
        for i in pareto:
            text_file.write(str(i)+"\n")

        text_file.close()

        soltions_to_csv(pareto, "AnnealerSimulated")"""

        #Make a graph with the soltions
        style.use('ggplot')
        f, ax = plt.subplots(1)
        plt.scatter(risk_p[0],dist_p[0],c="blue") # Pareto optimum colored in blue
        plt.scatter(risk_p[1],dist_p[1],c="yellow") # Front 2 colored in yellow
        plt.scatter(risk_p[2],dist_p[2],c="green") # Front 3 colored in green
        plt.scatter(risk_p[3],dist_p[3],c="red") # Front 4 colored in red
        plt.title('NSGA II')
        plt.ylabel('Total Distance (m)')
        plt.xlabel('Risk')
        plt.autoscale(enable = True,axis='both')
        plt.savefig(str(self.popSize)+"_str(TIME_PER_SOL).png")
        plt.show()

    def execute(self):

        self.init_population()

        i = 0
        while (i < self.iterationNumber):

            self.createOffsprings()
            self.combineAndSort()
            self.choosePopulation()

            i+=1

        self.showResultPareto()









