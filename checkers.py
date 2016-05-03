#python 3.5 64 bits
#pygame pygame-1.9.2a0-cp35-none-win_amd64
#bajo licencia GPLv3  >:v

import pygame
import time

class Checkers():
	"""Clase que define un Juego de Damas."""

	def __init__(self):
		# SETINGS OR CONSTANTS#
		pygame.init()
		pygame.display.set_caption("Chekers by Ariel Jiménez")
		self.display_width = 800
		self.display_height = 600
		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		self.clock = pygame.time.Clock() #fps manager
		self.FPS = 30
		self.block_size = 70
		pygame.display.set_icon(pygame.image.load("img/damas.png"))

		#COLORS#
		self.WHITE 	  = (255,255,255)
		self.BLACK 	  = (0,0,0)
		self.RED 	  = (255,0,0)
		self.GREEN 	  = (136,170,0)
		self.TRUEGREEN= (85,136,34)
		self.BLUE 	  = (0,0,255)
		self.BLUE2	  = (93,130,217)
		self.BROWN 	  = (75,75,0)
		self.YELOW    = (255,255,0)
		self.GRAY	  = (230,230,230)

		#GLOBAL VARS#
		self.tablero = []
		self.fichasB = 0
		self.fichasN = 0
		self.celdaSeleccionada = []
		self.movN  = [] #lista de movimientos normales [x, y] x actual pos , y land pos
		self.movJ  = [] #lista de movimientos con salto [x,y,z] x actual pos, y enemy pos, z land pos
		self.movKN = []
		self.movKJ = []
		self.playerTurn  = 'p2'
		self.playerEnemy = 'p1'
		self.p1Color     = self.WHITE
		self.p1ColorDama = self.BLUE
		self.p2Color     = self.BLACK
		self.p2ColorDama = self.RED

		#showstuff
		self.p1Score = 0
		self.p2Score = 0
		self.turns   = 0

		#FONTS#
		self.microfont 		= pygame.font.SysFont('comicsansms', 15)
		self.smallfont 		= pygame.font.SysFont('comicsansms', 25)
		self.medfont   		= pygame.font.SysFont('comicsansms', 50)
		self.largefont 		= pygame.font.SysFont('comicsansms', 80)

		self.fancysmallfont = pygame.font.Font('fonts/CaviarDreams.ttf', 25)
		self.fancymedfont   = pygame.font.Font('fonts/CaviarDreams.ttf', 50)
		self.fancylargefont = pygame.font.Font('fonts/CaviarDreams.ttf', 80)

		self.canJump  = False
		self.gameOver = False


	##################################################################################################
	############################### V O I D S   A N D   S T U F F ####################################
	##################################################################################################

	def verify_all_jumps(self, posOri):
		"""Verifica si el jugador puede saltar (comer) una ficha."""

		self.movJ  = []
		self.movKN = []
		self.movKJ = []
		self.canJump = False

		for pos in range(0,64):
			if self.tablero[pos][4] == 'k' and self.playerTurn == self.tablero[pos][2]:
				for n in range(pos, 0,-7):
					if n-7 >=0 and self.tablero[n-7][2] == '' and self.tablero[n-7][0] == 'g':
						if [n, n-7] not in self.movKN:
							self.movKN.append([n, n-7])

					elif n-14 >=0 and self.tablero[n-7][2] == self.playerEnemy and self.tablero[n-14][2] == '' and self.tablero[n-14][0] == 'g' :
						if [n, n-7, n-14] not in self.movKJ:
							self.movKJ.append([posOri, n-7, n-14])
					else:
						break

				for n in range(pos, 0,-9):
					if n-9 >=0 and self.tablero[n-9][2] == '' and self.tablero[n-9][0] == 'g':
						if [n, n-9] not in self.movKN:
							self.movKN.append([n, n-9])

					elif n-18 >=0 and self.tablero[n-9][2] == self.playerEnemy and self.tablero[n-18][2] == '' and self.tablero[n-18][0] == 'g' :
						if [n, n-9, n-18] not in self.movKJ:
							self.movKJ.append([posOri, n-9, n-18])
					else:
						break

				for n in range(pos, 63,7):
					if n+7 <= 63 and self.tablero[n+7][2] == '' and self.tablero[n+7][0] == 'g':
						if [n, n+7] not in self.movKN:
							self.movKN.append([n, n+7])

					elif n+14 <= 63 and self.tablero[n+7][2] == self.playerEnemy and self.tablero[n+14][2] == '' and self.tablero[n+14][0] == 'g' :
						if [n, n+7, n+14] not in self.movKJ:
							self.movKJ.append([posOri, n+7, n+14])
					else:
						break

				for n in range(pos, 63,9):
					if n+9 <= 63 and self.tablero[n+9][2] == '' and self.tablero[n+9][0] == 'g':
						if [n, n+9] not in self.movKN:
							self.movKN.append([n, n+9])

					elif n+18 <= 63 and self.tablero[n+9][2] == self.playerEnemy and self.tablero[n+18][2] == '' and self.tablero[n+18][0] == 'g' :
						if [n, n+9, n+18] not in self.movKJ:
							self.movKJ.append([posOri, n+9, n+18])
					else:
						break
			else:
				if self.tablero[pos][2] == 'p2' :
					if self.playerTurn == 'p2' and not self.tablero[pos][4] == 'k':
						if pos-18 >= 0 and self.tablero[pos-9][2] == self.playerEnemy and self.tablero[pos-18][2] == '' and self.tablero[pos-18][0] == 'g':
							if not self.movJ or not any(pos-18 == x[1] for x in self.movJ):
								self.movJ.append([pos, pos-9, pos-18])

						if pos-14 >= 0 and self.tablero[pos-7][2] == self.playerEnemy and self.tablero[pos-14][2] == '' and self.tablero[pos-14][0] == 'g':
							if not self.movJ or not any(pos-14 == x[1] for x in self.movJ):
								self.movJ.append([pos, pos-7, pos-14])

				elif self.tablero[pos][2] == 'p1':
					if self.playerTurn == 'p1' and not self.tablero[pos][4] == 'k':
						if pos+18 <= 63 and self.tablero[pos+9][2] == self.playerEnemy and self.tablero[pos+18][2] == '' and self.tablero[pos+18][0] == 'g':
							if not self.movJ or not any(pos+18 == x[1] for x in self.movJ):
								self.movJ.append([pos, pos+9, pos+18])

						if pos+14 <= 63 and self.tablero[pos+7][2] == self.playerEnemy and self.tablero[pos+14][2] == '' and self.tablero[pos+14][0] == 'g':
							if not self.movJ or not any(pos+14 == x[1] for x in self.movJ):
								self.movJ.append([pos, pos+7, pos+14])


		if self.movKN and self.tablero[self.tablero.index(self.celdaSeleccionada)][4] == 'k' \
		and any(self.tablero.index(self.celdaSeleccionada) == x[0] for x in self.movKN):
			for cel in self.movKN:
				self.tablero[cel[1]][3] = True # marks path

		if self.movKJ and self.tablero[self.tablero.index(self.celdaSeleccionada)][4] == 'k' \
		and any(self.tablero.index(self.celdaSeleccionada) == x[0] for x in self.movKJ):
			self.canJump = True
			for cel in self.movKJ:
				self.tablero[cel[2]][3] = True # marks the cel behind the enemy

		elif self.movJ:
			self.canJump = True
			for cel in self.movJ:
				self.tablero[cel[0]][3] = True
				self.tablero[cel[2]][3] = True
		# else:
		# 	self.canJump = False

		self.movKN = []


	def mark_legal_moves(self, pos):
		"""Marca gráficamente las posibles jugadas del jugador."""

		self.verify_all_jumps(pos) # to really make sure that the player cant jump

		#normal ones
		if not self.canJump and not self.movKJ:
			if self.playerTurn == 'p2' and not self.tablero[pos][4] == 'k':# and pos-18 >= 0 and not self.tablero[pos-18][3] and pos-14 >= 0 and not self.tablero[pos-14][3]:
				if pos-9 >= 0 and self.tablero[pos-9][2] == '':
					if not self.movN or not any(pos-9 == x[1] for x in self.movN):
						self.movN.append([pos, pos-9])

				if pos-7 >= 0 and self.tablero[pos-7][2] == '':
					if not self.movN or not any(pos-7 == x[1] for x in self.movN):
						self.movN.append([pos, pos-7])

			if self.playerTurn == 'p1' and not self.tablero[pos][4] == 'k':# and pos+18 <= 63 and not self.tablero[pos+18][3] and pos+14 <= 63 and not self.tablero[pos+14][3]:
				if pos+9 <= 63 and self.tablero[pos+9][2] == '':
					if not self.movN or not any(pos+9 == x[1] for x in self.movN):
						self.movN.append([pos, pos+9])

				if pos+7 <= 63 and self.tablero[pos+7][2] == '':
					if not self.movN or not any(pos+7 == x[1] for x in self.movN):
						self.movN.append([pos, pos+7])

			for cel in self.movN:
				self.tablero[cel[1]][3] = True

		self.movN = []


	def ficha_on_drag(self, celda, posOrigen):
		"""Muestra sobre el tablero la ficha sostenida."""

		if self.playerTurn == 'p1':
			if celda[4] == 'n':
				color = self.p1Color
			else:
				color = self.p1ColorDama
		else:
			if celda[4] == 'n':
				color = self.p2Color
			else:
				color = self.p2ColorDama

		for i in range(0,64): # turn off all except the selected cel
			if i == self.tablero.index(celda) and not self.canJump:
				self.tablero[i][3] = True
			else:
				self.tablero[i][3] = False

		self.mark_legal_moves(posOrigen)

		grab = True

		while grab:
			for event in pygame.event.get():
				mouseX, mouseY = pygame.mouse.get_pos()

				if pygame.mouse.get_pressed()[0]:
					pygame.draw.circle(self.gameDisplay, color, (mouseX, mouseY), self.block_size-40, 0)

				if event.type == pygame.MOUSEBUTTONUP:
					celdaDestino = self.enc_coordenadas(mouseX, mouseY)
					posDestino = self.tablero.index(celdaDestino)

					if not self.celdaSeleccionada == celdaDestino and mouseX < 8*self.block_size and mouseY < 8*self.block_size \
					 and self.tablero[posDestino][3]:

						if self.movKJ:
							if any(posOrigen == x[0] for x in self.movKJ):
						 		self.make_jump(self.movKJ, posOrigen, posDestino)

						elif self.movJ:
						 	self.make_jump(self.movJ, posOrigen, posDestino)

						else:
							self.tablero[posDestino][2:], self.tablero[posOrigen][2:] = self.tablero[posOrigen][2:], self.tablero[posDestino][2:]

						if posDestino > 55 or posDestino < 9:
							self.tablero[posDestino][4] = 'k'

						if not self.canJump: # if the player still can jump, his turn isnt over
							self.change_turn()

					grab = False

				pygame.display.update()
				self.gameDisplay.fill(self.GRAY)
				self.dibuja_tablero()
				self.show_score(self.turns)
				self.clock.tick(self.FPS)


	def make_jump(self, lista, posOri, posDes):
		"""Maneja los saltos de las fichas."""

		for cel in lista:
			if cel[0] == posOri and cel[2] == posDes:
				self.tablero[cel[1]][2] = ''
				self.tablero[posDes][2:],self.tablero[posOri][2:] = self.tablero[posOri][2:],self.tablero[posDes][2:]
				self.incrementa_score(self.playerTurn)

				self.mark_legal_moves(posDes)
				#self.verify_all_jumps(posDes)

				if self.movKJ:
					self.canJump = True

				if not self.canJump and self.movJ and not any(posDes == x[0] for x in self.movJ): # if the landpos != posDes, turn over
					for i in range(0,64): #turn_off_all_cells():
						self.tablero[i][3] = False

					#self.canJump = False

				break


	#==========================================================================================================#
	#=================================== ALMOST LEGACY STUFF ==================================================#
	#==========================================================================================================#

	def game_intro(self):
		"""Muestra la introducción al juego."""

		intro = True
		self.gameDisplay.fill(self.WHITE)

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_s:
							pygame.quit()
							quit()
						if event.key == pygame.K_j:
							intro = False

			self.msg_to_screen("JUEGO DE DAMAS", self.BLUE, -135, 'fancylarge')
			self.msg_to_screen("(Chekers)", self.BLACK, -55, 'fancymed')
			self.msg_to_screen("El jugador que logre 'comer' todas las piezas del enemigo", self.BLACK, 0, 'small')
			self.msg_to_screen("¡GANA!", self.RED, 45, 'fancymed')
			self.msg_to_screen("Presiona J para empezar a jugar o S para salir", self.BLACK, 80, 'small')
			self.msg_to_screen("Presiona P o ENTER para pausar el jeugo.", self.BLUE2, 120, 'small')

			pygame.display.update()
			self.clock.tick(10)


	def game_pause(self):
		"""Pausa el juego."""

		paused = True
		self.gameDisplay.fill(self.WHITE)

		while paused:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						paused = False

					elif event.key == pygame.K_s:
						pygame.quit()
						quit()

			self.msg_to_screen("JUEGO PAUSADO", self.BLACK, -100, "large")
			self.msg_to_screen("Presiona C para continuar o S para salir.", self.BLACK, 25)

			pygame.display.update()
			self.clock.tick(5)


	def inicializar(self):
		"""Resetea los valores de los puntajes."""

		self.playerTurn = 'p2'

		self.p1Score = 0
		self.p2Score = 0
		self.turns = 0
		self.tablero = []
		self.movimientoS = []
		self.movimientoN = []


	def enc_coordenadas(self, mouseX, mouseY):
		"""Returns la celda correspondientes a las cordenadas suministradas"""

		for celda in self.tablero:
			if  mouseX >= celda[1][0] and mouseX <= celda[1][0] + self.block_size and \
				mouseY >= celda[1][1] and mouseY <= celda[1][1] + self.block_size :
				return celda


	def change_turn(self):
		"""Maneja los cambios de turno y define el GameOver."""

		if self.fichasB == 0 or self.fichasN == 0:
			self.gameOver = True

		for pos in range(0,64):
			self.tablero[pos][3] = False

		if self.playerTurn  == 'p1':
			self.playerTurn  = 'p2'
			self.playerEnemy = 'p1'
		else:
			self.playerTurn  = 'p1'
			self.playerEnemy = 'p2'

		self.turns += 1


	def armar_tablero(self):
		"""Crea una una lista donde contendrá las posiciones iniciales del juego."""

		# g = gris v = verde
		x = 0
		y = 0
		celdaColor = ""

		for celda in range(1,65):
			if celda % 2 == 0:
				celdaColor = 'w'
			else:
				celdaColor = 'g'

			self.tablero.append([celdaColor,(x,y),'', False, 'n'])

			x += self.block_size

			if x >= self.block_size * 8:
				y += self.block_size
				x = 0

		# corrigue algunas anomalias para mostarse corecctamente las celdas
		ini = 'w'
		pos = 0

		for celda in self.tablero:
			if celda[0] == ini:
				celda[0] = 'w'	# modificamos su valor para mostrarlo correctamente
			else:
				celda[0] = 'g'
			pos += 1

			if pos % 8 == 0:
				if ini == 'g':
					ini = 'w'
				else:
					ini = 'g'
		pos = 1

		for celda in self.tablero:
			if celda[0] == 'g': #
				if pos <= 24:
					celda[2] = "p1"
					self.fichasB += 1

				elif pos > 40:
					celda[2] = "p2"
					self.fichasN += 1
			pos += 1


	def dibuja_tablero(self):
		"""Dibuja lo que contiene la lista tablero[]."""

		for celda in self.tablero:
			if celda[0] == 'w':
				pygame.draw.rect(self.gameDisplay, self.WHITE,  (celda[1][0], celda[1][1], self.block_size, self.block_size), 0)
			else:
				pygame.draw.rect(self.gameDisplay, self.TRUEGREEN,  (celda[1][0], celda[1][1], self.block_size, self.block_size), 0)

			if celda[2] == 'p1':
				pygame.draw.circle(self.gameDisplay, self.p1Color, (celda[1][0]+self.block_size//2, celda[1][1]+self.block_size//2), 20, 0)
			elif celda[2] == 'p2':
				pygame.draw.circle(self.gameDisplay, self.p2Color, (celda[1][0]+self.block_size//2, celda[1][1]+self.block_size//2), 20, 0)

			if celda[3] and celda[0] == 'g': #NAIZSU
				pygame.draw.rect(self.gameDisplay, self.RED,  (celda[1][0]+10, celda[1][1]+10, self.block_size-20, self.block_size-20), 2)

			if celda[4] == 'k' and celda[2] == 'p1': #king-sama-desu
				pygame.draw.circle(self.gameDisplay, self.p1ColorDama, (celda[1][0]+self.block_size//2, celda[1][1]+self.block_size//2), 20, 0)
			elif celda[4] == 'k' and celda[2] == 'p2':
				pygame.draw.circle(self.gameDisplay, self.p2ColorDama, (celda[1][0]+self.block_size//2, celda[1][1]+self.block_size//2), 20, 0)


	def incrementa_score(self, player):
		"""Incremente la puntuación de un jugador dado. Esto conlleva a la disminución de fichas del enemigo."""

		if player == 'p1':
			self.p1Score += 10
			self.fichasN -= 1
		else:
			self.p2Score += 10
			self.fichasB -= 1


	def show_score(self, score): #in the score panel
		"""Muestra la puntuación de los jugadores en el canvas."""

		turnos 	  = self.microfont.render("Turnos    : "+ str(score), True, self.BLUE)
		p1puntaje = self.microfont.render("Jugador 1 : "+ str(self.p1Score), True, self.BLUE)
		p2puntaje = self.microfont.render("Jugador 2 : "+ str(self.p2Score), True, self.BLUE)
		p1fichas  = self.microfont.render("Fichas Blancas    : "+ str(self.fichasB), True, self.BLUE)
		p2fichas  = self.microfont.render("Fichas Negras     : "+ str(self.fichasN), True, self.BLUE)
		turno 	  = self.microfont.render("Turno del Jugador : "+ str(self.playerTurn), True, self.RED)
		p1king 	  = self.microfont.render("p1 Damas : ", True, self.BLUE)
		p2king 	  = self.microfont.render("p2 Damas : ", True, self.RED)

		self.gameDisplay.blit(turnos,    [565, 0])
		self.gameDisplay.blit(p1puntaje, [565,20])
		self.gameDisplay.blit(p2puntaje, [565,40])
		self.gameDisplay.blit(p1fichas,  [565,60])
		self.gameDisplay.blit(p2fichas,  [565,80])
		self.gameDisplay.blit(turno,     [565,100])
		self.gameDisplay.blit(p1king,    [565,130])
		self.gameDisplay.blit(p2king,    [565,200])

		pygame.draw.circle(self.gameDisplay, self.p1ColorDama, (670, 140), 20, 0)
		pygame.draw.circle(self.gameDisplay, self.p2ColorDama, (670, 210), 20, 0)


	def msg_to_screen(self, msg, color, y_display=0, size='small'): # y_display = 0 its a default value, if this param not given, 0 ill be taken
		"""Maneja los mensajes en la pantalla."""

		textSurf, textRect = self.text_objects(msg, color, size)
		textRect.center = (self.display_width/2), (self.display_height/2) + y_display
		self.gameDisplay.blit(textSurf, textRect)

	def text_objects(self, text, color, size):
		"""Renderiza el texto en el Canvas."""

		if size == 'small':
			textSurface = self.smallfont.render(text, True, color)
		elif size == 'med':
			textSurface = self.medfont.render(text, True, color)
		elif size == 'large':
			textSurface = self.largefont.render(text, True, color)
		elif size == 'fancysmall':
			textSurface = self.fancysmallfont.render(text, True, color)
		elif size == 'fancymed':
			textSurface = self.fancymedfont.render(text, True, color)
		elif size == 'fancylarge':
			textSurface = self.fancylargefont.render(text, True, color)
		return textSurface, textSurface.get_rect()


	def game_loop(self):
		"""Método principal del juego."""

		gameExit = False
		self.gameOver = False

		self.armar_tablero()	# tambien updatea el self.tablero con los valores correctos de las celdas

		while not gameExit:
			self.gameDisplay.fill(self.GRAY)
			self.dibuja_tablero()
			self.show_score(self.turns)

			while self.gameOver == True:
				self.gameDisplay.fill(self.WHITE)
				self.msg_to_screen('Game Over', self.RED, -95, 'fancylarge')
				self.msg_to_screen(str(self.playerTurn)+' pierde', self.RED, -15, 'med')
				self.msg_to_screen('Presiona C para continuar o S para salir.', self.BLACK, 50, 'small')
				pygame.display.update()

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
				 		gameExit = True
				 		self.gameOver = False

					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_s:
							gameExit = True
							self.gameOver = False

						if event.key == pygame.K_c:
							self.inicializar()
							self.game_loop()

			if pygame.mouse.get_pressed()[0]:
				(mouseX, mouseY) = pygame.mouse.get_pos()

				if (mouseX >= 0 and mouseX < 8 * self.block_size) and (mouseY > 0 and mouseY < 8 * self.block_size):
					self.celdaSeleccionada = self.enc_coordenadas(mouseX, mouseY)
					pos = self.tablero.index(self.celdaSeleccionada)

					if self.tablero[pos][2] == self.playerTurn:
						self.ficha_on_drag(self.celdaSeleccionada, pos)

			for event in pygame.event.get():

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
						self.game_pause()

				if event.type == pygame.QUIT:
				 	gameExit = True
				 	self.gameOver = False

			pygame.display.update()
			self.clock.tick(self.FPS)

		pygame.quit()
		quit()
#===================================================================================================================#