import pygame
from general_functions import *
from random import randint
from random import uniform

"""
ALL CLASSES AND THEIR INHERITANCE
- Collectable
- LevelObj
- Particle
- Tree (LevelObj)
- SpriteAnimation
- Character(LevelObj)
- Player(Character)
- Enemy(Character)
- ParallaxLayer
- Camera
- Button
- VirtualJoy
"""

class Collectable():
	def __init__(self, x, y, name):
		self.x = x
		self.y = y
		self.altitude = y
		self.name = name
		self.collected = False
		self.gain = 0.02
		self.max = 0.5
		self.h_speed = self.max
		self.down = True
		
		self.sprite = pygame.image.load(
		f"assets/collectables/{name}.png"
		).convert_alpha()
		
		self.rect = self.sprite.get_rect()
		
	def update(self, direction):
		speed = (   (self.y - 60) / 180  )  * 2.4
		self.x += direction.x * speed
		self.rect.midbottom = (self.x, self.altitude)
		
	def check_collecting(self, player, dynamic_obj_list):
		if self.rect.colliderect(player.collis_rect):
			player.inventory[f"{self.name}"]["amount"] += 1
			dynamic_obj_list.remove(self)
			
		
	def animate(self):
		if self.down:
			self.h_speed += self.gain
			if self.h_speed > self.max:
				self.h_speed = self.max
			if self.altitude > self.y: self.down = False
			
		if self.down == False:
			self.h_speed -= self.gain
			if self.h_speed < -self.max:
				self.h_speed = -self.max
			if self.altitude < self.y: self.down = True
		
		self.altitude += self.h_speed
		self.rect.midbottom = (self.x, self.altitude)
		


class LevelObj():
	def __init__(self, info):
		self.sprite_path = info["path"]
		self.scalingfactor = ((info["y"] - 60) / 180) * 2.5
		if "no_scaling" in info: self.scalingfactor = 1
		
		self.x = info["x"]
		self.y = info["y"]
		self.w = info["w"]
		self.h = info["h"]

		self.speed = None
		self.speed_factor = 1.2
		if "speed_factor" in info:
			self.speed_factor = info["speed_factor"]
		
		self.sprite=pygame.image.load(self.sprite_path).convert_alpha()
		
		self.scaledsprite = pygame.transform.scale_by(self.sprite, self.scalingfactor)
		
		self.collis_rect = pygame.Rect(self.x, self.y,
		self.w * self.scalingfactor,
		self.h * self.scalingfactor)
		
		self.scaled_sprt_rect = None
		
		self.info = info
	
		
	def update(self, direction):
		speed = (   (self.y - 60) / 180  )  * self.speed_factor
		self.x += direction.x * speed * 2
		
		self.collis_rect.w = self.w * self.scalingfactor
		self.collis_rect.h = self.h * self.scalingfactor
		
		self.collis_rect.midbottom = (self.x, self.y)
		self.scaled_sprt_rect = self.scaledsprite.get_rect()
		
		self.scaled_sprt_rect.midbottom= self.collis_rect.midbottom
		if "sprite_offset_x" in self.info:
			self.scaled_sprt_rect.centerx =  self.collis_rect.centerx + self.info["sprite_offset_x"]


class Particle():
	def __init__(self, initx, inity, ground, type):
		self.initx = initx
		self.inity = inity
		self.x = initx
		self.y = inity
		self.speed = 0
		self.fall_speed = round(uniform(0.2, 0.5), 2)
		self.speed_gain = round(uniform(0.01, 0.02), 2)
		self.max_speed = randint(1, 2)
		self.falling = False
		self.forward = bool(randint(0, 1))
		self.ground = randint(ground - 8, ground + 8)
		self.alpha = 255
		
		self.sprite = self.sprite = pygame.image.load(
		f"assets/particles/{type}.png"
		).convert_alpha()
			
	def update(self, direction):
		speed = (   (self.ground - 60) / 180  )  * 2.4
		self.initx += direction.x * speed
		self.x += direction.x * speed
	
	def fall(self):
		self.y += self.fall_speed
		if self.forward:
			self.speed += self.speed_gain
			if self.speed > self.max_speed:
				self.speed = self.max_speed
			if self.x > self.initx: self.forward = False
				
		if self.forward == False:
			self.speed -= self.speed_gain
			if self.speed < -self.max_speed:
				self.speed = -self.max_speed
			if self.x < self.initx: self.forward = True
		
		self.x += self.speed
		
		if self.y >= self.ground:
			self.y = self.ground
			self.speed = 0
			self.alpha -= 2
			self.sprite.set_alpha(self.alpha)


