import numpy as np
import yaml

# import settings
with open("config.yaml", "r") as yamlfile:
  config = yaml.safe_load(yamlfile)
  
wallPenalty = config["wall_penalty"]
emptyCatching = config["empty_catching"]
reward = config["reward"]
mutationRate = config["mutation_rate"]
totalMoves = config["total_moves"]

wall=config["wall"]
rubbish=config["rubbish"]
empty_space=config["empty_space"]

# MOVEMENTS
north = config['north']
south = config['south']
east = config['east']
west = config['west']
random = config['random']
no_movement = config['no_movement']
catch_rubbish = config['catch_rubbish']

CARDINALS=[north, south, east, west]

class Robot:
  def __init__(self, world, dna=None, wallPenalty=wallPenalty, emptyCatching=emptyCatching, reward=reward, mutationRate=mutationRate, totalMoves=totalMoves):
    self.posY = 1
    self.posX = 1

    self.world = world

    self.dna = dna == None and ''.join(str(rand) for rand in np.random.randint(7, size=243)) or dna

    self.wallPenalty = wallPenalty
    self.emptyCatching=emptyCatching
    self.reward=reward
    self.mutationRate=mutationRate
    self.totalMoves = totalMoves

    # generate json with 
    spaceStates = [wall, empty_space, rubbish] # wall, empty, rubbish
    self.situations = dict()
    count = 0
    for up in spaceStates:
        for right in spaceStates:
            for down in spaceStates:
                for left in spaceStates:
                    for robotPosition in spaceStates:
                        self.situations[up+right+down+left+robotPosition] = count
                        count += 1
  
  def crossover(self, robot):
    newDna = ''

    for i in range(122):
      newDna = newDna + self.dna[i]

    for i in range(121):
      newDna = newDna + robot.dna[i]

    return Robot(newDna)
  

  def move(self):
    robotVision = self.world.getRobotVision(self.posX, self.posY)
    currentSituation = self.situations[robotVision]
    robotAction = self.dna[currentSituation]

    if robotAction == 4:
      robotAction = np.random.choice([north, south, east, west])
      
    if robotAction == north:
      self.moveNorth()
    elif robotAction == south:
      self.moveSouth()
    elif robotAction == east:
      self.moveEast()
    elif robotAction == west:
      self.moveWest()

  def moveNorth(self):
    self.posY = self.posY - 1

  def moveSouth(self):
    self.posY = self.posY + 1
    
  def moveEast(self):
    self.posX = self.posX + 1

  def moveWest(self):
    self.posX = self.posX - 1
