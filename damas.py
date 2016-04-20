#python 3.5 64 bits
#pygame pygame-1.9.2a0-cp35-none-win_amd64

import pygame
import time
import random

gameName = "Chekers by Ariel Jimenez"

# SETINGS OR CONSTANTS#
pygame.init() 
pygame.display.set_caption(gameName) 
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock() #fps manager
FPS = 30
block_size = 70
icon = pygame.image.load("img/damas.png")
pygame.display.set_icon(icon)

#COLORS#
WHITE 	  = (255,255,255)
BLACK 	  = (0,0,0)
RED 	  = (255,0,0)
GREEN 	  = (136,170,0)
TRUEGREEN = (85, 136, 34)
BLUE 	  = (0,0,255)
BROWN 	  = (75,75,0)

#OTHERS CONSTANTS#
tablero = []
fichasB = 0
fichasN = 0
celdaSeleccionada = []
playerTurn  = 'p2'
playerEnemy = 'p1'
p1Color 	= WHITE
p1ColorDama = BLUE
p2Color     = BLACK
p2ColorDama = RED

currentPlayerEatCels = [] #tuple list with(x,y) x = pos at piece to eat, y = pos at land after eat

#showstuff
p1Score = 0
p2Score = 0
turns = 0

#FONTS#
microfont = pygame.font.SysFont('comicsansms', 15)
smallfont = pygame.font.SysFont('comicsansms', 25)
medfont   = pygame.font.SysFont('comicsansms', 50)
largefont = pygame.font.SysFont('comicsansms', 80)

fancysmallfont = pygame.font.Font('fonts/CaviarDreams.ttf', 25)
fancymedfont   = pygame.font.Font('fonts/CaviarDreams.ttf', 50)
fancylargefont = pygame.font.Font('fonts/CaviarDreams.ttf', 80)

gameOver = False
canEat = False


# #VOIDS AND STUFF#
def inicializar():
	"""Resetea los valores de los puntajes"""
	global fichasB
	global fichasN
	global p1Score
	global p2Score
	global turns

	fichasB = 12
	fichasN = 12
	p1Score = 0
	p2Score = 0
	turns = 0


def celda_selected(celda):
	""""Marca la celda seleccionada"""
	global canEat
	global celdaSeleccionada

	currentPlayerEatCels = [] 
	pos = 0
	temp = 0

	if not celdaSeleccionada == celda:
		for i in tablero:
			if not i == celda:
				tablero[pos][3] = False
			else:
				tablero[pos][3] = True
				temp = pos
			pos += 1

		celdaSeleccionada = celda 
	posibles_jugadas_R(temp) #<-------------------------


def posibles_jugadas_R(pos, dire='none'): # RECURSIVE METHOD
	"""Método que marca las posibles jugadas de la ficha seleccionada. Según las reglas debe elegir el máximo \
	   número de saltos. Además, la ficha no puede desplazarse hacia atras, solo los 'kings' pueden hacer esto."""

	global currentPlayerEatCels
	global canEat

	if playerTurn == 'p2':		
		if pos-14 >= 0 and tablero[pos-7][2] == playerEnemy and tablero[pos-14][2] == '' and tablero[pos-14][0] == 'g':
			tablero[pos-14][3] = True
			canEat = True
			currentPlayerEatCels.append([pos, pos-7, pos-14])
			posibles_jugadas_R(pos-14)

		elif not canEat and pos-7 >= 0 and tablero[pos-7][2] == '' and tablero[pos-7][0] == 'g' and tablero[pos][2] == playerTurn:
			tablero[pos-7][3] = True		

		if pos-18 >= 0 and tablero[pos-9][2] == playerEnemy and tablero[pos-18][2] == '' and tablero[pos-18][0] == 'g':
			tablero[pos-18][3] = True
			canEat = True
			currentPlayerEatCels.append([pos, pos-9, pos-18])
			posibles_jugadas_R(pos-18)

		elif not canEat and pos-9 >= 0 and tablero[pos-9][2] == '' and tablero[pos-9][0] == 'g'  and tablero[pos][2] == playerTurn:
			tablero[pos-9][3] = True

	else:
		if pos+14 <= 63 and tablero[pos+7][2] == playerEnemy and tablero[pos+14][2] == '' and tablero[pos+14][0] == 'g':
			tablero[pos+14][3] = True
			canEat = True
			currentPlayerEatCels.append([pos, pos+7, pos+14])			
			posibles_jugadas_R(pos+14)

		elif not canEat and pos+7 <= 63 and tablero[pos+7][2] == '' and tablero[pos+7][0] == 'g'  and tablero[pos][2] == playerTurn:
			tablero[pos+7][3] = True

		if pos+18 <= 63 and tablero[pos+9][2] == playerEnemy and tablero[pos+18][2] == '' and tablero[pos+18][0] == 'g':
			tablero[pos+18][3] = True
			canEat = True
			currentPlayerEatCels.append([pos, pos+9, pos+18])			
			posibles_jugadas_R(pos+18)

		elif not canEat and pos+9 <= 63 and tablero[pos+9][2] == '' and tablero[pos+9][0] == 'g'  and tablero[pos][2] == playerTurn:
			tablero[pos+9][3] = True
	

def ficha_tomada(celda):
	global currentPlayerEatCels

	celda_selected(celda)

	if playerTurn == 'p1':
		color = p1Color
	else:
		color = p2Color

	grab = True

	while grab:
		for event in pygame.event.get():
			mouseX, mouseY = pygame.mouse.get_pos()
			
			if pygame.mouse.get_pressed()[0]:				
				pygame.draw.circle(gameDisplay, color, (mouseX, mouseY), block_size-40, 0)			

			if event.type == pygame.MOUSEBUTTONUP:				
				celdaDestino = enc_coordenadas(mouseX, mouseY)
				pos = tablero.index(celdaDestino)
				
				if not celdaSeleccionada == celdaDestino and tablero[pos][0] == 'g' and celdaDestino[3]: #movimiento a una celda vacia
					setMovimiento(celdaSeleccionada, celdaDestino)
					change_turn()
				
				grab = False

			pygame.display.update()
			dibuja_tablero()
			clock.tick(FPS)


def enc_coordenadas(mouseX, mouseY):
	for celda in tablero:
		if  mouseX >= celda[1][0] and mouseX <= celda[1][0] + block_size and \
			mouseY >= celda[1][1] and mouseY <= celda[1][1] + block_size :
			return celda


def setMovimiento(celdaOrigen, celdaDestino): # celda es una lista con la data de la celda
	global currentPlayerEatCels
	global tablero	

	posOrigen = tablero.index(celdaOrigen)
	posDestino = tablero.index(celdaDestino)	
	fichaPlayer = tablero[posOrigen][2]	

	print(currentPlayerEatCels)
	print(posOrigen, posDestino)

	if len(currentPlayerEatCels) > 0:
		for cel in currentPlayerEatCels:
			if cel[2] == posDestino:	

				limpiar_celdas_duplicadas()				

				if posDestino == currentPlayerEatCels[-1][2]: #si laposicion destino not es igual al ultimo land de la ficha
					comer_fichas(fichaPlayer)
					currentPlayerEatCels = [] # reset

				#else:	
					

					# for celda in currentPlayerEatCels:
					# 	if celda[2] == posDestino:
					# 		currentPlayerEatCels = currentPlayerEatCels[:currentPlayerEatCels.index(celda)+1]

					# comer_fichas(fichaPlayer)
	
	tablero[posOrigen][2], tablero[posDestino][2] = '', fichaPlayer
	
	if   fichaPlayer == 'p1' and posDestino >= 56:
		coronar_ficha(posDestino)
	elif fichaPlayer == 'p2' and posDestino <= 8:		
		coronar_ficha(posDestino)


def coronar_ficha(pos):
	tablero[pos][4] = True


def change_turn():
	global playerTurn
	global playerEnemy
	global turns
	global gameOver

	if fichasB == 0 or fichasN == 0:
		gameOver = True

	for pos in range(0,64):
		tablero[pos][3] = False

	if playerTurn  == 'p1':
		playerTurn  = 'p2'
		playerEnemy = 'p1'
	else:
		playerTurn  = 'p1'
		playerEnemy = 'p2'
	turns += 1


def comer_fichas(fichaPlayer):#lauch time
	global canEat

	for celda in currentPlayerEatCels:		
		tablero[celda[1]][2] = '' #eat up and clean out the cel
		incrementa_score(fichaPlayer)

	canEat = False


def limpiar_celdas_duplicadas():
	global currentPlayerEatCels

	for curCelda in currentPlayerEatCels:		

		for celda in currentPlayerEatCels:
			if not curCelda == celda and curCelda[1] == celda[1]:
				currentPlayerEatCels.remove(celda)	


def armar_tablero():
	# g = gris v = verde
	x = 0
	y = 0
	celdaColor = ""

	for celda in range(1,65):
		if celda % 2 == 0:
			celdaColor = 'w'
		else:
			celdaColor = 'g'

		tablero.append([celdaColor,(x,y),'', False, False])

		x += block_size

		if x >= block_size * 8:
			y += block_size
			x = 0

	# corrigue algunas anomalias para mostarse corecctamente las celdas
	ini = 'w'
	pos = 0

	for celda in tablero:
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

	# pone las fichas en posicion incial
	global fichasB
	global fichasN
	pos = 1
	
	for celda in tablero:
		if celda[0] == 'g': #
			if pos <= 24:
				celda[2] = "p1"
				fichasB += 1

			elif pos > 40:	
				celda[2] = "p2"	
				fichasN += 1
		pos += 1	


