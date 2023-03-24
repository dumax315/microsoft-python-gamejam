# Import Modules
import os
import pygame
import math

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")



def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()



class paddle(pygame.sprite.Sprite):
    """Paddle that moves with a and d"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("paddle.png", -1, scale=2)
        self.rect.move_ip(1280/2-self.rect.width/2,400)
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        deltaX = 0

        if keys[pygame.K_a]:
            deltaX -= self.speed
        if keys[pygame.K_d]:
            deltaX += self.speed

        self.rect.move_ip(deltaX,0)

    def collides(self, target):

        # hitbox = self.rect.inflate(-5, -5)
        return self.rect.colliderect(target.rect)

class ball(pygame.sprite.Sprite):
    """A ball that bounces around the screen"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("ball.png", -1, 2)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 300, 90
        self.vx = 4
        self.vy = 4

    def update(self):
        
        self._move()

    def _move(self):
        """move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move(self.vx, self.vy)
        if not self.area.contains(newpos):
            
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.bounce({"x":1,"y":0})
            if self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                self.bounce({"x":0,"y":1})
                
            newpos = self.rect.move(self.vx, self.vy)
            self.rect = newpos
        else:
            self.rect = newpos

    def bounce(self, side):
        # reflectedVector = velocityVector - scale(surfaceNormal, 2.0*dot(surfaceNormal, velocityVector))]\
        self.vx = self.vx - (side["x"]*self.vx + side["y"]*self.vy)*side["x"]*2
        self.vy = self.vy - (side["x"]*self.vx + side["y"]*self.vy)*side["y"]*2
        print(side["y"])
        

        
        

screen = pygame.display.set_mode((1280, 480), pygame.SCALED)
pygame.display.set_caption("Break Out")

pygame.init()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((170, 238, 187))


if pygame.font:
    font = pygame.font.Font(None, 64)
    text = font.render("Break Out     Score = 0", True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(text, textpos)


screen.blit(background, (0, 0))
pygame.display.flip()


paddle = paddle()
ball = ball()
allsprites = pygame.sprite.RenderPlain((paddle,ball))
clock = pygame.time.Clock()


going = True
while going:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            going = False

    if paddle.collides(ball):
        ball.bounce({"x":0,"y":1})
    allsprites.update()
    
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()

pygame.quit()