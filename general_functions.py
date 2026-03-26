import pygame
import json
import classes

#-------------------------------------
def subclasses_recursive(cls):
    direct = cls.__subclasses__()
    indirect = []
    for subclass in direct:
        indirect.extend(subclasses_recursive(subclass))
    return tuple(direct + indirect)

#-------------------------------------
def y_sort(background_list, dynamic_obj_list):
	result_list = [ obj for obj in background_list ]
	
	unsorted = [   [obj, obj.y] for obj in dynamic_obj_list  ]
	sorted_list = sorted(unsorted, key=lambda item : item[1])
	
	#item[0] is the obj, item[1] is its y pos
	for item in sorted_list: result_list.append(item[0])
	
	fg_obj = []
	for obj in result_list:
		if not isinstance(obj, classes.Collectable):
			if "z_index" in obj.info:
				fg_obj.append([   obj, obj.info["z_index"]   ])
	
	fg_obj = sorted(fg_obj, key=lambda item : item[1])
	
	for item in fg_obj:
		result_list.remove(item[0])
		result_list.append(item[0])
	
	return result_list

#-------------------------------------	
def save_area(background_list, dynamic_obj_list, path):
	all_obj = background_list + dynamic_obj_list
	objects_info = {}
	
	for index, obj in enumerate(all_obj):
		objects_info[f"{type(obj)}{index}"] = obj.info
	
	with open(path, "w") as file:
		json.dump(objects_info, file)	

	
#-------------------------------------
def load_area(path):
				
	with open(path) as file:
		objects_info = json.load(file) #returns a list (or dict)
		
		background = []
		dynamic_obj = []

		for info in objects_info:
			if "ParallaxLayer" in info:
				obj = classes.ParallaxLayer(objects_info[info])	
				background.append(obj)							
			if "LevelObj" in info:
				obj = classes.LevelObj(objects_info[info])
				dynamic_obj.append(obj)	
			if "Tree" in info:
				obj = classes.Tree(objects_info[info])
				dynamic_obj.append(obj)

		return background, dynamic_obj			
	
		
#-------------------------------------				
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
	x, y = mouse_pos[0], mouse_pos[1]
	
	clicking = False
	if True in pygame.mouse.get_pressed(): clicking = True
		
	if clicking and x < left:  input_direct += LEFT
	if clicking and x > right: input_direct += RIGHT
	if clicking and y < up:    input_direct += UP
	if clicking and  y > down:  input_direct += DOWN
	if clicking and  y < 665: input_direct.x, input_direct.y = 0, 0
		
	if input_direct != (0, 0): input_direct = input_direct.normalize()
	
	return input_direct
	
				

#-------------------------------------
def create_background(background):
	if background == "forest1":
		return [
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 82,
		"speed_factor" : 4,
		"path" : "assets/forest/parallax/0.png"
		}),
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 139,
		"speed_factor" : 1.6,
		"path" : "assets/forest/parallax/1.png"
		}),
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 119,
		"speed_factor" : 2,
		"path" : "assets/forest/parallax/2.png"
		}),	
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 131,
		"speed_factor" : 2,
		"path" : "assets/forest/parallax/grass_chunk.png"
		}),
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 155,
		"speed_factor" : 2,
		"path" : "assets/forest/parallax/3.png"
		}),	
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 173,
		"speed_factor" : 2,
		"path" : "assets/forest/parallax/4.png"
		}),	
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 191,
		"speed_factor" : 2,
		"path" : "assets/forest/parallax/5.png"
		}),	
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 210,
		"speed_factor" : 2,
		"path" : "assets/forest/parallax/6.png"
		}),	
		
		classes.ParallaxLayer({
		"x" : 0,
		"y" : 240,
		"speed_factor" : 2,
		"path" : "assets/forest/parallax/7.png"
		})
		
		]
		
#-------------------------------------	
def collision(player, rects):
	def collis_type(wall):
		if wall.top <= player.collis_rect.bottom < wall.center[1]:#+1
			return "bottom"
		if wall.bottom >= player.collis_rect.top > wall.center[1]:#-1
			return "top"
		if wall.right >= player.collis_rect.left > wall.center[0]:#-1
			return "left"
		if wall.left <= player.collis_rect.right < wall.center[0]:#+1
			return "right"
				
	index = player.collis_rect.collidelist(rects)
	rect = rects[index]
	
	if  collis_type(rect) == "bottom":
		player.y = rect.top
							
	if collis_type(rect) == "top":
		player.y = rect.bottom + player.collis_rect.h
						
	if  collis_type(rect) == "right":
		player.x = rect.left - player.collis_rect.w / 2
							
	if collis_type(rect) == "left":
		player.x = rect.right + player.collis_rect.w / 2
		

#-------------------------------------
def render_all(obj_list, surface, txt_obj, button, player, txt):
	surface.fill((165, 221, 219))
	
	for obj in obj_list:		
		if isinstance(obj, classes.Collectable):
			#pygame.draw.rect(surface, (0, 255, 0), obj.rect)
			surface.blit(obj.sprite, (obj.rect.topleft))
			
		
		if isinstance(obj, classes.ParallaxLayer):
			if obj.loop:
				surface.blit(obj.sprite, (obj.x-432, obj.y - obj.h))
				surface.blit(obj.sprite, (obj.x, obj.y - obj.h))
				surface.blit(obj.sprite, (obj.x+432, obj.y - obj.h))
				
			else:
				for ind, char in enumerate(obj.info['composition']):
					sprite = None
					if char == "0": sprite = obj.sprite
					if char == "1": sprite = obj.exit_sprite
					surface.blit(sprite, (obj.x + (432*ind), obj.y - obj.h))	
			
			
		if isinstance(obj, classes.LevelObj):
			surface.blit(obj.scaledsprite, obj.scaled_sprt_rect.topleft)
				
			#pygame.draw.rect(surface, (255, 0, 0), obj.collis_rect)
			
			if "z_index" in obj.info:
				if obj.collis_rect.x < player.x < obj.collis_rect.x + obj.w:
					obj.scaledsprite.set_alpha(63)
				else: obj.scaledsprite.set_alpha(255)
				
			
			if isinstance(obj, classes.Tree):
#				pygame.draw.rect\
#				(surface, (0, 255, 0), obj.range_rect, width = 1)
				
				for particle in obj.particles:
					if particle.alpha > 4:
						surface.blit(particle.sprite, (particle.x, particle.y))
						
				if obj.vanishing:
					obj.alpha -= 2
					obj.leaves.set_alpha(obj.alpha)
					if obj.alpha <= 2: obj.vanishing = False
				
				if obj.alpha > 4:
					surface.blit(obj.rot_leaves, obj.rot_rect)
					
				
				
		
	#pygame.draw.circle(sm_surface, (0, 127, 255), joy.origin, joy.radius)
	#pygame.draw.rect(sm_surface, (255, 255, 255), joy.rect)
	
	#pygame.draw.rect(surface, (0,0,255), button.button_rect)	
	
	text = txt_obj.render(txt, True, (255, 0, 255))

	surface.blit(text, (3, 3))
	
				
#-------------------------------------
def rotate(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotate(surface, -angle)  
    rotated_offset = offset.rotate(angle)  
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect