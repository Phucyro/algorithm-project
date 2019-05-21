import city_parser

def solutions_to_csv(solutions,name):
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