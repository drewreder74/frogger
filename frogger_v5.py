import pygame, sys
from random import randint

pygame.init()

size = width, height = 595, 735
screen = pygame.display.set_mode(size)
pygame.display.set_caption('FROGGER')
clock = pygame.time.Clock()

white = 255, 255, 255
black = 0, 0, 0
green = 150, 236, 150
red = 255, 0, 0
font_name = pygame.font.match_font('arial')

artDir = "/Users/drewreder/github/frogger/frogger_sprites/"

### FROG / SPRITESHEET INFO
FROG_H = 30
FROG_W = 32
curFrogFrameX = 0
curFrogFrameY = 0
lives = 3
frogOnLog = False
win = False
end = False

###CAR INFO
carLeftSpeed = 2
carRightSpeed = 1
CAR_H = 26
CAR_W = 24

### Log Info
logSpeed = 1
LOG_W = 116
LOG_H = 22

### WATER INFO
WATER_W = 600
WATER_H = 175

### MOVEMENT
x_change = 0
y_change = 0

### SPRITES CLASSES
class Frog(object):
		def __init__(self, x1, y1):
				self.image = pygame.image.load(artDir + "frogger_frog4.png").convert()
				#self.image = pygame.image.load("/Users/drewreder/OneDrive/CODE/Python/frogger_sprites/frogger_frog2.png").convert()
				self.image.set_colorkey((255,255,255))
				self.x = x1
				self.y = y1

		def draw(self, surface):
				surface.blit(self.image, (self.x, self.y),(curFrogFrameX*FROG_W, curFrogFrameY*FROG_H, FROG_W, FROG_H))

class Path(object):
	def __init__(self, x1, y1):
		self.image = pygame.image.load(artDir + "frogger_path.png")
		#self.image = pygame.image.load("/Users/drewreder/OneDrive/CODE/Python/frogger_sprites/frogger_path.png").convert()
		self.x = x1
		self.y = y1

	def draw(self, surface):
		surface.blit(self.image, (self.x, self.y))

class Road(object):
		def __init__(self, x1, y1):
				self.image = pygame.image.load(artDir + "frogger_road.png")
				#self.image = pygame.image.load("/Users/drewreder/OneDrive/CODE/Python/frogger_sprites/frogger_road.png").convert()
				self.x = x1
				self.y = y1

		def draw(self, surface):
				surface.blit(self.image, (self.x, self.y))

class Water(object):
		def __init__(self, x1, y1):
				self.image = pygame.image.load(artDir + "frogger_water.png")
				#self.image = pygame.image.load("/Users/drewreder/OneDrive/CODE/Python/frogger_sprites/frogger_water.png").convert()
				self.x = x1
				self.y = y1

		def draw(self, surface):
				surface.blit(self.image, (self.x, self.y))

class carRight(object):
	def __init__(self, path, x1, y1):
				self.image = pygame.image.load(path)
				#self.image = pygame.image.load("path")
				self.x = x1
				self.y = y1

	def draw(self, surface):
				surface.blit(self.image, (self.x, self.y))

class carLeft(object):
	def __init__(self, path, x1, y1):
				self.image = pygame.image.load(path)
				#self.image = pygame.image.load("path")
				self.x = x1
				self.y = y1

	def draw(self, surface):
				surface.blit(self.image, (self.x, self.y))

class logRight(object):
		def __init__(self, x1, y1):
				self.image = pygame.image.load(artDir + "frogger_log1.png").convert()
				self.image.set_colorkey((0,0,0))
				self.image.set_colorkey((255,255,255))
				self.x = x1
				self.y = y1

		def draw(self, surface):
				surface.blit(self.image, (self.x, self.y))

class logLeft(object):
	def __init__(self, x1, y1):
				self.image = pygame.image.load(artDir + "frogger_log2.png").convert()
				self.image.set_colorkey((0,0,0))
				self.image.set_colorkey((255,255,255))
				self.x = x1
				self.y = y1

	def draw(self, surface):
				surface.blit(self.image, (self.x, self.y))

### FUNCTIONS
def drawText(surf, text, size, x, y, color):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def carCollision():
	for c in carRightList:
		if frog.x < (c.x + CAR_W) and (frog.x + FROG_W) > c.x and \
			frog.y < (c.y + CAR_H) and (frog.y + FROG_H) > c.y:
				return True

	for c in carLeftList:
		if frog.x < (c.x + CAR_W) and (frog.x + FROG_W) > c.x  and \
			frog.y < (c.y + CAR_H) and (frog.y + FROG_H) > c.y:
				return True
	return False

def logRightCollision():
	global frogOnLog
	for l in logRightList:
		if frog.x < (l.x + LOG_W) and (frog.x + FROG_W) > l.x and \
			frog.y < (l.y + LOG_H) and (frog.y + FROG_H) > l.y:
				frogOnLog = True
				return True

	return False

