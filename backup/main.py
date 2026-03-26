import pygame
import classes


pygame.init()

#SCREEN VARIABLES DECLARATION
size = (1024, 960)
screen = pygame.display.set_mode(size)
sm_surface = pygame.Surface((256, 240))


#PLAYER VARIABLES DECLARATION
player = classes.Player()
player.pos = (80, 32)


#----------------- TILE VARIABLE DECLARATION ---------------------
tile_list = []

grass = pygame.image.load("assets/grass.png")
dirt = pygame.image.load("assets/dirt.png")	

tiles_coord = [ #matrix 16x15	
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0],
[1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]  ]

for y, line in enumerate(tiles_coord):
	for x, tile in enumerate(line):
		if tile == 1:
			grass_rect = grass.get_rect(topleft=(x * 16, y * 16 ))
			tile_list.append(grass_rect)
			
		if tile == 2:
			dirt_rect = dirt.get_rect(topleft=(x * 16, y * 16 ))
			tile_list.append(dirt_rect)
			
			

#----------------- DRAW TILES -------------------------------
def draw_tiles():
	for y, line in enumerate(tiles_coord):
		for x, tile in enumerate(line):
			if tile == 1:
				sm_surface.blit(grass, (x * 16, y * 16 ))
			
			if tile == 2:
				sm_surface.blit(dirt, (x * 16, y * 16 ))
				


#----------------- INPUT DETECTION -------------------------------
up = 1758
down = 1974
left = 426
right = 645
	
UP = pygame.math.Vector2(0, -1) 
DOWN = pygame.math.Vector2(0, 1)
LEFT = pygame.math.Vector2(-1, 0)
RIGHT = pygame.math.Vector2(1, 0)
	
def input_detection(): #returns a Vector
	input_direct = pygame.math.Vector2(0, 0)
	
	mouse_pos = pygame.mouse.get_pos()
	keys = pygame.mouse.get_pressed()
	
	for key in keys:
		if key and mouse_pos[0] < left:  input_direct += LEFT
		if key and mouse_pos[0] > right: input_direct += RIGHT
		if key and mouse_pos[1] < up:    input_direct += UP
		#if key and mouse_pos[1] > down:  input_direct += DOWN
		
	if input_direct != (0, 0): input_direct = input_direct.normalize()
	
	return input_direct




last_input = pygame.math.Vector2(0,0)
run = True

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False
	
	
	#move
	input_direct = input_detection()
	if input_direct.x:
		last_input = input_direct	
	player.move(input_direct, last_input, tile_list)
	
		
	#render
	sm_surface.fill((31, 31, 31))
	for tile in tile_list:
		pygame.draw.rect(sm_surface, (0,255,0), tile)	
	draw_tiles()
	player.render(sm_surface)
	
	
    #scale screen
	scl_surface = pygame.transform.scale(sm_surface, (size))	
	screen.blit(scl_surface, (0, 0))



	pygame.display.update()
	

pygame.quit() 