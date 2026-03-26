import pygame
from random import choice
import time
from general_functions import *

pygame.init()

clock = pygame.time.Clock()
log = pygame.font.Font()

#SCREEN VARIABLES DECLARATION
size = (1080, 600)
sm_size = (432, 240)
screen = pygame.display.set_mode(size)
sm_surface = pygame.Surface(sm_size)

class LevelArea():
	def __init__(self, name):
		self.sprite = pygame.image.load(f"cells/{name}.png")
		self.name = name
	

areas = [
LevelArea("UDLR"),	
LevelArea("ULR"),
LevelArea("UDR"),
LevelArea("DLR"),
LevelArea("UDL"),
LevelArea("UL"),
LevelArea("UR"),
LevelArea("DR"),
LevelArea("DL"),
LevelArea("UD"),
LevelArea("LR"),
LevelArea("U"),
LevelArea("R"),
LevelArea("D"),
LevelArea("L")
]

areas.extend([LevelArea("UDLR")]*10)


world = { (20, 15) : LevelArea("UDLR") }

def generate_tile():
	def check_neighb(oposite_dir, new_tile):
		x, y = new_tile[0], new_tile[1]
		up, down  = (x, y-1), (x, y+1)
		left, right = (x-1, y), (x+1, y)
			
		directions = []
		available = 0
		
		if up in world:
			if "D" in world[up].name: directions.append("U")	
		else:
			available += 1
		
		if down in world:
			if "U" in world[down].name: directions.append("D")	
		else:
			available += 1
		
		if left in world:
			if "R" in world[left].name: directions.append("L")	
		else:
			available += 1
		
		if right in world:
			if "L" in world[right].name: directions.append("R")	
		else:
			available += 1
			
		if available >= 3:
			avail_obj = [ a for a in areas if oposite_dir in a.name ]
			world[new_tile] = choice(avail_obj)

		else:
			avail_obj = [ a for a in areas if list(a.name) == directions ]
			world[new_tile] = choice(avail_obj)
				
	for curr_tile in list(world):
		x, y = curr_tile[0], curr_tile[1]
		up, down, left, right = (x, y-1), (x, y+1), (x-1, y), (x+1, y)
		
		c = choice(world[curr_tile].name)		
		
		if c == "U" and up not in world: check_neighb("D", up)
		if c == "D" and down not in world: check_neighb("U", down)
		if c == "L" and left not in world: check_neighb("R", left)
		if c == "R" and right not in world: check_neighb("L", right)
			

def all_tiles_closed(): #returns True if all tiles are closed
	checked_tiles_bool = []
	for curr_tile in list(world):
		x, y = curr_tile[0], curr_tile[1]
		up, down, left, right = (x, y-1), (x, y+1), (x-1, y), (x+1, y)
		
		checked_dir = []
		for exit in world[curr_tile].name:
			if exit == "U": checked_dir.append((up in world))
			if exit == "D": checked_dir.append((down in world))
			if exit == "L": checked_dir.append((left in world))
			if exit == "R": checked_dir.append((right in world))
		
		checked_tiles_bool.append(all(checked_dir))
	
	return all(checked_tiles_bool)


while not all_tiles_closed():
	generate_tile()
		
map = pygame.Surface((sm_size[0] * 8, sm_size[1] * 8))
map.fill((100, 200, 50))
for k in world: map.blit(world[k].sprite, (k[0]*16, k[1]*16))
x, y = 0, 0 

#while True:
#	while iterations < len(world) * 2:
#		iterations = generate_tile(iterations)

#	if len(world) < 30:
#		iterations = 0
#		world = { (10, 6) : LevelArea("UDLR") }
#	else: break
	

run = True

while run:
	game_time = clock.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False
		if event.type == pygame.FINGERDOWN: pass
	
	
	x += -input_detection()[0] * 5
	y += -input_detection()[1] * 5
			
			#world = { (10, 6) : choice(areas) }
		#	world = { (10, 6) : LevelArea("UDLR") }
	
	
	sm_surface.fill((165, 221, 219))
	
#	closed_tiles = generate_tile()
			
	sm_surface.blit(map, (x, y))

	text = log.render(f"{len(list(world))}", True, (255, 255, 100))
	
	sm_surface.blit(text, (3, 3))	
	
	
	
	
    #scale screen
	scl_surface = pygame.transform.scale(sm_surface, (size))	
	screen.blit(scl_surface, (0, 0))
#	time.sleep(0.5)
	pygame.display.update()

	
	

pygame.quit()