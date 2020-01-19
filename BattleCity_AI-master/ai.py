import random
import time
import multiprocessing
import sys
import queue as Queue

class ai_agent():
	mapinfo = []
	encoded_map = []
	dangerous_map = []
	#map_width = 0
	#map_height = 0

	def __init__(self):
		self.mapinfo = []
		self.encoded_map = []
		self.map_width = 13
		self.map_height = 13
		self.encoded_player_top = -1
		self.encoded_player_left = -1

		#               up right down left
		self.dir_top =  [-1, 0,  1,   0]
		self.dir_left = [0,  1,  0,  -1]

		#	dangerous location (bullets may pass in near time)
		self.dangerous_map = []

		# adjusting
		self.adjusting = False

	# rect:					[left, top, width, height]
	# rect_type:			0:empty 1:brick 2:steel 3:water 4:grass 5:froze
	# castle_rect:			[12*16, 24*16, 32, 32]
	# mapinfo[0]: 			bullets [rect, direction, speed]]
	# mapinfo[1]: 			enemies [rect, direction, speed, type]]
	# enemy_type:			0:TYPE_BASIC 1:TYPE_FAST 2:TYPE_POWER 3:TYPE_ARMOR
	# mapinfo[2]: 			tile 	[rect, type] (empty don't be stored to mapinfo[2])
	# mapinfo[3]: 			player 	[rect, direction, speed, Is_shielded]]
	# shoot:				0:none 1:shoot
	# move_dir:				0:Up 1:Right 2:Down 3:Left 4:None
	# keep_action:			0:The tank work only when you Update_Strategy. 	1:the tank keep do previous action until new Update_Strategy.

	# def Get_mapInfo:		fetch the map infomation
	# def Update_Strategy	Update your strategy


			
			
	def operations (self,p_mapinfo,c_control):	

		while True:
		#-----your ai operation,This code is a random strategy,please design your ai !!-----------------------			
			self.Get_mapInfo(p_mapinfo)

			bullets = self.mapinfo[0]
			enemies = self.mapinfo[1]
			tiles = self.mapinfo[2]
			player = self.mapinfo[3][0]
			player_left = player[0][0]
			player_top = player[0][1]

			q=0
			for i in range(100):
				q+=1

			# print bullets

			self.encode_map(bullets, enemies, tiles, player)
			

			# print player

			# self.print_encoded_map()
			# raw_input()
	

			# print self.mapinfo[0]
			# time.sleep(0.001)	
			
			#q=0
			#for i in range(10000000):
			#	q+=1


			shoot = random.randint(0,1)
			move_dir = random.randint(0,4)
			keep_action = 1

			
			# get encoded player position
			self.encoded_player_left = player_left / 32
			self.encoded_player_top = player_top / 32

			# get player's direction
			player_dir = player[1]

			adjust_top = self.encoded_player_top * 32
			adjust_left = self.encoded_player_left * 32

			# print "player_top: %d,  player_left: %d" %(player_top, player_left)
			move = self.dodge_bullets(bullets, player_top, player_left)
			if (move != -1):
				print("Dodge Bullet")
				self.Update_Strategy(c_control, 0, move, 1)
				continue

			# 1. check if the position of player's tank is on the multiplier of 32
			if (player_dir == 1 or player_dir == 3):
				if (player_top - adjust_top > 5):
					# print "adjust left"
					self.Update_Strategy(c_control, 0, 0, keep_action)
					continue

			elif (player_dir == 0 or player_dir == 2):
				if (player_left - adjust_left > 5):
					# print "adjust left"
					self.Update_Strategy(c_control, 0, 3, keep_action)
					continue

			# 2. check nearest 5 blocks in every direction ( bullet, tank )
			# check for bullets
			move = self.check_bullets(bullets)
			if (move != -1):
				# print "Found Bullet"
				self.Update_Strategy(c_control, 1, move, 1)
				continue


			# check for tanks
			move = self.check_tanks()
			if (move != -1):
				# print "Found Tank"
				self.Update_Strategy(c_control, 1, move, 1)
				continue


			# 3. BFS
			self.generate_dangerous_map(bullets, enemies)
			move = self.bfs()
			if (move == -1):
				move = random.randint(0,4)
				self.Update_Strategy(c_control, 0, move, keep_action)
			else:
				self.Update_Strategy(c_control, 0, move, keep_action)
			#keep_action = 0
			

			#-----------
			# self.Update_Strategy(c_control,shoot,move_dir,keep_action)
		#------------------------------------------------------------------------------------------------------
	
	def dodge_bullets(self, bullets, player_top, player_left):
		range = 100
		for bullet in bullets:
			bullet_top = bullet[0][1]
			bullet_left = bullet[0][0]
			bullet_bottom = bullet[0][1] + bullet[0][3]
			bullet_right = bullet[0][0] + bullet[0][2]
			bullet_h_mid = (bullet_top + bullet_bottom) / 2
			bullet_v_mid = (bullet_left + bullet_right) / 2
			bullet_dir = bullet[1]
			# top part of player tank
			if ((bullet_bottom > player_top and bullet_bottom <= player_top + 10) or (bullet_h_mid > player_top and bullet_h_mid <= player_top + 10)):
				if ((player_left < bullet_left and player_left + range > bullet_left and bullet_dir == 3) or (player_left > bullet_left and player_left - range < bullet_left and  bullet_dir == 1)):
					return 2
			# bottom part of player tank
			if ((bullet_top > player_top + 16 and bullet_top <= player_top + 26) or (bullet_h_mid > player_top + 16 and bullet_h_mid <= player_top + 26)):
				if ((player_left < bullet_left and player_left + range > bullet_left and bullet_dir == 3) or (player_left > bullet_left and player_left - range < bullet_left and bullet_dir == 1)):
					return 0
			# left part of player tank
			if ((bullet_right > player_left and bullet_right <= player_left + 10) or (bullet_v_mid > player_left and bullet_v_mid <= player_left + 10)):
				if ((player_top < bullet_top and player_top + range > bullet_top and bullet_dir == 0) or (player_top > bullet_top and player_top - range < bullet_top and bullet_dir == 2)):
					return 1
			# right part of player tank
			if (bullet_left > player_left + 16 and bullet_left <= player_left + 26 or (bullet_v_mid > player_left + 16 and bullet_v_mid <= player_left + 26)):
				if ((player_top < bullet_top and player_top + range > bullet_top and bullet_dir == 0) or (player_top > bullet_top and player_top - range < bullet_top and bullet_dir == 2)):
					return 3

		return -1

	def check_bullets(self, bullets):
		for bullet in bullets:
			encoded_bullet_left = bullet[0][0] / 32
			encoded_bullet_top = bullet[0][1] / 32
			encoded_bullet_right = (bullet[0][0] + bullet[0][2]) / 32
			encoded_bullet_bottom = (bullet[0][1] + bullet[0][3]) / 32
			bullet_dir = bullet[1]

			if (encoded_bullet_left == self.encoded_player_left):
				if (encoded_bullet_top < self.encoded_player_top and bullet_dir == 2):
					return 0
				elif (encoded_bullet_top > self.encoded_player_top and bullet_dir == 0):
					return 2

			if (encoded_bullet_top == self.encoded_player_top):
				if (encoded_bullet_left < self.encoded_player_left and bullet_dir == 1):
					return 3
				elif (encoded_bullet_left > self.encoded_player_left and bullet_dir == 3):
					return 1

		return -1

	def check_tanks(self):
		for i in range(4):
			current_left = self.encoded_player_left
			current_top = self.encoded_player_top
			for j in range(5):
				current_left = current_left + self.dir_left[i]
				current_top = current_top + self.dir_top[i]
				if (current_left < 0 or current_left >= 13 or current_top < 0 or current_top >= 13 or self.encoded_map[current_top][current_left] == '@'):
					break
				if (self.encoded_map[current_top][current_left] == 'E'):
					return i

		return -1

	def bfs(self):
		q = Queue.Queue()

		player_left = 0
		player_top = 0

		for i in range(self.map_height):
			for j in range(self.map_width):
				if (self.encoded_map[i][j] == 'P'):
					player_top = i
					player_left = j
					break

		# record whether the position has been visited
		visited = [[False for x in range(self.map_width)] for y in range(self.map_height)]
		
		visited[player_top][player_left] = True
		# put first 4 block into queue.
		for i in range(4):
			new_top = player_top + self.dir_top[i]
			new_left = player_left + self.dir_left[i]
			if (new_left < 0 or new_left >= 13 or new_top < 0 or new_top >= 13 or self.dangerous_map[new_top][new_left] == True):
				continue
			if (self.encoded_map[new_top][new_left] != '@'):
				q.put([new_top, new_left, i])
				visited[new_top][new_left] = True

		result_move = -1

		while not q.empty():
			temp = q.get()
			current_top = temp[0]
			current_left = temp[1]
			direction = temp[2]
			visited[current_top][current_left] = True

			if (self.encoded_map[current_top][current_left] == 'E'):
				# print "found enemy"
				result_move = direction
				return result_move

			for i in range(4):
				new_top = current_top + self.dir_top[i]
				new_left = current_left + self.dir_left[i]
				if (new_left < 0 or new_left >= 13 or new_top < 0 or new_top >= 13):
					continue
				if (visited[new_top][new_left] == False and self.encoded_map[new_top][new_left] != '@'):
					q.put([new_top, new_left, direction])

		return result_move

	def encode_map(self, bullets, enemies, tiles, player):
		result = [['_' for x in range(self.map_width)] for y in range(self.map_height)]

		for bullet in bullets:
			b_left = bullet[0][0] / 32
			b_top = bullet[0][1] / 32
			if (b_left >= 0 and b_left < 13 and b_top >= 0 and b_top < 13):
				result[b_top][b_left] = 'B'

			b_right = (bullet[0][0] + bullet[0][2]) / 32
			b_bottom = (bullet[0][1] + bullet[0][3]) / 32
			if (b_right >= 0 and b_right < 13 and b_bottom >= 0 and b_bottom < 13):
				result[b_bottom][b_right] = 'B'
			

		for enemy in enemies:
			e_left = enemy[0][0]
			e_top = enemy[0][1]
			result[e_top / 32][e_left / 32] = 'E'

		for tile in tiles:
			t_left = tile[0][0]
			t_top = tile[0][1]
			t_type = tile[1]
			if (t_type == 1 or t_type == 2 or t_type == 3):
				result[t_top / 32][t_left / 32] = '@'
	
		player_left = player[0][0]
		player_top = player[0][1]

		result[player_top / 32][player_left / 32] = 'P'
		
		self.encoded_map = result

	def generate_dangerous_map(self, bullets, enemies):
		result = [[False for x in range(self.map_width)] for y in range(self.map_height)]
		
		# put positions that bullets may pass into dangerous map
		for bullet in bullets:
			b_left = bullet[0][0] / 32
			b_top = bullet[0][1] / 32
			b_right = (bullet[0][0] + bullet[0][2]) / 32
			b_bottom = (bullet[0][1] + bullet[0][3]) / 32
			b_dir = bullet[1]

			# This situation happened before, but still reason is unknown.
			if (b_left >= 0 and b_left < 13 and b_top >= 0 and b_top < 13):
				result[b_top][b_left] = True			

			current_top = b_top
			current_left = b_left
			current_bottom = b_bottom
			current_right = b_right

			# mark next 3 blocks as dangerous
			for i in range(4):
				current_top = current_top + self.dir_top[b_dir]
				current_left = current_left + self.dir_left[b_dir]
				current_bottom = current_bottom + self.dir_top[b_dir]
				current_right = current_right + self.dir_left[b_dir]
				if (current_left >= 0 and current_left < 13 and current_top >= 0 and current_top < 13):
					result[current_top][current_left] = True
				if (current_right >= 0 and current_right < 13 and current_bottom >= 0 and current_bottom < 13):
					result[current_bottom][current_right] = True

		
		# put positions that tanks may shoot into dangerous map
		for enemy in enemies:
			e_left = enemy[0][0] / 32
			e_top = enemy[0][1] / 32
			e_dir = enemy[1]

			# This situation happened before, but still reason is unknown.
			if (e_left < 0 or e_left >= 13 or e_top < 0 or e_top >= 13):
				continue;
			
			result[e_top][e_left] = True

			current_top = e_top
			current_left = e_left

			# mark next 2 blocks as dangerous
			for i in range(2):
				current_top = current_top + self.dir_top[e_dir]
				current_left = current_left + self.dir_left[e_dir]
				if (current_left < 0 or current_left >= 13 or current_top < 0 or current_top >= 13):
					continue;
				result[current_top][current_left] = True

		self.dangerous_map = result

	def print_encoded_map(self):
		for i in range(13):
			for j in range(13):
				sys.stdout.write(self.encoded_map[i][j])
			sys.stdout.write("\n")

	def Get_mapInfo(self,p_mapinfo):
		if p_mapinfo.empty()!=True:
			try:
				self.mapinfo = p_mapinfo.get(False)
			except Queue.Empty:
				skip_this=True

	def Update_Strategy(self,c_control,shoot,move_dir,keep_action):
		if c_control.empty() ==True:
			c_control.put([shoot,move_dir,keep_action])
			return True
		else:
			return False

