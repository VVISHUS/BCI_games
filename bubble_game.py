import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Shooter")

# Define colors
WHITE = (255,255,255)
BLACK = (0, 0, 0)

# Bubble parameters
BUBBLE_RADIUS = 30
BUBBLE_SPEED = 0.3
B=1
# Cannon parameters
CANNON_WIDTH = 50
CANNON_HEIGHT = 10

# Path to the folder containing images
IMAGE_FOLDER = "images"

# Load cannon images
BASE_IMAGE = pygame.image.load(os.path.join("images", "cannon_base.png")).convert_alpha()
GUN_IMAGE = pygame.image.load(os.path.join("images", "cannon_gun_up.png")).convert_alpha()

def get_bullet(i):
    COLORED_BALL_IMAGE = pygame.image.load(os.path.join("images", f"bubble{i}.png")).convert_alpha()
    # Resize colored ball image to match bubble size
    COLORED_BALL_IMAGE = pygame.transform.scale(COLORED_BALL_IMAGE, (BUBBLE_RADIUS * 2, BUBBLE_RADIUS * 2))
    return COLORED_BALL_IMAGE

# Define Bubble class
class Bubble:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

# Define Cannon class
class Cannon:
    global B
    B= random.randint(1,9)
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 3
        self.angle = 0
        self.ball_image = get_bullet(B)

    def draw(self):
        # Draw cannon base
        screen.blit(BASE_IMAGE, (self.x - BASE_IMAGE.get_width() // 2, self.y - BASE_IMAGE.get_height()))

        # Rotate gun image
        m_x,m_y=pygame.mouse.get_pos()
        radians = math.atan2(m_y - self.y, m_x - self.x)
        degrees = math.degrees(radians) + 90
        rotated_gun = pygame.transform.rotate(GUN_IMAGE,-degrees)
        rotated_gun_rect = rotated_gun.get_rect(center=(self.x, self.y-35))

        # Draw rotated gun
        screen.blit(rotated_gun, rotated_gun_rect)

        # Draw colored ball at cannon's mouth
        #rotated_ball = pygame.transform.rotate(COLORED_BALL_IMAGE,-degrees)
        #rotated_ball_rect = rotated_ball.get_rect(center=(self.x, self.y - 120))
        ball_rect = self.ball_image.get_rect(center=(self.x, self.y - 35))
        screen.blit(self.ball_image, ball_rect)

    def rotate(self, mouse_pos):
        # Calculate angle of rotation
        self.angle = math.atan2(self.y - mouse_pos[1], mouse_pos[0] - self.x)

    def shoot(self):
        global B
        bull= Bullet(self.x,self.y - 65, self.angle, get_bullet(B))
        B=random.randint(1,9)
        self.ball_image = get_bullet(B)
        return bull
    

# Define Bullet class
class Bullet:
    def __init__(self, x, y, angle, image):
        self.x = x
        self.y = y
        self.angle = angle
        self.image = image
        self.dx = BUBBLE_SPEED * math.cos(angle)
        self.dy = -BUBBLE_SPEED * math.sin(angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

# Function to generate random image from the images folder
def random_image():
    num = random.randint(1, 9)
    image_path = os.path.join("images", f"bubble{num}.png")
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, (BUBBLE_RADIUS * 2, BUBBLE_RADIUS * 2))

# Function to generate bubbles
def generate_bubbles():
    bubbles = []
    for row in range(6):
        for col in range(10):
            bubble_image = random_image()
            bubble = Bubble(50 + col * 70 + (row % 2) * 35, 50 + row * 40, bubble_image)
            bubbles.append(bubble)
    return bubbles

# Function to check if two bubble images are the same
def same_image(image1, image2):
    return pygame.image.tostring(image1, "RGBA") == pygame.image.tostring(image2, "RGBA")

file="max_score_file.txt"
def display_winning(moves,minscore):
    font = [pygame.font.Font(None, 100-i) for i in range(10)]
    font.extend([pygame.font.Font(None, 100-i) for i in range(10,0,-1)])
    font2 = [pygame.font.Font(None, 85-i) for i in range(10)]
    font2.extend([pygame.font.Font(None, 85-i) for i in range(10,0,-1)])
    text_surface=list()
    test2=list()
    for i in range(20):
        text_surface.append(font[i].render(f' Moves : {moves}', True, (0,0,0)))
        test2.append(font2[i].render(f' MINIMUM MOVES YET : {minscore}', True, (0,0,0)))
    screen.blit(text_surface[i//45], (200, 30))   
    screen.blit(test2[i//45], (20,130))   

# Main game loop
def main():
    cannon = Cannon()
    bubbles = generate_bubbles()
    bullets = []
    moves=0
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                cannon.rotate(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    moves+=1
                    bullets.append(cannon.shoot())
        
        if(len(bubbles)==0):
            try:
                with open(file,'r') as f:
                    minscore=int(f.read())
            except FileNotFoundError:
                minscore=100000000   
                    
            with open(file,'w') as f:
                minscore=min(minscore,moves)
                f.write(f"{minscore}")    
                
            display_winning(moves,minscore)   
            #continue
            
        # Update and draw bullets
        for bullet in bullets:
            bullet.update()
            bullet.draw()

        # Draw cannon
        cannon.draw()
        
        # Check collision between bullets and bubbles
        for bullet in bullets:
            for bubble in bubbles:
                if bullet.rect.colliderect(bubble.rect):
                    if same_image(bullet.image, bubble.image):
                        bubbles.remove(bubble)
                        adjacent_bubbles = [b for b in bubbles if (abs(b.x - bullet.x) <= (BUBBLE_RADIUS+5) and abs(b.y - bullet.y) <= (BUBBLE_RADIUS+5)) or (abs(b.x - bubble.x) <= (BUBBLE_RADIUS+10) and abs(b.y - bubble.y) <= (BUBBLE_RADIUS+5)) ]
                        for adjacent_bubble in adjacent_bubbles:
                             if same_image(adjacent_bubble.image, bullet.image):
                               bubbles.remove(adjacent_bubble)
                    else:
                        bub= Bubble(bullet.x,bullet.y,bullet.image)
                        bubbles.append(bub)
                        
                    try:    
                        bullets.remove(bullet)   
                    except ValueError:
                        bullets.append(bullet)
                        continue     
    
                        
        #print(len(bubbles))                       
        # Draw bubbles
        for bubble in bubbles:
            bubble.draw()
    
            
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