class Tree(LevelObj):
	def __init__(self, info):
		self.angle = 0
		self.leaves = None
		self.leaves_pos = None
		self.rot_leaves = None
		self.rot_rect = None
		self.offset = pygame.math.Vector2(0, 0)
		self.type = info["type"]
		self.falling = False
		self.falling_speed = 0
		self.bouncing = False
		self.vanishing = False
		self.alpha = 255
		self.leaf_particle_fall = False
		self.particles = []
		self.drop_item = False
		self.hits_taken = 0
		self.shaking_forward = False
		self.hit_from_right = None
		self.player_faces_tree = None
		
		factor = ((info["y"] - 60) / 180) * 2.5 
		self.range_rect = pygame.Rect(0, 0, factor * 48, factor * 24)
		
		trunk_path = f"assets/forest/tree/{info['type']}_trunk.png"
		info["path"] = trunk_path
			
		self.leaves = pygame.image.load(f"assets/forest/tree/{info['type']}_leaves.png").convert_alpha()
	
		self.leaves = pygame.transform.scale_by(self.leaves, factor)
		
		super().__init__(info)		
			
	def updt_tree(self, dynamic_obj_list, player,
	button_action=None):
		def create_particles(amount):
			for i in range(amount):
				randx = round(uniform(x - w, x + w * 2), 1)
				randy = round(uniform(y - h, y - h/2), 1)
				ground = self.scaled_sprt_rect.bottom
				
				self.particles.append(
				Particle(randx, randy, ground, "leaf")
				)
				
		def update_particles():
			for i, particle in enumerate(self.particles):
				particle.fall()
				if particle.alpha < 4: del self.particles[i]
					
					
		x = self.scaled_sprt_rect.x
		y = self.scaled_sprt_rect.y
		w, h = self.scaled_sprt_rect.w, self.scaled_sprt_rect.h
		
		self.range_rect.center = self.scaled_sprt_rect.midbottom
		
		
		#defining if player looks at tree
		self.player_faces_tree = False
		if (player.x >= self.range_rect.center[0] and \
		player.facing_left) or \
		(player.x < self.range_rect.center[0] and \
		player.facing_left == False):
			self.player_faces_tree = True
			
		# start player animation
		if button_action == "interact" and \
		player.collis_rect.colliderect(self.range_rect) and \
		player.inventory["axe"]["equipped"] and \
		self.player_faces_tree:
			player.inventory["axe"]["using"] = True
			
		#increase hit amount and create leaf particle
		if player.collis_rect.colliderect(self.range_rect) and \
		player.inventory["axe"]["using"] and \
		player.animations["use_axe"].index >= 3 and \
		self.angle == 0:
			self.hits_taken += 1
			self.shaking_forward = True
			self.falling_speed = 0.5
			create_particles(8)
			if player.x >= self.range_rect.center[0]:
				self.hit_from_right = True
			else: self.hit_from_right = False
		
		#enable fall state	
		if self.hits_taken >= 5:
			self.falling = True
			self.shaking_forward = False
			self.hits_taken = 0
		
		
		# update forward shake
		if self.shaking_forward:
			self.angle += self.falling_speed
			self.falling_speed -= 0.08
			if self.angle <= 0:
				self.angle = 0
				self.falling_speed = 0
				self.shaking_forward = False
			self.leaf_particle_fall = True
		
		#update fall 
		if self.falling:
			self.falling_speed += 0.01
			self.angle += self.falling_speed
			if self.angle > 17: self.falling_speed += 0.05
			if self.angle > 68:
				self.falling_speed = 0
				self.falling = False
				self.bouncing = True
				self.drop_item = True
			
		
		if self.drop_item:
			item = Collectable(x + w / 2, y + h + 1, "wood")
			dynamic_obj_list.append(item)
			self.drop_item = False
				
		#create particles
		if self.leaf_particle_fall == False and self.falling:
				create_particles(15)
				self.leaf_particle_fall = True	
		
		#update particles
		if self.leaf_particle_fall:
			update_particles()
				
		#bouncing back after fall
		if self.bouncing:
			self.falling_speed += 0.05
			self.angle -= self.falling_speed
			if self.angle < 67:
				self.bouncing = False
				self.vanishing = True
		
		final_angle = self.angle
		if self.hit_from_right:
			final_angle = -self.angle
		
		#rotate cut part of the tree
		if self.type == "tree1":
			pivot = [x + w/2, y + h/1.8]
			self.offset.x, self.offset.y =   0,   -(h * 0.8)
			
			self.rot_leaves, self.rot_rect = rotate(
			self.leaves,
			final_angle,
			pivot, self.offset
			)
			
			
			
