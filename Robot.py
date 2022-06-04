import random as rd
import numpy as np
import yaml
import time

# import settings
with open("config.yaml", "r") as yamlfile:
  config = yaml.safe_load(yamlfile)
  
wallPenalty = config["wall_penalty"]
emptyCatchingPenalty = config["empty_catching_penalty"]
reward = config["reward"]
mutationRate = config["mutation_rate"]
totalMoves = config["total_moves"]

wall=config["wall"]
rubbish=config["rubbish"]
empty_space=config["empty_space"]

# MOVEMENTS
up = config['north']
down = config['south']
right = config['east']
left = config['west']
random = config['random']
no_movement = config['no_movement']
catch_rubbish = config['catch_rubbish']

class Robot:
  def __init__(self, world, dna=None, wallPenalty=wallPenalty, emptyCatching=emptyCatchingPenalty, reward=reward, mutationRate=mutationRate, totalMoves=totalMoves):
    self.posY = 1
    self.posX = 1

    self.world = world

    self.score = 0

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

    return Robot(self.world, newDna)

  def mutate(self):
    dnaMutationPositions = rd.sample(range(0, self.dna.__len__()-1), 14)
    for dnaPosition in dnaMutationPositions:
      dnaArr = list(self.dna)
      dnaArr[dnaPosition] = str(rd.randint(0, 6))
      self.dna = ''.join(str(d) for d in dnaArr)
     
  
  def simulate(self):
    for i in range(totalMoves):
      self.move()

    return self.score
      

  def move(self):
    robotVision = self.world.getRobotVision(self.posX, self.posY)
    currentSituation = self.situations[robotVision]
    robotAction = self.dna[currentSituation]

    if robotAction == 4:
      robotAction = np.random.choice([up, down, right, left])
    
    if robotAction == up:
      self.moveUp(robotVision[0])
    elif robotAction == down:
      self.moveDown(robotVision[2])
    elif robotAction == right:
      self.moveRight(robotVision[3])
    elif robotAction == left:
      self.moveLeft(robotVision[1])
    elif robotAction == catch_rubbish:
      self.catchRubbish()

  def moveUp(self, robotVision):
    if self.doWallPenalty(robotVision): 
      return
    self.posY = self.posY - 1

  def moveDown(self, robotVision):
    if self.doWallPenalty(robotVision): 
      return
    self.posY = self.posY + 1
    
  def moveRight(self, robotVision):
    if self.doWallPenalty(robotVision): 
      return
    self.posX = self.posX + 1

  def moveLeft(self, robotVision):
    if self.doWallPenalty(robotVision): 
      return
    self.posX = self.posX - 1
    

  def catchRubbish(self):
    wasSucceeded = self.world.removeRubbish(self.posX, self.posY)
    if wasSucceeded:
      self.score += reward
    else:
      self.score += emptyCatchingPenalty

  def doWallPenalty(self, robotVision):
    if robotVision == wall:
      self.score += wallPenalty
      return True
    else:
      return False

