from simanneal import Annealer
import chromosome
import random
import city_parser
from matplotlib import pyplot as plt
from matplotlib import style

NBRE_RES = 20 #Number of solutions that is going to be computed
TIME_PER_SOL = 0.2 #Number of minutes allowed to optimize a solution

class recuit(Annealer): #We use simanneal that implement the Annealer Simulated algorithm

    def __init__(self,state):
        super(recuit,self).__init__(state)

    def move(self): #This function get a neighboor solution of the current solution
        self.state.change_to_neighboor()

    def energy(self): #This function get the "energy" of the solution
        return self.state.get_fitness_score()


def get_pareto(list):
    """This function get the pareto optimum solutions from a list of solutions """
    pareto = []
    other = []
    for i in list:
        for j in list:
            if j != i:
                if i.tot_dist > j.tot_dist and i.mean_risk > j.mean_risk : #If solution i is dominated by atleast one solution it's not part of the pareto
                    other.append(i)
    for i in list:
        if i not in other: #Every solution that is not dominated is part of the pareto
            pareto.append(i)
    return pareto,other

def soltions_to_csv(solutions,name):
    """This function create a CSV file with all the solution from a list of solutions"""
    cities = city_parser.CityParser().parse()
    output = open(str(name)+".csv", "w")
    for a in solutions:
        for i in range(0,3): #iterate on each truck
            output.write("0;")
            money = "0;"
            curr_money = 0
            for j in range(a.camion[i],a.camion[i+1]):
                output.write(str(a.tour[j])+";")
                curr_money += cities[a.tour[j]].money
                money += str(round(curr_money,2))+";"
            output.write("0;\n")
            output.write(money+"\n")



init_state = chromosome.tour()
rec = recuit(init_state)
auto_schedule = rec.auto(minutes=TIME_PER_SOL) #Get the parameters so that every solutions in computed in TIME_PER_SOL * minutes


to_show = []
#This loop compute the values with the annealar simulated algorithm
for i in range(0,NBRE_RES):
    print(str(i)+"/"+str(NBRE_RES)+"\n")
    init_state = chromosome.tour() #Create a random solution
    rec = recuit(init_state) #Create the Annealer simulation
    rec.set_schedule(auto_schedule) #Set the max / min temperature and the nbre of steps
    it,miles = rec.anneal() #Run the simulation
    to_show.append(it)



pareto,other = get_pareto(to_show) #Compute the pareto optimum values

# Get X and Y values for pareto optimum solutions

risk_p = []
dist_p = []
for j in pareto:
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

soltions_to_csv(pareto, "AnnealerSimulated")

#Make a graph with the soltions
style.use('ggplot')
f, ax = plt.subplots(1)
plt.scatter(risk_p,dist_p,c="blue") # Pareto optimum colored in blue
plt.scatter(risk,dist,c="red") # Other colored in red
plt.title('Annealar')
plt.ylabel('Total Distance (m)')
plt.xlabel('Risk')
plt.autoscale(enable = True,axis='both')
plt.savefig(str(NBRE_RES)+"_"+str(TIME_PER_SOL)+".png")
plt.show()
