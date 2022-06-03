import yaml
import time 
from Robot import Robot

from World import World

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

world = World()
robot = Robot(world)
print("\n" * 100)
world.printGrid(robot)
robot.moveSouth()
time.sleep(3)
print("\n" * 100)
world.printGrid(robot)
time.sleep(3)
print("\n" * 100)
robot.moveSouth()
world.printGrid(robot)
time.sleep(3)
print("\n" * 100)
robot.moveEast()
world.printGrid(robot)