import numpy as np
import yaml

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

wall=config["wall"]
rubbish=config["rubbish"]
empty_space=config["empty_space"]

worldSize = config['world_size']
rubbishProbability = config['rubbish_probability']

class World:
  def __init__(self, rubbishProbability=rubbishProbability, worldSize=worldSize):
    self.worldSize = worldSize
    self.rubbishProbability = rubbishProbability

    # creates 10x10 world with random rubbish positions and empty spaces
    self.grid = np.random.choice([empty_space,rubbish], size=(self.worldSize+2,self.worldSize+2), p=(1 - self.rubbishProbability, self.rubbishProbability))

    # sets the walls
    self.grid[:, [0, self.worldSize-1]] = wall
    self.grid[[0, self.worldSize-1], :] = wall

  def printGrid(self, robot):
    for y in range(self.worldSize):
      for x in range(self.worldSize):
          if (x == robot.posX and y == robot.posY):
            print('[R]', end ='')
          else:
            print(f'[{self.grid[y][x]}]', end ='')
      print()
  
  def getRobotVision(self, posX, posY):
    return self.grid[posX, posY - 1] + self.grid[posX - 1, posY] + self.grid[posX, posY + 1] + self.grid[posX + 1, posY] + self.grid[posX, posY]