def logLeftCollision():
	global frogOnLog
	for l in logLeftList:
		if frog.x < (l.x + LOG_W) and (frog.x + FROG_W) > l.x and \
			frog.y < (l.y + LOG_H) and (frog.y + FROG_H) > l.y:
				frogOnLog = True
				return True

	return False


def waterCollision():
	global frogOnLog
	if frogOnLog:
		return False
	if frog.x < (water0.x + WATER_W) and (frog.x + FROG_W) > water0.x and \
		frog.y < (water0.y + WATER_H) and (frog.y + FROG_H) > water0.y:
			return True
	return False

def carMovement():
	global carRightSpeed
	global carLeftSpeed
	for i in carRightList:
			i.draw(screen)
			i.x += carRightSpeed
			if i.x >= 595:
				i.x = 0
				carRightSpeed += .0001
	for i in carLeftList:
			i.draw(screen)
			i.x -= carLeftSpeed
			if i.x <= 0:
				i.x = 595
				carLeftSpeed += .0001

def logMovement():
	global logSpeed
	for i in logRightList:
			i.draw(screen)
			i.x += logSpeed
			if i.x - 116 >= 595:
				i.x = -116
				logSpeed += .0001
	for i in logLeftList:
			i.draw(screen)
			i.x -= logSpeed
			if i.x + 116 <= 0:
				i.x = 595
				logSpeed += .0001

def frogDeath():
	global lives
	frog.image.set_alpha(0)
	frog.y = 700
	frog.x = 262
	lives -= 1
	frog.image.set_alpha(1000)


def gameOver():
	global end
	global win
	global lives
	global x_change
	global y_change
	if lives <= 0:
		x_change = 0
		y_change = 0
		frog.image.set_alpha(0)
		carRightSpeed = 1
		carLeftSpeed = 2
		logSpeed = 1
		end = True
		win = False
		return True
	end = False
	return False

def gameWin():
	global carRightSpeed
	global carLeftSpeed
	global logSpeed
	global x_change
	global y_change
	global win
	global end
	if frog.y <= 40:
		y_change = 0
		x_change = 0
		carRightSpeed += .2
		carLeftSpeed += .2
		logSpeed += .2
		win = True
		end = False
		return True
	win = False
	return False

def screenReset():
	global lives
	lives = 3
	frog.x = 262
	frog.y = 700
	frog.image.set_alpha(1000)


### CREATING SPRITES

carRightList = []
xStart = 0
yStart = 280
carRightList.append(carRight(artDir + "cars/frogger_car0(right).png", xStart, yStart))
carRightList.append(carRight(artDir + "cars/frogger_car1(right).png", xStart+70, yStart))
carRightList.append(carRight(artDir + "cars/frogger_car0(right).png", xStart+140, yStart))
carRightList.append(carRight(artDir + "cars/frogger_car1(right).png", xStart+100, yStart+35))
carRightList.append(carRight(artDir + "cars/frogger_car1(right).png", xStart+315, yStart+35))
carRightList.append(carRight(artDir + "cars/frogger_car5(right).png", xStart+560, yStart+35))
carRightList.append(carRight(artDir + "cars/frogger_car1(right).png", xStart+208, yStart+70))
carRightList.append(carRight(artDir + "cars/frogger_car5(right).png", xStart+335, yStart+105))
carRightList.append(carRight(artDir + "cars/frogger_car1(right).png", xStart+523, yStart+105))
carRightList.append(carRight(artDir + "cars/frogger_car5(right).png", xStart+75, yStart+175))
carRightList.append(carRight(artDir + "cars/frogger_car0(right).png", xStart+134, yStart+175))
carRightList.append(carRight(artDir + "cars/frogger_car0(right).png", xStart+455, yStart+175))
carRightList.append(carRight(artDir + "cars/frogger_car0(right).png", xStart+297, yStart+140))
carRightList.append(carRight(artDir + "cars/frogger_car0(right).png", xStart+335, yStart+140))
carRightList.append(carRight(artDir + "cars/frogger_car1(right).png", xStart+567, yStart+140))

carLeftList = []
xStart = 595
yStart = 525
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart, yStart))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+250, yStart))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart, yStart))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+100, yStart+35))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+315, yStart+35))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+560, yStart+35))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+208, yStart+70))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+335, yStart+140))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+567, yStart+140))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+297, yStart+140))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+335, yStart+105))
carLeftList.append(carLeft(artDir + "cars/frogger_car6(left).png", xStart+523, yStart+105))