def dibuja_tablero():	
	
	for celda in tablero:
		if celda[0] == 'w':
			pygame.draw.rect(gameDisplay, WHITE,  (celda[1][0], celda[1][1], block_size, block_size), 0)
		else:
			pygame.draw.rect(gameDisplay, TRUEGREEN,  (celda[1][0], celda[1][1], block_size, block_size), 0)	

		if celda[2] == 'p1':
			pygame.draw.circle(gameDisplay, p1Color, (celda[1][0]+block_size//2, celda[1][1]+block_size//2), 20, 0)
		elif celda[2] == 'p2':
			pygame.draw.circle(gameDisplay, p2Color, (celda[1][0]+block_size//2, celda[1][1]+block_size//2), 20, 0)

		if celda[3]:
			pygame.draw.rect(gameDisplay, RED,  (celda[1][0]+10, celda[1][1]+10, block_size-20, block_size-20), 2)

		if   celda[4] and celda[2] == 'p1': #dama
			pygame.draw.circle(gameDisplay, p1ColorDama, (celda[1][0]+block_size//2, celda[1][1]+block_size//2), 20, 0)
		elif celda[4] and celda[2] == 'p2':
			pygame.draw.circle(gameDisplay, p2ColorDama, (celda[1][0]+block_size//2, celda[1][1]+block_size//2), 20, 0)


def incrementa_score(ficha):
	global p1Score
	global p2Score
	global fichasB
	global fichasN

	if ficha == 'p1':
		p1Score += 10
		fichasN -= 1
	else:
		p2Score += 10
		fichasB -= 1


def show_score(score): #in the score panel
	turnos 	  = microfont.render("Turnos: "+ str(score), True, BLUE)
	p1puntaje = microfont.render("Jugador 1 : "+ str(p1Score), True, BLUE)
	p2puntaje = microfont.render("Jugador 2 : "+ str(p2Score), True, BLUE)
	p1fichas  = microfont.render("Fichas Blancas : "+ str(fichasB), True, BLUE)
	p2fichas  = microfont.render("Fichas Negras : "+ str(fichasN), True, BLUE)
	turno 	  = microfont.render("Turno del Jugador : "+ str(playerTurn), True, RED)

	gameDisplay.blit(turnos,    [620, 0])
	gameDisplay.blit(p1puntaje, [620,20])
	gameDisplay.blit(p2puntaje, [620,40])
	gameDisplay.blit(p1fichas,  [620,60])
	gameDisplay.blit(p2fichas,  [620,80])
	gameDisplay.blit(turno,     [620,100])


def msg_to_screen(msg, color, y_display=0, size='small'): # y_display = 0 its a default value, if this param not given, 0 ill be taken
	textSurf, textRect = text_objects(msg, color, size)
	textRect.center = (display_width/2), (display_height/2) + y_display
	gameDisplay.blit(textSurf, textRect)

def text_objects(text, color, size):
	if size == 'small': 
		textSurface = smallfont.render(text, True, color)
	elif size == 'med': 
		textSurface = medfont.render(text, True, color)
	elif size == 'large': 
		textSurface = largefont.render(text, True, color)
	elif size == 'fancysmall': 
		textSurface = fancysmallfont.render(text, True, color)
	elif size == 'fancymed': 
		textSurface = fancymedfont.render(text, True, color)
	elif size == 'fancylarge': 
		textSurface = fancylargefont.render(text, True, color)
	return textSurface, textSurface.get_rect()

def game_loop():
	global tablero
	global gameOver

	gameExit = False
	gameOver = False	

	gameDisplay.fill(WHITE)	
	armar_tablero()	# tambien updatea el tablero con los valores correctos de las celdas	

	while not gameExit:
		gameDisplay.fill(WHITE)		
		dibuja_tablero() 
		show_score(turns)

		while gameOver == True:
			gameDisplay.fill(WHITE)
			msg_to_screen('Game Over ' + str(playerTurn)+' loose', RED, -15, 'fancylarge')
			msg_to_screen('Press C to continue or Q to quit.', BLACK, 50, 'med')
			pygame.display.update()

			for event in pygame.event.get():				
				if event.type == pygame.QUIT:
			 		gameExit = True
			 		gameOver = False			 		

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
						
					if event.key == pygame.K_c:
						inicializar()
						game_loop()
		

		if pygame.mouse.get_pressed()[0]:
			(mouseX, mouseY) = pygame.mouse.get_pos()			

			if (mouseX >= 0 and mouseX < 8 * block_size) and (mouseY > 0 and mouseY < 8 * block_size):
				celdaClicked = enc_coordenadas(mouseX, mouseY)
				pos = tablero.index(celdaClicked)			

				if tablero[pos][2] == playerTurn: 
					ficha_tomada(celdaClicked)

		for event in pygame.event.get():			

			if event.type == pygame.QUIT:			 	
			 	gameExit = True
			 	gameOver = False		

		pygame.display.update()		
		clock.tick(FPS)	

	pygame.quit()
	quit() 

#==============================#
game_loop()


