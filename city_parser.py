import json

class City():
    def __init__(this,_name,_population,_distances):
        this.name = _name
        this.population = _population
        this.distances = _distances
        this.money = round(this.population*0.70,1)

    def get_dist_to(self,index):
        return self.distances[index]

    def __str__(this):
        return str(this.name) + " a " + str(this.population) + " habitants et engendre " + str(this.money) +" € par mois"

class CityParser():
    """Class to parse populationBrussels.json"""
    def parse(self):
        jsonfile = open("populationBrussels.json")
        data = json.load(jsonfile)
        out = []
        for i in data:
            cur_city = data[i]
            out.append(City(cur_city["name"],cur_city["population"],cur_city["distances"]))
        return out