logRightList = []
rightXStart = 0
leftXStart = 595
yStart = 70
logRightList.append(logRight(rightXStart, yStart))
logRightList.append(logRight(rightXStart+232, yStart))
logRightList.append(logRight(rightXStart+464, yStart))
logRightList.append(logRight(rightXStart+70, yStart+105))
logRightList.append(logRight(rightXStart+302, yStart+105))
logRightList.append(logRight(rightXStart+534, yStart+105))
logRightList.append(logRight(rightXStart+140, yStart+70))
logRightList.append(logRight(rightXStart+372, yStart+70))
logRightList.append(logRight(rightXStart+604, yStart+70))

logLeftList = []
leftXStart = 595
logLeftList.append(logLeft(leftXStart, yStart+35))
logLeftList.append(logLeft(leftXStart-232, yStart+35))
logLeftList.append(logLeft(leftXStart-464, yStart+35))
logLeftList.append(logLeft(rightXStart-464, yStart+140))
logLeftList.append(logLeft(leftXStart-580, yStart+140))

### CREATING SPRITES
frog = Frog(262, 700)
path0 = Path(0, 490)
path1 = Path(0, 700)
path2 = Path(0, 245)
road0 = Road(0, 490)
road1 = Road(0, 245)
water0 = Water(0, 70)

### GAME LOOP
running = True
while running:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						running = False
						sys.exit()
### FROG MOVEMENT / FRAME CHANGE
				if event.type == pygame.KEYDOWN:
						dist = 35
						if event.key == pygame.K_UP:
								y_change = -1*dist
								curFrogFrameY = 1
								curFrogFrameX = 1
								pygame.mixer.music.load(artDir + "frog_jump.mp3")
								pygame.mixer.music.play(0)
								if frog.y - FROG_H < 0:
									y_change = 0
						elif event.key == pygame.K_DOWN:
								y_change = dist
								curFrogFrameY = 1
								curFrogFrameX = 3
								pygame.mixer.music.load(artDir + "frog_jump.mp3")
								pygame.mixer.music.play(0)
								if frog.y + FROG_H > 700:
									y_change = 0
						if event.key == pygame.K_RIGHT:
								x_change = dist
								curFrogFrameY = 0
								curFrogFrameX = 1
								pygame.mixer.music.load(artDir + "frog_jump.mp3")
								pygame.mixer.music.play(0)
								if frog.x + FROG_W > 595:
									x_change = 0
						elif event.key == pygame.K_LEFT:
								x_change = -1*dist
								curFrogFrameY = 0
								curFrogFrameX = 3
								pygame.mixer.music.load(artDir + "frog_jump.mp3")
								pygame.mixer.music.play(0)
								if frog.x < 0:
									x_change = 0

				if event.type == pygame.KEYDOWN:
					if gameOver():
						if event.key == pygame.K_SPACE:
							screenReset()
					if gameWin():
						if event.key == pygame.K_SPACE:
							screenReset()

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_RIGHT:
						curFrogFrameX = 0
						x_change = 0
						frogOnLog = False
					elif event.key == pygame.K_LEFT:
						curFrogFrameX = 2
						x_change = 0
						frogOnLog = False
					if event.key == pygame.K_UP:
						curFrogFrameX = 0
						y_change = 0
						frogOnLog = False
					elif event.key == pygame.K_DOWN:
						curFrogFrameX = 2
						y_change = 0
						frogOnLog = False

				gameOver()
				gameWin()
				frog.x += x_change
				frog.y += y_change

### FROG ON LOG MOVEMENT / DEATH
		if logRightCollision():
			frog.x += logSpeed
			if frog.x > 595:
				frogDeath()
		elif logLeftCollision():
			frog.x -= logSpeed
			if frog.x + FROG_W < 0:
				frogDeath()
		if waterCollision():
			pygame.mixer.music.load(artDir + "frog_splash.mp3")
			pygame.mixer.music.play(0)
			frogDeath()
		elif carCollision():
			frogDeath()

		drawText(screen, "LIVES = " + str(lives), 30, 70, 700, red)

		if gameOver():
			drawText(screen, "GAME OVER", 50, width/2, height/2, black)
			drawText(screen, "PRESS SPACE TO PLAY AGAIN", 30, width/2, height/2+50, black)
			carRightSpeed = 1

			carLeftSpeed = 2
			logSpeed = 1

		if win:
			drawText(screen, "GOOD JOB!... ITS GOING TO GET FASTER", 30, width/2, height/2, black)
			drawText(screen, "SPACE TO CONTINUE", 15, width/2, height/2+50, black)

### DRAWING TO SCREEN
		pygame.display.update()
		screen.fill(green)
		road0.draw(screen)
		road1.draw(screen)
		path0.draw(screen)
		path1.draw(screen)
		path2.draw(screen)
		water0.draw(screen)
		carMovement()
		logMovement()
		frog.draw(screen)

		clock.tick(60)