class SpriteAnimation():
	def __init__(self, spritesheet, grid_size, amount, row=0, 
	rate=0.2, loop=True):
		self.frames = []
		self.current_frame = None
		self.index = 0
		self.framerate = rate
		self.loop = loop
		self.amount = amount
		
		for i in range(amount):
			cell = pygame.Surface\
			((grid_size, grid_size), pygame.SRCALPHA)
			
			cell.blit(spritesheet, (-(i * grid_size), -(row * grid_size)))
			self.frames.append(cell)
			
	def play(self):
		if self.index <= self.amount - 1:
			self.current_frame = self.frames[round(self.index)]
			self.index += self.framerate
			
			if self.index > self.amount - 1:
				if self.loop: self.index = 0
				if self.loop == False: self.current_frame = self.frames[-1]
		
	def reset(self):
		self.current_frame = self.frames[0]
		self.index = 0
		

class Character(LevelObj):
	def __init__(self, x, y, w, h, cell_size, default_sheet_path):
		info = {"x" :  x,"y" : y, "w" : w, "h" : h,
		"path" : "assets/place_holder.png"}
		
		super().__init__(info)
		
		self.default_sheet = pygame.image.load(
		default_sheet_path
		).convert_alpha()
		
		self.animations = {
		"walk_down" : SpriteAnimation(
		self.default_sheet, cell_size, 8),
		
		"walk_up" : SpriteAnimation(
		self.default_sheet, cell_size, 8, 1),
		
		"idle_down" : SpriteAnimation(
		self.default_sheet, cell_size, 2, 2, 0.01)
		}
	
		self.sprite = None
		self.facing_left = True
		self.velocity = pygame.math.Vector2(0, 0)
		
	def move(self, direction, rects):
		speed = ( (self.y - 60) / 180  ) * self.speed_factor
		
		collision(self, rects)
		
		self.velocity.x, self.velocity.y = direction.x, direction.y
		self.x += self.velocity.x * speed * 2
		self.y += self.velocity.y * speed
		
		if self.collis_rect.collidelistall(rects): self.velocity *= 0
						
			
         #_________ANIMATION STUFF________________
			
		#defining facing direction
		if direction.x < 0: self.facing_left = True
		if direction.x > 0: self.facing_left = False
			
		# down diagonal sprite walk animation
		if direction.x != 0 or direction.y > 0:
			self.animations["walk_down"].play()
			self.sprite = self.animations["walk_down"].current_frame
		
		#up diagonal sprite walk animation	
		if direction.y < 0:
			self.animations["walk_up"].play()
			self.sprite = self.animations["walk_up"].current_frame
		
		# idle	
		if direction == (0, 0):
			self.animations["idle_down"].play()
			self.sprite = self.animations["idle_down"].current_frame
				
	def scaling_flipping(self):
			self.scalingfactor = ((self.y - 60) / 180) * 2.5	
			
			self.scaledsprite = pygame.transform.scale_by(
			self.sprite, self.scalingfactor)
			
			if self.facing_left == False:
				self.scaledsprite = pygame.transform.flip(
				self.scaledsprite, True, False)
			
			


class Player(Character):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h, 32, "assets/animation/player.png")
		
		self.axe_spritesheet = pygame.image.load(
		"assets/animation/player_axe.png").convert_alpha()
		
		self.inventory = {
		"wood" : {"amount" : 0, "equipped" : False},
		"axe" : {"amount": 1, "equipped" : True, "using" : False}
		}
		
	def update_animation(self):
		# AXE ANIMATION
		if "use_axe" not in self.animations:
			self.animations["use_axe"] = SpriteAnimation\
			(self.axe_spritesheet, 48, 7, loop=False)
	
		if self.inventory["axe"]["equipped"] and \
		self.inventory["axe"]["using"]:
			
			self.animations["use_axe"].play()
			self.sprite = self.animations["use_axe"].current_frame
		
		if self.animations["use_axe"].current_frame == \
		self.animations["use_axe"].frames[-1]:
			self.inventory["axe"]["using"] = False
			self.animations["use_axe"].reset()



class Enemy(Character):
	def __init__(self, x, y, w, h):
		pass
			
			
			
		

