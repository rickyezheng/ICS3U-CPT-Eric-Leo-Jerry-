import pygame

#Defining a button class that can be used to detect mouse clicks
#1. __init__ initializes when you create a new instance of Button 
#2 function defines x,y(coordinates that determine where it will be placed), image represents the button, single_click only allows for a single click
#self.click initializes a flag to track whether it has been clicked
#self.rect.topleft sets the coordinates
#self.rect creates a pygame.rect
class Button():
  def __init__(self, x, y, image, single_click):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.clicked = False
    self.single_click = single_click

#1 function draws the button on specificed surface
#2 pygame.mouse.get_pos() gets the current position- built in function
#3 self.rect.collidepoint checks if its within the button
#pygame. get_pressed()[] checks if its being pressed
  def draw(self, surface):
    action = False
    # Get mouse position
    position = pygame.mouse.get_pos()

    # Check mouseover and clicked conditions
    if self.rect.collidepoint(position):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        action = True
        # If button is a single click type, then set clicked to True
        if self.single_click:
          self.clicked = True

    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False

    # Draw button on screen
    surface.blit(self.image, self.rect)

    return action
  
  #from ChatGPT modified, created a class for interactive buttons