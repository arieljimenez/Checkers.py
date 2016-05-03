
import checkers
import pygame


obj = checkers.Checkers()

obj.game_intro()
obj.game_loop()

# #==================================================


# pygame.init()
# display_width = 800
# display_height = 600
# gameDisplay = pygame.display.set_mode((display_width,display_height))
# clock = pygame.time.Clock() #fps manager
# FPS = 30
# block_size = 70

# #COLORS#
# WHITE 	  = (255,255,255)
# BLACK 	  = (0,0,0)
# RED 	  = (255,0,0)
# GREEN 	  = (136,170,0)
# TRUEGREEN= (85,136,34)
# BLUE 	  = (0,0,255)
# BLUE2	  = (93,130,217)
# BROWN 	  = (75,75,0)
# YELOW    = (255,255,0)
# GRAY	  = (230,230,230)



# def game_loop():
# 	"""Método principal del juego."""

# 	gameExit = False
# 	gameOver = False


# 	while not gameExit:
# 		gameDisplay.fill(WHITE)

# 		pygame.draw.circle(gameDisplay, BLACK, (60, 60), 20, 0)

# 		for event in pygame.event.get():

# 			if event.type == pygame.KEYDOWN:
# 				if event.key == pygame.K_p or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
# 					game_pause()

# 			if event.type == pygame.QUIT:
# 			 	gameExit = True
# 			 	gameOver = False

# 		pygame.display.update()
# 		clock.tick(FPS)

# 	pygame.quit()
# 	quit()


# ######################################

# game_loop()

