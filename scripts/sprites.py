import pygame

# Create Ball sprite
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        BALL_IMG = pygame.image.load("images/ball.png")
        self.image = pygame.transform.scale(BALL_IMG, (20, 20))
        self.rect = self.image.get_rect()
        
        self.x_velocity = 0
        self.y_velocity = 0
        self.gravity = 0.5
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def xcor(self):
        return self.rect.center[0]
    
    def ycor(self):
        return self.rect.center[1]
    
    # For the ball to be affected by gravity and physics
    def update_velocity(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        self.y_velocity += self.gravity
    
    # Bounce off the wall instead of continuing to go off-screen
    def bounce_wall(self):
        self.x_velocity *= -1.01
    
    # Bounce off the paddle when hit based on where the ball hit the paddle
    def bounce_paddle(self, accuracy):
        self.y_velocity = -18
        self.x_velocity += accuracy / 4

# Create Paddle sprite
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def xcor(self):
        return self.rect.center[0]
    
    def ycor(self):
        return self.rect.center[1]
    
    # Reposition the paddle to be aimed where the mouse is along the X axis
    def aim(self, x):
        self.rect.center = (x, 450)