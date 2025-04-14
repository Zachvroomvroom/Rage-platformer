import pygame
pg = pygame

class SpriteSheet():
  def __init__(self, image):
    self.sheet = image
  def get_image(self, frame,framey, width, height, scale, color):
    width_use = int(width*scale)
    height_use = int(height*scale)
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(self.sheet, (0, 0), ((frame * width), (framey*height), width, height))
    image = pygame.transform.scale(image, (width_use, height_use))
    image.set_colorkey(color)

sprite_sheet_image = pg.image.load('spritesheet.png')
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
# size = 1
for x in range(25):
    for y in range(32):
        #426X629
        # if x == 6 and y==0:
        plats.append(sprite_sheet.get_image(x, y, 17.04, 17.03,SCALE, BLACK))

        image = sprite_sheet.get_image(x, y, 17.04, 17.03,SCALE, BLACK)
        image.set_colorkey(BLACK)