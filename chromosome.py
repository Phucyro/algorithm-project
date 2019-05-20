import random
import city_parser

class tour():
    """docstring for chromosome."""


    def __init__(self, seed=None):
        self.tour = [i for i in range(1,20)]
        #random.seed(seed)
        random.shuffle(self.tour)
        #liste de 4 ints commencant par 0, mais pas de 0 en index 1
        self.camion = self.set_camion()

        self.cities = city_parser.CityParser().parse()
        self.TOT_MONEY = 0
        for i in self.cities:
            self.TOT_MONEY += i.money #Compute the total money available

        while not self.respect_constraint(): #Create a random solution that respect the constraint
            random.shuffle(self.tour)
            self.camion = self.set_camion()

        self.tot_dist,self.mean_risk = self.get_total_dist() #Compute the risk and distane

        self.mean_risk /= 10000

        self.mean_risk = round(self.mean_risk,3)

        self.undergoDominationCount = 0

        self.dominatesList = list()

    def __str__(self):
        out = ""
        for i in range(0,3):
            out += "The truck " + str(i+1) +" goes through : "
            for j in range(self.camion[i],self.camion[i+1]):
                out += self.cities[self.tour[j]].name + ", "
            out += "\n"
        out += "And the mean risk of this tour is : "+str(self.mean_risk) + " with a total distance of : " + str(self.tot_dist)
        return out


    def change_to_neighboor(self):
        """This function turn the solution into one of her neighboor"""
        a = random.randint(1, len(self.tour) - 1)
        b = random.randint(1, len(self.tour) - 1)
        self.tour[a], self.tour[b] = self.tour[b], self.tour[a] #Swap two self.cities in the tour
        while not self.respect_constraint():
                a = random.randint(1, len(self.tour) - 1)
                b = random.randint(1, len(self.tour) - 1)
                self.tour[a], self.tour[b] = self.tour[b], self.tour[a] #Swap two self.cities in the tour


    def get_total_dist(self):
        """This function compute the risk and the total distance of the solution"""
        tot_dist = 0
        tot_risk = []

        for i in range(0,3): #0,1,2
            risk = []
            previous = 0
            cur_money = 0

            for j in range(self.camion[i],self.camion[i+1]):
                dist= self.cities[previous].get_dist_to(self.tour[j])
                tot_dist += dist
                cur_money += self.cities[previous].money
                risk.append(cur_money*dist)
                previous = self.tour[j]
            tot_dist += self.cities[previous].get_dist_to(0)
            tot_risk.append(self.mean(risk))

        return (tot_dist,round(self.mean(tot_risk),2))

    def crossover_type_1(self,other):
        """Make a cycle crossover between two solutions"""
        cycles = self.detect_cycle(self.tour,other.tour) #Get the cycle in the two solutions
        child1 = [0 for i in range(0,19)]
        child2 = [0 for i in range(0,19)]
        count = 0
        for i in cycles: #This loop create the two children with the cycles
            if count%2 == 0:
                for j in i:
                    child1[self.tour.index(j)] = j
                    child2[other.tour.index(j)] = j

            else:
                for j in i:
                    child2[self.tour.index(j)] = j
                    child1[other.tour.index(j)] = j
            count += 1

        return None
    def crossover_type_2(self,other):
        #Ecrire different type de crossover
        return None
    def crossover_type_3(self,other):
        #Ecrire different type de crossover
        return None
    def detect_cycle(self,chrom1,chrom2):
        """This function detect the cycle in 2 solutions"""
        used = list()
        out = list()
        cur_cycle = list()
        for i in chrom1:
            cur_cycle = []
            if i not in used:
                while i not in cur_cycle:
                    cur_cycle.append(i)
                    used.append(i)
                    i = chrom2[chrom1.index(i)]

                out.append(cur_cycle)
        print(out)
        return out

    def get_fitness_score(self):
        """This fucntion return the fitness score of the solution (The lower the better)"""
        self.tot_dist,self.mean_risk = self.get_total_dist()
        self.mean_risk /= 10000
        self.mean_risk = round(self.mean_risk,3)
        return self.tot_dist + self.mean_risk

    def set_camion(self):
        """This function divide the solutions in 3 part (for 3 trucks)"""
        camion = [0,0,19]
        while not self.all_unique(camion):
            previous = 1
            for i in range(0,2):
                previous = random.randint(previous,18)
                camion[i] = previous
        camion.insert(0,0)
        return camion

    def all_unique(self,list):
        """This function check that all element in a list are unique"""
        list_c = list.copy()

        for i in list_c:
            list_c.pop(list_c.index(i))
            if i in list_c:
                return False

        if (list[0] == 0): #Eviter d'avoir le premier camion qui ne fait pas de trajet
            return False

        return True

    def mean(self,list):
        if len(list) > 0:
            return sum(list) / float(len(list))
        else:
            return 0

    def respect_constraint(self):
        """Check if no truck goes through the 3 biggest cities (1,2,10) and if no truck
        carries more than the half of all the money available"""
        trucks = []
        for i in range(0,3): #This loop create a list of list (one list = one truck tour)
            truck = []
            for j in range(self.camion[i],self.camion[i+1]):
                truck.append(self.tour[j])
            trucks.append(truck)
        for i in trucks:
            money = 0
            if 1 in i and 2 in i and 10 in i: #Check if the truck don't goes through the 3 biggest cities
                    return False
            for j in i:
                money += self.cities[self.tour[j-1]].money
            if money >= self.TOT_MONEY/2: #Check if the truck doesn't carry more than the half of all the money
                return False
        return True





    def dominates(self, other):

        distValue, riskValue = self.get_total_dist()

        otherDistValue , otherRiskValue = other.get_total_dist()

        """
        print("distValue : {}, riskValue : {}".format(distValue, riskValue))
        print("otherDistValue: {}, otherRiskValue: {}".format(otherDistValue, otherRiskValue))
        """

        if (distValue <= otherDistValue and riskValue <= otherRiskValue) and (distValue < otherDistValue or riskValue < otherRiskValue):
            return True
        else:
            return False


    def addDominated(self, dominated):
        self.dominatesList.append(dominated)

    def removeDominated(self, dominated):
        self.dominatesList.remove(dominated)

    def incrementDominationCount(self):
        self.undergoDominationCount += 1

    def decrementDominationCount(self):
        self.undergoDominationCount -= 1

    def print_domination(self):
        print("nombre de solutions qu on domine {} et nombre de dominations subies {}".format(len(self.dominatesList), self.undergoDominationCount))

    def getDominationCount(self):
        return self.undergoDominationCount

    def getDominatedList(self):
        return self.dominatesList


""""
print(test)
test2 = tour(400)
print(test2)

print("crossover")
test.crossover_type_1(test2)
print(test)
"""
