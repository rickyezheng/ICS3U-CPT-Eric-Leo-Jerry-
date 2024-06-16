import pygame

#Defining a button class that can be used to detect mouse clicks
class Button():
  def __init__(self, x, y, image, single_click):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.clicked = False
    self.single_click = single_click

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