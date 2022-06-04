import yaml
import numpy as np
from Robot import Robot
import random

from World import World

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

world = World()
population = [Robot(world) for _ in range(300)]

bestRobot = Robot(world)

for i in range(1000):
    fitnessArray = np.zeros(len(population))

    # calculate fitness
    for populationIndex in range(len(population)):
        fitness = population[populationIndex].simulate()
        fitnessArray[populationIndex] = fitness
    

    newPop = []

    # tournament selection
    for tournamentIndex in range(int(len(population)*0.8)):
        selectedIndividuous = random.sample(range(0, len(population)-1), len(population)-1) # [0, 5, 56, 32, 3]
        fitnessOfIndividuous = [fitnessArray[inx] for inx in selectedIndividuous] # [-100, 30, 56, 32, 3]
        betterRobot = max(fitnessOfIndividuous)
        betterRobotIndex = fitnessOfIndividuous.index(betterRobot)
        newPop.append(population[selectedIndividuous[betterRobotIndex]])
                
    population = newPop

    fitnessArray = [robot.score for robot in population]
    bestFitness = max(fitnessArray)
    bestRobot = population[fitnessArray.index(bestFitness)]

    # crossover
    for robot in range(int(len(population)*0.25)):
        selectIndCross = random.sample(range(0, len(population)-1), 2) 
        father = population[selectIndCross[0]]
        mother = population[selectIndCross[1]]
        child = father.crossover(mother)
        population.append(child)
    
    # mutation
    if random.randint(0, 100) < 8:
        print(">>>>>>    mutouuuu   <<<<<<")
        print(">>>>>>    mutouuuu   <<<<<<")
        print(">>>>>>    mutouuuu   <<<<<<")
        print(">>>>>>    mutouuuu   <<<<<<")
        print(">>>>>>    mutouuuu   <<<<<<")
        print(">>>>>>    mutouuuu   <<<<<<")
        print(">>>>>>    mutouuuu   <<<<<<")
        indInx = random.randint(0, len(population)-1)
        population[indInx].mutate()
    
    print("population_size: " + str(len(population)))
    print("best_score: " + str(bestRobot.score))
    print("iterations: " + str(i))


print()
print()
print("Best Robot SCORE:" + str(bestRobot.simulate()))