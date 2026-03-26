import pygame
import time

class Player():
	def __init__(self):
		self.sprite = pygame.image.load("assets/player.png")
		self.sprite.convert_alpha()
		
		self.falling = True
		self.jumping = False
		self.inertia = 0
		
		self.gravity = 0.03 #0.02
		self.friction = 1.05 #0.01
		
		self.jump_height = -16
		self.height_vel = -1
		self.fall_vel = 0.01
		self.speed = 0

		self.velocity = pygame.math.Vector2(0, 0)
		
	
		self.offset = (-5,-2)
		
		self.pos = pygame.math.Vector2(0, 0)
		
		self.w = 6
		self.h = 14
		self.rect_size = (self.w, self.h)
		self.rect = pygame.Rect(self.pos, self.rect_size)
	
		
			
				
	
	#MOVE										
	def move(self, direction, last_dir, tile_list):
		self.pos += pygame.math.Vector2(0,0)
		self.rect.topleft = self.pos
			
		def collis_type(tile):
			if self.rect.bottom == tile.top + 1:
				return "bottom"
			if self.rect.top == tile.bottom - 1:
				return "top"
			if self.rect.left == tile.right - 1:
				return "left"
			if self.rect.right == tile.left + 1:
				return "right"

				
		def on_ground():
			bottom_rect = pygame.Rect(0, 0, 1, 1)
			bottom_rect.w = self.w
			bottom_rect.h = 1
			bottom_rect.topleft = self.rect.bottomleft
			
			if bottom_rect.collidelistall(tile_list):
				return True
			else: return False
			
		
		
		#MOVE
		
		#move on x 
		if direction.x != 0:
			self.inertia = False
			self.speed = 0.5
			self.pos.x += direction.x * self.speed
				
		#inertia
		else:
			self.inertia = True
			self.speed /= self.friction
			if self.speed <= 0.001:
				self.speed = 0
				
			self.pos.x += last_dir.x * self.speed
			
			
		#enable jump	
		if direction.y < 0 and not self.falling:
			self.jumping = True
				
		#jump	
		if self.jumping:
			self.pos.y += self.height_vel
			self.height_vel += self.gravity
					
			if self.height_vel >= 1:
				self.height_vel = 1
					
			if on_ground():
				self.height_vel = -1
				#self.pos.y += -1
				self.jumping = False
				
				
		#enable fall
		if not on_ground() and not self.jumping:
			self.falling = True
	
		#fall	
		if self.falling:
			self.pos.y += self.fall_vel
			self.fall_vel += self.gravity
				
			if self.fall_vel >= 1:
				self.fall_vel = 1
				
			if on_ground():
				self.fall_vel = 0.01
				#self.pos.y += -1
				self.falling = False
		
		self.rect.topleft = self.pos
	
		
		#COLLISION
		for index in self.rect.collidelistall(tile_list):
			tile = tile_list[index]
			
			#if tile.colliderect(self.rect):
			if self.inertia: direction.x = last_dir.x
			if self.jumping: direction.y = self.height_vel
			if self.falling: direction.y = self.fall_vel
				
			if direction.y > 0 and collis_type(tile) == "bottom":
				self.pos.y = tile.top - self.h
						
			if direction.y < 0 and collis_type(tile) == "top":
				self.pos.y = tile.bottom
					
			if direction.x > 0 and collis_type(tile) == "right":
				self.pos.x = tile.left - self.w
						
			if direction.x < 0 and collis_type(tile) == "left":
				self.pos.x = tile.right
	
			self.rect.topleft = self.pos
				
			
			
	def render(self, surface):
		posx = self.rect.x + self.offset[0]
		posy = self.rect.y + self.offset[1]	
		surface.blit(self.sprite, (posx, posy))
		#pygame.draw.rect(surface, (255,0,0), self.rect)
		
	
	
	
	