class ParallaxLayer():
	def __init__(self, info):
		file = pygame.image.load(
		f"assets/{info['area']}/parallax/{info['number']}.png")	

		self.sprite = file.convert_alpha()
		self.h = self.sprite.get_height()
		self.x = info["x"]
		self.y = info["y"]
		self.speed_factor = info["speed_factor"]
		self.loop = True
		self.exit_sprite = None
		self.is_foreground_tree = False
		if "is_foreground_tree" in info: self.is_foreground_tree = True
		
		'''
		Composition refers to the relation between a normal
		background layer and and background layer with an
		an exit. 1 means exit, and 0 means no exit.
		The composition is read and drawn by render_all()
		'''
		
		if "composition" in info:
			self.loop = False
			self.exit_sprite = pygame.image.load(
			f"assets/{info['area']}/parallax/{info['number']}-exit.png")
		
		self.info = info
		
		
	def update(self, direction):
		speed = (self.y - 60) / 180
		speed = round(speed, 1)
		
		self.x += direction.x * speed * self.speed_factor
		
		if self.loop and (self.x > 432 or self.x + 432 < 0): self.x = 0


class Camera():
	def __init__(self):
		self.speed = 0
		self.rect = pygame.Rect(216, 0, 1, 240)
		self.reseting = False
		self.max_speed = 1.1 #1.1
		self.accel = 0.04 # 0.04

	def move(self, obj_list, dynamic_obj_list, player,
	button_action = None):
		if player.velocity.x < 0:
			self.rect.x = 324
			self.speed += self.accel
			self.reseting = False
			
		if player.velocity.x > 0:
			self.rect.x = 108
			self.speed += self.accel
			self.reseting = False
			
		if self.speed >= self.max_speed and self.reseting == False:
			 self.speed = self.max_speed
			
		if self.rect.colliderect(player.collis_rect) and \
		player.velocity.x != 0:
			self.speed = 1
				
		if player.velocity.x == 0:
			self.reseting = True
			self.rect.x = 216
			
			if player.collis_rect.centerx < self.rect.x:
				self.speed = (player.collis_rect.centerx - self.rect.x) / -90
				velocity = pygame.math.Vector2(1, 0) * self.speed
				
				for i in obj_list:
					i.update(velocity)
					if isinstance(i, Tree):
						for particle in i.particles: particle.update(velocity)
					
			if player.collis_rect.centerx > self.rect.x:
				self.speed = (player.collis_rect.centerx - self.rect.x) / 90
				velocity = pygame.math.Vector2(-1, 0) * self.speed

				for i in obj_list:
					i.update(velocity)
					if isinstance(i, Tree):
						for particle in i.particles: particle.update(velocity)
					
			if self.rect.colliderect(player.collis_rect):
				self.speed = 0
				
		for i in obj_list:
			i.update(-player.velocity  * self.speed)
			
			if isinstance(i, Tree):
				i.updt_tree(dynamic_obj_list, player, button_action)
				for particle in i.particles:
					particle.update(-player.velocity  * self.speed)
			
			if isinstance(i, Collectable):
				i.check_collecting(player, dynamic_obj_list)
				i.animate()
		

class Button():
	def __init__(self, text, x, y, w, h):
		self.text = text
		self.button_rect = pygame.Rect(x, y, w, h)
		self.cursor = pygame.Rect(-32, -32, 8, 8)
		
	def pressed(self, cursorx, cursory):
		self.cursor.center = (cursorx, cursory)
		if self.button_rect.colliderect(self.cursor): return True
		else: return False
		


class VirtualJoy():
	def __init__(self):
		self.origin = (80, 160)
		self.radius = 64
		self.stick_pos = [self.origin[0], self.origin[1]]
		self.finger_relative_dist = [0, 0]
		self.absl_dist = pygame.math.Vector2(0, 0)
		self.relative_dist = pygame.math.Vector2(0, 0)
		self.rect = pygame.Rect(0, 0, 32, 32)
		self.rect.center = [self.origin[0], self.origin[1]]
		self.on_circle = False
		
		
	def update(self, fingerx, fingery):
		self.stick_pos = [self.origin[0], self.origin[1]]

		self.absl_dist.x = fingerx - self.origin[0]
		self.absl_dist.y = fingery - self.origin[1]
		
		self.relative_dist = self.absl_dist / self.radius
		
		if self.relative_dist != True:
			self.relative_dist = self.relative_dist.normalize()
		
		if (fingerx - self.origin[0]) ** 2 \
		+ (fingery - self.origin[1]) ** 2 < self.radius ** 2:
			self.on_circle = True
			self.stick_pos[0] = fingerx
			self.stick_pos[1] = fingery	

		else:
			self.on_circle = False
			self.stick_pos[0] = self.origin[0]\
			+ self.relative_dist.x * self.radius
			
			self.stick_pos[1] = self.origin[1]\
			 + self.relative_dist.y * self.radius
			 
#		if abs(self.relative_dist.x) > 0.95 or \
#		abs(self.relative_dist.y) > 0.95:
#			self.relative_dist *= 1.01
		
			
				
			
		self.rect.center = self.stick_pos
			