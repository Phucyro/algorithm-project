import chromosome
import random

class nsga2():

    def __init__(self, nombrePop):

        self.sizePop = nombrePop

        self.population = list()
        self.front = list()


    def init_population(self,seed):
        """" Initialise un certain nombre de resultats aleatoire """

        random.seed(seed)

        for i in range(self.sizePop):

            solution = chromosome.tour(random.randint(0,1000))
            self.population.append(solution)

    def non_dominated_sorting(self):

        firstFront = self.population.copy() #copie la population dans le front 0 (pareto)
        frontIndex = 0

        self.front.append(firstFront)

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

        while frontIndex < 2:

            newFront = list()

            #Debut deplacement solution

            for solution in self.front[frontIndex]:

                if solution.getDominationCount() != 0:

                    toMove.append(solution)

            for solution in toMove:

                newFront.append(solution) #ajout dans le nouveau front
                self.front[frontIndex].remove(solution) #on le retire du front precedent

            #On regarde dans le front en frontIndex pour voir les villes que ses solutions dominent
            #par exemple si la solution non dominee A domine la solution B,C
            # on va decrementer B,C de 1 au niveau du dominationCount

            for solution in self.front[frontIndex]:

                listeDomines = solution.getDominatedList()

                for domines in listeDomines:

                    domines.decrementDominationCount()

            #on rajoute le front dans self.front et on reitere
            self.front.append(newFront)
            frontIndex+=1
            toMove.clear()


        print("Au final: on a donc pour les 3 ranks :")
        k = 0
        for rank in self.front:
            k+=1
            print("Rank {} :".format(k))
            for solution in rank:
                tot_dist, tot_risk = solution.get_total_dist()
                print("Solution avec tot dist {} et tot risk {}".format(tot_dist,tot_risk))


test = nsga2(30)
test.init_population(100)
test.non_dominated_sorting()


