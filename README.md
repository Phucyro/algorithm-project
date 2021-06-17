## [Project done during my computer sciences studies]

## Context
Brussels region has 19 municipalities. There is still a significant part of the population who pays in cash.
Therefore, each month, armored trucks leave the National Bank and pass by each municipality to recover the money.
These trucks are subject of numerous lusts, especially from thieves and robbers.
This is why the paths taken by these trucks are important.

Let's say that you have three thrucks:

These tours must simultaneously:

-minimize the total distance travelled

-minimize the "risk" which is modeled as the total distance traveled weighted by the total amout of cash present in the truck during the journey.

Constraints:

-At no time may a truck transport more than 50% of the total amount of cash.

-The three most populous municipalities cannot be visited by the same truck.

Design the algorithm and find the optimal Pareto frontier.


## Pre-requis

To install Annealar : pip install simanneal
To install matplotlib : python -m pip install -U matplotlib

## Lancement
Recuit Simule: python recuit_simule.py
NSGA II: python main.py
