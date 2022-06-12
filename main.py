import yaml
import numpy as np
from Robot import Robot
import random
import sys

from World import World

def roulette_select(population, fitnesses, num):
    """ Roulette selection, implemented according to:
        <http://stackoverflow.com/questions/177271/roulette
        -selection-in-genetic-algorithms/177278#177278>
    """
    total_fitness = float(sum(fitnesses))
    rel_fitness = [f/total_fitness for f in fitnesses]
    # Generate probability intervals for each individual
    probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
    # Draw new population
    new_population = []
    for n in iter(range(num)):
        r = np.random.rand()
        for (i, individual) in enumerate(population):
            if r <= probs[i]:
                new_population.append(individual)
                break
    return new_population

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

world = World()
population = [Robot(world) for _ in range(500)]

bestRobot = Robot(world)

for i in range(300):
    fitnessArray = np.zeros(len(population))

    # calculate fitness
    for populationIndex in range(len(population)):
        fitness = population[populationIndex].simulate()
        fitnessArray[populationIndex] = fitness
    

    newPop = []

    # tournament selection
    # for tournamentIndex in range(int(len(population)*0.8)):
    #     selectedIndividuous = random.sample(range(0, len(population)-1), len(population)-1) # [0, 5, 56, 32, 3]
    #     fitnessOfIndividuous = [fitnessArray[inx] for inx in selectedIndividuous] # [-100, 30, 56, 32, 3]
    #     betterRobot = max(fitnessOfIndividuous)
    #     betterRobotIndex = fitnessOfIndividuous.index(betterRobot)
    #     newPop.append(population[selectedIndividuous[betterRobotIndex]])

    #roullete selection
    newPop = roulette_select(population, fitnessArray, int(len(population)*0.60))
                
    population = newPop

    fitnessArray = [robot.score for robot in population]
    bestFitness = max(fitnessArray)
    bestRobot = population[fitnessArray.index(bestFitness)]

    # crossover
    for robot in range(int(len(population)*0.7)):
        selectIndCross = random.sample(range(0, len(population)-1), 2) 
        father = population[selectIndCross[0]]
        mother = population[selectIndCross[1]]
        child = father.crossover(mother)
        population.append(child)
    
    #mutation chance
    if random.randint(0, 100) < 8:
        indInx = random.randint(0, len(population)-1)
        population[indInx].mutate()

    
    print("population_size: " + str(len(population)))
    print("best_score: " + str(bestRobot.score))
    print("iterations: " + str(i))


print()
print()
print("Best Robot SCORE:" + str(bestRobot.simulate()))