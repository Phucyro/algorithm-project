import chromosome
import random
import copy

import numpy as np
import random as rn


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

                self.front[0].append(newSolution)

                if len(self.front[0]) >= self.popSize:
                    break
                else:
                    continue

            if len(self.front[0]) >= self.popSize:
                break


    def combineAndSort(self):

        for pop in self.population:

            self.front[0].append(copy.deepcopy(pop))

        self.non_dominated_sorting()

    def choosePopulation(self):

        self.population.clear()
        print(self.front)
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

                tot_dist, tot_risk = solution.get_total_dist()
                print("Solution avec tot dist {} et tot risk {}".format(tot_dist, tot_risk))

    def calculate_crowding(self, scores):
        # Crowding is based on a vector for each individual
        # All dimension is normalised between low and high. For any one dimension, all
        # solutions are sorted in order low to high. Crowding for chromsome x
        # for that score is the difference between the next highest and next
        # lowest score. Total crowding value sums all crowding for all scores

        population_size = len(scores[0])
        number_of_scores = len(scores[:])

        # create crowding matrix of population (row) and score (column)
        crowding_matrix = np.zeros((population_size, number_of_scores))

        # normalise scores (ptp is max-min)
        normed_scores = (scores - scores.min(0)) / scores.ptp(0)

        # calculate crowding distance for each score in turn
        for col in range(number_of_scores):
            crowding = np.zeros(population_size)

            # end points have maximum crowding
            crowding[0] = 1
            crowding[population_size - 1] = 1

            # Sort each score (to calculate crowding between adjacent scores)
            sorted_scores = sorted(normed_scores[:, col], key=lambda x: [x.tot_dist, x.mean_risk], reverse=True)

            sorted_scores_index = np.argsort(
                normed_scores[:, col])

            # Calculate crowding distance for each individual
            crowding[1:population_size - 1] = \
                (sorted_scores[2:population_size] -
                sorted_scores[0:population_size - 2])

            # resort to orginal order (two steps)
            re_sort_order = np.argsort(sorted_scores_index)
            sorted_crowding = crowding[re_sort_order]

            # Record crowding distances
            crowding_matrix[:, col] = sorted_crowding

        # Sum crowding distances of each score
        crowding_distances = np.sum(crowding_matrix, axis=1)

        return crowding_distances

    def reduce_by_crowding(self, scores, number_to_select):
        # This function selects a number of solutions based on tournament of
        # crowding distances. Two members of the population are picked at
        # random. The one with the higher croding dostance is always picked
        scores = np.array(self.front)
        number_to_select = self.popSize - 1
        population_ids = np.arange(scores.shape[0])

        crowding_distances = self.calculate_crowding(scores)

        picked_population_ids = np.zeros((number_to_select))

        picked_scores = np.zeros((number_to_select, len(scores[0, :])))

        for i in range(number_to_select):

            population_size = population_ids.shape[0]

            fighter1ID = rn.randint(0, population_size - 1)

            fighter2ID = rn.randint(0, population_size - 1)

            # If fighter # 1 is better
            if crowding_distances[fighter1ID] >= crowding_distances[
                fighter2ID]:

                # add solution to picked solutions array
                picked_population_ids[i] = population_ids[
                    fighter1ID]

                # Add score to picked scores array
                picked_scores[i, :] = scores[fighter1ID, :]

                # remove selected solution from available solutions
                population_ids = np.delete(population_ids, (fighter1ID), axis=0)

                scores = np.delete(scores, (fighter1ID), axis=0)

                crowding_distances = np.delete(crowding_distances, (fighter1ID), axis=0)
            else:
                picked_population_ids[i] = population_ids[fighter2ID]

                picked_scores[i, :] = scores[fighter2ID, :]

                population_ids = np.delete(population_ids, (fighter2ID), axis=0)

                scores = np.delete(scores, (fighter2ID), axis=0)

                crowding_distances = np.delete(
                    crowding_distances, (fighter2ID), axis=0)
                
        # Convert to integer
        picked_population_ids = np.asarray(picked_population_ids, dtype=int)
        return (picked_population_ids)

test = nsga2(30)
test.init_population(100)

i=0

while (i<5):

    test.createOffsprings()
    test.combineAndSort()
    test.reduce_by_crowding(0,0)

    i+=1







