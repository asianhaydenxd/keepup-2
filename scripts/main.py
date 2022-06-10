import pygame, sprites as sprites, random, colorsys

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KeepUp 2")

scene = "main_menu"
current_time = 0
event_time = 0

score = 0

hit1 = pygame.mixer.Sound("sounds/hit1.wav")
hit2 = pygame.mixer.Sound("sounds/hit2.wav")
beep = pygame.mixer.Sound("sounds/beep.wav")

# Sprite initializations
BALL = sprites.Ball()
BALL.rect.center = (WIDTH/2, HEIGHT/2)

PADDLE = sprites.Paddle()
PADDLE.rect.center = (WIDTH/2, 450)

def write(text, font_name, font_size, position):
    font = pygame.font.SysFont(font_name, font_size)
    render = font.render(text, True, (0, 0, 0))
    render_rect = render.get_rect(center = position)
    wn.blit(render, render_rect)

# Run every frame
def draw_game():
    global scene
    global score
    global bg_color
    
    PADDLE.draw(wn)
    
    # Allow mouse to control the paddle
    mouse_x = pygame.mouse.get_pos()[0]
    PADDLE.aim(mouse_x)
    
    if current_time - event_time > 3000:
        BALL.draw(wn)
        
        BALL.update_velocity()
        
        write(f"{score}", "Consolas", 20, (WIDTH/2, 20))
        
        # Bounce when the ball hits the wall
        if BALL.rect.right > WIDTH or BALL.rect.left < 0:
            BALL.bounce_wall()
            hit2.play()
        
        # Paddle keeps the ball up
        if BALL.rect.colliderect(PADDLE.rect):
            BALL.bounce_paddle(BALL.xcor() - PADDLE.xcor())
            score += 1
            bg_color = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(random.random(), 0.9, 0.9))
            hit1.play()
        
        if BALL.rect.top > HEIGHT:
            beep.play()
            scene = "done"
            
            BALL.rect.center = (WIDTH/2, HEIGHT/2)
            BALL.x_velocity = 0
            BALL.y_velocity = 0
            bg_color = (255, 255, 255)
        
        return
    
    if current_time - event_time > 2000:
        write("1", "Consolas", 20, wn.get_rect().center)
    elif current_time - event_time > 1000:
        write("2", "Consolas", 20, wn.get_rect().center)
    else:
        write("3", "Consolas", 20, wn.get_rect().center)

def draw_done():
    write("Game Over", "Consolas", 100, (WIDTH/2, HEIGHT/2))
    write(f"SCORE: {score}", "Consolas", 40, (WIDTH/2, HEIGHT/2 + 65))
    write(f"CLICK TO GO BACK TO MENU", "Consolas", 15, (WIDTH/2, HEIGHT/2 + 100))

def draw_menu():
    write("KeepUp 2", "Consolas", 150, (WIDTH/2, HEIGHT/2))
    write("CLICK ANYWHERE TO START", "Consolas", 40, (WIDTH/2, HEIGHT/2 + 100))
    write("BY HAYDEN TAYLOR", "Consolas", 15, (WIDTH/2, HEIGHT/2 + 160))

if __name__ == "__main__":
    FPS = pygame.time.Clock()
    bg_color = (255, 255, 255)
    while True:
        FPS.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if scene == "main_menu":
                    beep.play()
                    scene = "game"
                    score = 0
                    event_time = pygame.time.get_ticks()
                if scene == "done":
                    beep.play()
                    scene = "main_menu"
        
        current_time = pygame.time.get_ticks()
        
        wn.fill(bg_color)
        
        if scene == "main_menu":
            draw_menu()
        
        if scene == "game":
            draw_game()
        
        if scene == "done":
            draw_done()
        
        pygame.display.update()