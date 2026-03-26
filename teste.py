import pygame
from general_functions import *

pygame.init()

clock = pygame.time.Clock()
log = pygame.font.Font()

#SCREEN VARIABLES DECLARATION
size = (1080, 600)
sm_size = (432, 240)
screen = pygame.display.set_mode(size)
sm_surface = pygame.Surface(sm_size)

points = (
(64, 64), 
(30, 80), 
(250, 200), 
(300, 100),
(120, 64)

)

curr_start_point_index = 0
curr_end_point_index = 1

rect = pygame.Rect(0, 0, 16, 16)
pos = list(points[0])
rect.center = pos


def follow_straight_line(start_point, end_point,
obj_coord, speed=0.01):
	#dist between start and end point
	distx = end_point[0] - start_point[0]
	disty = end_point[1] - start_point[1]
	line_size = (distx ** 2 + disty ** 2) ** 0.5
	
	#dist between obj pos a and end point
	obj_distx = end_point[0] - obj_coord[0]
	obj_disty = end_point[1] - obj_coord[1]
	obj_dist = (obj_distx ** 2 + obj_disty ** 2) ** 0.5
		
	new_coord = list(obj_coord)
	change_line = False
	
		
	if obj_dist > speed * (2/3):
		new_coord[0] += distx * speed / line_size
		new_coord[1] += disty * speed / line_size
	
	else:
		change_line = True
			
	return new_coord, change_line



run = True

while run:
	time = clock.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False
		
	curr_start_point = points[curr_start_point_index]
	curr_end_point = points[curr_end_point_index]
	
	change_line = False
	
	pos, change_line = follow_straight_line(
	curr_start_point,
	curr_end_point,
	pos,
	speed = 15
	)
	
	teste = "teste"
	
	if change_line:
		if curr_end_point_index < len(points) - 1:
			curr_start_point_index += 1
			curr_end_point_index += 1
			
		else: teste = "hey"
			
	
	
	rect.center = pos
	
	sm_surface.fill((165, 221, 219))
	
	pygame.draw.lines(sm_surface, (255, 0, 0), False, 
	points)
	
	pygame.draw.rect(sm_surface, (0, 0, 255), rect)
	
	
	
	text = log.render(f"{teste}", True, (255, 0, 0))
	
	sm_surface.blit(text, (3, 3))
	
	
	
	
	
	
	
	
    #scale screen
	scl_surface = pygame.transform.scale(sm_surface, (size))	
	screen.blit(scl_surface, (0, 0))



	pygame.display.update()
	

pygame.quit()