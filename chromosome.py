import random
import city_parser

class tour():
    """docstring for chromosome."""

    def __init__(self, seed):
        self.tour = [i for i in range(1,20)]
        random.seed(seed)
        random.shuffle(self.tour)
        self.camion = self.set_camion()
        self.tot_dist,self.mean_risk = self.get_total_dist()
        self.mean_risk /= 1000
        self.mean_risk = round(self.mean_risk,3)

    def __str__(self):
        cities = city_parser.CityParser().parse()
        out = ""
        for i in range(0,3):
            out += "Le camion " + str(i+1) +" passe par (En partant de la BN et en revenant a la BN) : "
            for j in range(self.camion[i],self.camion[i+1]):
                out += cities[self.tour[j]].name + ", "
            out += "\n"
        out += "And the mean risk of this tour is : "+str(self.mean_risk) + " with a total distance of : " + str(self.tot_dist)
        return out


    def get_total_dist(self):
        previous = 0
        tot_dist = 0
        tot_risk = []
        cities = city_parser.CityParser().parse()

        for i in range(0,3):
            risk = []
            for j in range(self.camion[i],self.camion[i+1]):
                dist= cities[previous].get_dist_to(self.tour[j])
                tot_dist += dist
                risk.append(cities[previous].money*dist)
                previous = self.tour[j]
            tot_dist += cities[previous].get_dist_to(0)
            tot_risk.append(self.mean(risk))

        return (tot_dist,round(self.mean(tot_risk),2))

    def crossover_type_1(self,other):
        cycles = self.detect_cycle(self.tour,other.tour)
        child1 = [0 for i in range(0,19)]
        child2 = [0 for i in range(0,19)]
        count = 0
        for i in cycles:
            print(i)
            if count%2 == 0:
                for j in i:
                    child1[self.tour.index(j)] = j
                    child2[other.tour.index(j)] = j

            else:
                for j in i:
                    child2[self.tour.index(j)] = j
                    child1[other.tour.index(j)] = j
            count += 1
        print(child1)
        print(child2)
        return None
    def crossover_type_2(self,other):
        #Ecrire different type de crossover
        return None
    def crossover_type_3(self,other):
        #Ecrire different type de crossover
        return None
    def detect_cycle(self,chrom1,chrom2):
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
        return None

    def set_camion(self):
        camion = [0,0,19]
        while not self.all_unique(camion):
            previous = 0
            for i in range(0,2):
                previous = random.randint(previous,18)
                camion[i] = previous
        camion.insert(0,0)
        return camion

    def all_unique(self,list):
        list_c = list.copy()
        for i in list_c:
            list_c.pop(list_c.index(i))
            if i in list_c:
                return False
        return True

    def mean(self,list):
        return sum(list)/float(len(list))


test = tour(59)
print(test)
test2 = tour(4194)
print(test2)