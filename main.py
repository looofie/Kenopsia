import pygame
import classes
from general_functions import *
from time import sleep 
from sys import getsizeof

pygame.init()
clock = pygame.time.Clock()
txt_obj = pygame.font.Font(size=20)

#SCREEN VARIABLES DECLARATION
screen_size = (1080, 600)
screen = pygame.display.set_mode(screen_size)

sm_surf_size = (432, 240)
sm_surface = pygame.Surface(sm_surf_size)

button = classes.Button("interact", 360, 8, 64, 32)
camera = classes.Camera()
vpoint = pygame.Rect(216, 60, 2, 2)
player = classes.Player(216, 200, 8, 8)	
#joy = classes.VirtualJoy()

lists = load_area("data/test.json")
background_list = lists[0]
dynamic_obj_list = lists[1]
dynamic_obj_list.extend([player])


rects = [obj.collis_rect for obj in dynamic_obj_list if isinstance(obj,(classes.Character)) == False and isinstance(obj,(classes.ParallaxLayer)) == False]
rects.append(pygame.Rect(-256, -64, 2, 2))

#background_list = create_background("forest1")
#dynamic_obj_list = [player]

#rects = [obj.collis_rect for obj in dynamic_obj_list if isinstance(obj,(classes.Character)) == False]
#rects.append(pygame.Rect(-256, -64, 2, 2))

#save_area(background_list, dynamic_obj_list, "data/test.json")


#---------------- MAIN LOOP ---------‐----
run = True

while run:
	button_action = None
#	sleep(0.1)
	time = clock.tick(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		
		if event.type == pygame.FINGERDOWN:
			fingerx = event.x * sm_surf_size[0]
			fingery = event.y * sm_surf_size[1] * 3.45
			if fingery <= sm_surf_size[1] and \
			button.pressed(fingerx, fingery) == False:
				
#				lists = load_area("data/test_original.json")
#				background_list = lists[0]
#				dynamic_obj_list = lists[1]
#				dynamic_obj_list.append(player)
				
				tree_info = {
				"x" : fingerx,
				"y" : fingery,
				"w" : 20,
				"h" : 10,
				"type" : "tree1" }
				
				tree = classes.Tree(tree_info)
				
				dynamic_obj_list.append(tree)
				rects.insert(0, tree.collis_rect)
			
			if button.pressed(fingerx, fingery):
				button_action = "interact"
				#tree.updt_tree(10)
				
#				joy.origin = [fingerx, fingery]

#		if event.type == pygame.FINGERUP:
#			joy.stick_pos = [joy.origin[0], joy.origin[1]]
#			joy.relative_dist.x, joy.relative_dist.y = 0, 0
#			joy.rect.center = joy.stick_pos
#			
#		if event.type == pygame.FINGERMOTION:
#			fingerx = event.x * sm_surf_size[0]
#			fingery = event.y * sm_surf_size[1] * 3.45
#			joy.update(fingerx, fingery)

						

			
			
	# if player gets to exit:
			#change_area()
	
	obj_list = y_sort(background_list, dynamic_obj_list)

	player.move(input_detection(), rects)
	player.update_animation()
	player.scaling_flipping()
		
	camera.move(
	obj_list,
	dynamic_obj_list,
	player,
	button_action
	)
	
		
	render_all(
	obj_list,
	sm_surface,
	txt_obj,
	button,
	player,
	f"{clock}"
	)
		
	
	
    #scale screen
	scl_surface = pygame.transform.scale(
	sm_surface,
	(screen_size)
	)	
	
	screen.blit(scl_surface, (0, 0))



	pygame.display.update()

		
#save_area(background_list, dynamic_obj_list, "data/test.json")
pygame.quit()