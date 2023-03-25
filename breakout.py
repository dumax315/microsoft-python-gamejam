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
        self.rect.topleft = 700, 100
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

            #change to game over later
            if (self.rect.bottom > self.area.bottom):  
                pygame.quit()
                
            newpos = self.rect.move(self.vx, self.vy)
            self.rect = newpos
        else:
            self.rect = newpos

    def bounce(self, side):
        # reflectedVector = velocityVector - scale(surfaceNormal, 2.0*dot(surfaceNormal, velocityVector))]\
        self.vx = self.vx - (side["x"]*self.vx + side["y"]*self.vy)*side["x"]*2
        self.vy = self.vy - (side["x"]*self.vx + side["y"]*self.vy)*side["y"]*2
        

        

class block(pygame.sprite.Sprite):
    """Paddle that moves with a and d"""

    def __init__(self, posX, posY):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("paddle.png", -1, scale=3)
        self.rect.move_ip(posX,posY)


    def collides(self, target):

        # hitbox = self.rect.inflate(-5, -5)
        return self.rect.colliderect(target.rect)
    
    def collisionNormal(self, target):
        if self.rect.left < target.rect.left or self.rect.right > target.rect.right:
            return {"x":0,"y":1}
        if self.rect.top < target.rect.top or self.rect.bottom > target.rect.bottom:
            return {"x":1,"y":0}

# class Label(pygame.sprite.Sprite):
#     def __init__(self):
#         # Call the parent class (Sprite) constructor  
#         pygame.sprite.Sprite.__init__(self)
#         self.score = 0
#         self.font = pygame.font.Font(None, 64)
#         self.textSurf = self.font.render(f"Break Out     Score = {self.score}", True, (10, 10, 10))
#         self.image = pygame.Surface((1000, 1000))
#         self.textpos = self.textSurf.get_rect(centerx=background.get_width() / 2, y=10)
#         self.image.blit(self.textSurf, self.textpos)

#         self.rect = self.textpos

# class Label1(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
#         self.score = 0
#         self.font = pygame.font.Font(None, 64)
#         self.text = self.font.render(f"Break Out     Score = {self.score}", True, (10, 10, 10))
#         self.image = pygame.Surface((width, height))
#         self.textpos = self.text.get_rect(centerx=background.get_width() / 2, y=10)
#         screen.blit(self.text, self.textpos)



#     def draw(self, screen):
#         screen.blit(self.text, self.textpos)

#     def update(self):
#         # self.surface.fill((170, 238, 187))
#         # self.textpos = self.text.get_rect(centerx=background.get_width() / 2, y=10)
#         screen.blit(self.text, self.textpos)


screen = pygame.display.set_mode((1280, 480), pygame.SCALED)
pygame.display.set_caption("Break Out")

pygame.init()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((170, 238, 187))
score = 0




screen.blit(background, (0, 0))
pygame.display.flip()



font = pygame.font.Font(None, 64)

text = font.render(f"Break Out     Score = {score}", True, (10, 10, 10))

textpos = text.get_rect(centerx=background.get_width() / 2, y=10)


paddle = paddle()
ball = ball()
blocks = (block(100,100),block(200,160),block(300,100),block(400,160))
allsprites = pygame.sprite.RenderPlain((paddle,ball))
blocksGroup = pygame.sprite.RenderPlain(blocks)

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



    for block in pygame.sprite.spritecollide(ball, blocksGroup, 1):
        if block.collides(ball):
            ball.bounce(block.collisionNormal(ball))
            block.kill()
            score += 1
            text = font.render(f"Break Out     Score = {score}", True, (10, 10, 10))

            # allsprites.remove(block)

    blocksGroup.update()
    allsprites.update()

   
    
    screen.blit(background, (0, 0))
    screen.blit(text, textpos)
    blocksGroup.draw(screen)
    allsprites.draw(screen)
    pygame.display.flip()

pygame.quit()