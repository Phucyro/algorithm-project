import chromosome
import random
import copy

class nsga2():

    def __init__(self, nombrePop):

        self.popSize = nombrePop

        self.population = list()
        self.front = list()



    def init_population(self,seed):
        """" Initialise un certain nombre de resultats aleatoire """

        random.seed(seed)

        for i in range(self.popSize):

            solution = chromosome.tour(random.randint(0,1000))
            self.population.append(solution)


    def non_dominated_sorting(self):

        frontIndex = 0

        #Pour tous les elements deux a deux, on regarde qui domine qui
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

        #On a donc chaque "tour" qui a dominationCount (nombre de solutions qui le dominent)
        # et dominatedList : la liste des solutions qu'il domine

        #liste qui va garder les solutions a deplacer au rank suivant (car dominationCount != 0)
        toMove = list()

        while frontIndex < 3:

            newFront = list()

            """solutionNonDominatedInFrontIndex = True

            for solution in self.front[frontIndex]:
                if solution.getDominationCount == 0:
                    solutionNonDominatedInFrontIndex = False

            if solutionNonDominatedInFrontIndex == False:
                break"""

            #Debut deplacement solution
            #print(str(len(self.front[frontIndex])) + "\n ----------") 
            for solution in list(self.front[frontIndex]):

                if solution.getDominationCount() != 0:

                    newFront.append(solution) #ajout dans le nouveau front
                    self.front[frontIndex].remove(solution) #on le retire du front precedent
                else:
                    listeDomines = solution.getDominatedList()

                    for domines in listeDomines:

                        domines.decrementDominationCount()

            #for solution in toMove:
            #print(len(newFront))
            #print(len(self.front[frontIndex]))    

            #On regarde dans le front en frontIndex pour voir les villes que ses solutions dominent
            #par exemple si la solution non dominee A domine la solution B,C
            # on va decrementer B,C de 1 au niveau du dominationCount

            #for solution in self.front[frontIndex]:

                

            #on rajoute le front dans self.front et on reitere
            self.front.append(newFront)
            frontIndex+=1
            toMove.clear()


        print("Fin dominated sorting:")
        k = 0
        for rank in self.front:
            k+=1
            print("Rank {} :".format(k))
            for solution in rank:
                tot_dist, tot_risk = solution.get_total_dist()
                print("Solution avec tot dist {} et tot risk {}".format(tot_dist,tot_risk))


    def createOffsprings(self):

        self.front.clear()

        firstFront = copy.deepcopy(self.population)
        self.front.append(firstFront)

        for i in range(len(self.population)):
            for j in range(i+1, len(self.population)):

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

        duplicate = False

        dist, risk = solution.get_total_dist()

        for sol in front:
            sol_dist, sol_risk = sol.get_total_dist()

            if dist == sol_dist and risk == sol_risk:
                print("Duplicate found")
                duplicate = True

        return duplicate


    def combineAndSort(self):

        for pop in self.population:

            self.front[0].append(copy.deepcopy(pop))

        self.non_dominated_sorting()

    def choosePopulation(self):

        self.population.clear()

        for rank in self.front:
            for solution in rank:

                if len(self.population) < self.popSize:
                    self.population.append(solution)

                else:
                    break

            if len(self.population) >= self.popSize:
                break

    def showResultPareto(self):

        k=0
        for rank in self.front:

            k += 1
            if k != 1:
                print("Rank {} non parreto :".format(k))
            else:
                print("Rank Parreto!")

            for solution in rank:

                print(solution)

test = nsga2(30)
test.init_population(100)

i=0

while (i<10):

    test.createOffsprings()
    test.combineAndSort()
    test.choosePopulation()

    i+=1


test.showResultPareto()





