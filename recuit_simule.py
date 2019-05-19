from simanneal import Annealer
import chromosome
import random
from matplotlib import pyplot as plt
from matplotlib import style

NBRE_RES = 150 #Number of solutions that is going to be computed
TIME_PER_SOL = 0.02 #Number of minutes allowed to optimize a solution

class recuit(Annealer):

    def __init__(self,state):
        super(recuit,self).__init__(state)

    def move(self): #This function get a neighboor solution of the current solution
        a = random.randint(1, len(self.state.tour) - 1)
        b = random.randint(1, len(self.state.tour) - 1)
        self.state.tour[a], self.state.tour[b] = self.state.tour[b], self.state.tour[a] #Swap two cities in the tour
        return None
    def energy(self):
        return self.state.get_fitness_score()


def get_pareto(list):
    pareto = []
    other = []
    for i in list:
        for j in list:
            if j != i:
                if i.tot_dist > j.tot_dist and i.mean_risk > j.mean_risk :
                    other.append(i)
    for i in list:
        if i not in other:
            pareto.append(i)
    return pareto,other



init_state = chromosome.tour()
rec = recuit(init_state)
auto_schedule = rec.auto(minutes=TIME_PER_SOL)


to_show = []
#This loop compute the values with the annealar simulated algorithm
for i in range(0,NBRE_RES):
    init_state = chromosome.tour()
    rec = recuit(init_state)
    #rec.steps = 41000
    #rec.tmin = 330.0
    #rec.tmax = 330000.0
    #rec.steps = 10000
    rec.set_schedule(auto_schedule)
    it,miles = rec.anneal()
    to_show.append(it)



pareto,other = get_pareto(to_show) #Compute the pareto optimum values

# Get X and Y values for pareto optimum solutions

risk_p = []
dist_p = []
for j in to_show:
    risk_p.append(j.mean_risk)
    dist_p.append(j.tot_dist)


# Get X and Y values for non pareto optimum solutions
risk = []
dist = []
for j in other:
    risk.append(j.mean_risk)
    dist.append(j.tot_dist)


text_file = open(str(NBRE_RES)+"_"+str(TIME_PER_SOL)+".txt", "w")
for i in pareto:
    text_file.write(str(i)+"\n")

text_file.close()


#Make a graph with the soltions
style.use('ggplot')
f, ax = plt.subplots(1)
plt.scatter(risk_p,dist_p,c="blue") # Pareto optimum colored in blue
plt.scatter(risk,dist,c="red") # Other colored in red
plt.title('Annealar')
plt.ylabel('Total Distance (m)')
plt.xlabel('Risk')
plt.autoscale(enable = True,axis='both')
plt.show()
plt.savefig(str(NBRE_RES)+"_"+str(TIME_PER_SOL)+".png")
