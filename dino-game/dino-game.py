import cv2
import numpy as np
import joblib
import pygame
from sys import exit
from random import randrange, choice
import os

# Add error handling for model loading
try:
    jump_model = joblib.load('model_second_iteration.pkl')
    print("Model loaded successfully")
except FileNotFoundError:
    print("Error: jump_model.pkl not found!")
    exit()
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

msg = ''

def convert_frame_to_model(Canny_image):
    '''
    1° step = resize the image to (height=96, width=128) 
    2° step = reshape the image to (-1, img.size)
    3° step = give the image to the model
    '''
    #1° Step
    width = 128
    height = 128
    dim = (width, height)
    resized = cv2.resize(Canny_image, dim, interpolation = cv2.INTER_AREA)
    
    #2° Step
    reshaped_image = resized.reshape(-1, resized.size)
    
    #3° Step
    return jump_model.predict(reshaped_image)
    
cap = cv2.VideoCapture(0)


x = 800 #500
y = 700 #400

os.environ['SDL_VIDEO_WINDOW_POS'] = f'{(x, y)}'

#os.environ['SDL_VIDEO_CENTERED'] = '0'

THIS_FOLDER = os.getcwd()

pygame.init()
pygame.mixer.init()  # Initialize mixer explicitly

SCREEN_WIDTH = 840
SCREEN_HEIGHT = 680

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

FPS = 30
GAME_SPEED = 10
FLOOR_SPEED = 10
GAME_OVER = False

points = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

song = 0

font = pygame.font.SysFont('comicsansms', 40, True, True)

# Add error handling for score sound
try:
    score_sound = pygame.mixer.Sound(os.path.join(THIS_FOLDER,'score_sound.wav'))
    score_sound.set_volume(0.2)
except (pygame.error, FileNotFoundError) as e:
    print(f"Could not load score_sound.wav: {e}")
    score_sound = None

def create_colored_surface(width, height, color):
    """Create a colored rectangle as fallback for missing images"""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Add error handling for sounds
        try:
            self.jump_sound = pygame.mixer.Sound(os.path.join(THIS_FOLDER,'jump_sound.wav'))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load jump_sound.wav: {e}")
            self.jump_sound = None
            
        try:
            self.death_sound = pygame.mixer.Sound(os.path.join(THIS_FOLDER, 'death_sound.wav'))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load death_sound.wav: {e}")
            self.death_sound = None
        
        self.up = False
        self.stop = False
        self.xpos = 50
        self.ypos = (SCREEN_HEIGHT // 2) + 140
        
        # Try to load dino images with fallback
        self.dino_imgs = []
        for i in range(3):
            try:
                img_path = os.path.join(THIS_FOLDER, f'dinossaur{i}.png')
                self.dino_imgs.append(pygame.image.load(img_path).convert_alpha())
            except (pygame.error, FileNotFoundError):
                print(f"Could not load dinossaur{i}.png, using colored rectangle")
                self.dino_imgs.append(create_colored_surface(84, 84, GREEN))

        self.index = 0
        self.image = self.dino_imgs[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (84, 84))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = self.xpos, self.ypos
    
    def collision(self):
        global GAME_SPEED, FLOOR_SPEED
        if pygame.sprite.spritecollide(dino, obstacle_group, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(dino, flying_dino_group, False, pygame.sprite.collide_mask):
            GAME_SPEED = 0
            FLOOR_SPEED = 0
            self.stop = True
            flying_dino.stop = True
            
    def jump(self):
        if self.jump_sound:
            self.jump_sound.play()
        self.up = True
        
    def update(self):
        #JUMP CONDITION
        if self.stop == False:
            if self.up == False:
                if self.rect[1] < self.ypos:
                    self.rect[1] += 20
                else:
                    self.rect[1] = self.ypos
            if self.up == True:
                if self.rect[1] <= self.ypos - 200:
                    self.up = False
                else:
                    self.rect[1] -= 30
        
            #SPRITES
            if self.index >= len(self.dino_imgs) - 1:
                self.index = 0
            self.index += 0.25

            self.image = self.dino_imgs[int(self.index)]
            self.image = pygame.transform.scale(self.image, (128, 128))
            self.mask = pygame.mask.from_surface(self.image)

        else:
            pass

class Flying_dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        
        
        # Try to load flying dino images with fallback
        self.flying_dino_imgs = []
        for i in range(2):
            try:
                img_path = os.path.join(THIS_FOLDER, f'fly_dino{i}.png')
                self.flying_dino_imgs.append(pygame.image.load(img_path).convert_alpha())
            except (pygame.error, FileNotFoundError):
                print(f"Could not load fly_dino{i}.png, using colored rectangle")
                self.flying_dino_imgs.append(create_colored_surface(84, 84, BLUE))
        
        self.stop = False
        self.index = 0
        self.image = self.flying_dino_imgs[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        
        self.image = pygame.transform.scale(self.image, (84, 84))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = SCREEN_WIDTH, (SCREEN_HEIGHT // 2) 

    def update(self):
        #SPRITES
        if self.stop == False:
            if self.index >= len(self.flying_dino_imgs) - 1:
                self.index = 0

            self.index += 0.25
            self.image = self.flying_dino_imgs[int(self.index)]
            self.image = pygame.transform.scale(self.image, (128, 128))
            self.mask = pygame.mask.from_surface(self.image)
        else:
            pass

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Try to load obstacle image with fallback
        try:
            self.image = pygame.image.load(os.path.join(THIS_FOLDER,'obstacle0.png')).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print("Could not load obstacle0.png, using colored rectangle")
            self.image = create_colored_surface(84, 84, RED)
            
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (84, 84))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + 162
        self.mask = pygame.mask.from_surface(self.image)

class Clouds(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Try to load cloud image with fallback
        try:
            self.image = pygame.image.load(os.path.join(THIS_FOLDER,'clouds0.png')).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print("Could not load clouds0.png, using colored rectangle")
            self.image = create_colored_surface(148, 148, WHITE)
            
        self.image = pygame.transform.scale(self.image, (148, 148))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = (SCREEN_WIDTH // 2) + randrange(-400, 400, 100) , (SCREEN_HEIGHT // 2) - randrange(200, 400, 100)
    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect[0] = SCREEN_WIDTH
            self.rect[1] = (SCREEN_HEIGHT // 2) - randrange(200, 400, 100)
        self.rect[0] -= GAME_SPEED

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Try to load floor image with fallback
        try:
            self.image = pygame.image.load(os.path.join(THIS_FOLDER,'floor0.png')).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print("Could not load floor0.png, using colored rectangle")
            self.image = create_colored_surface(64, 64, BLACK)
            
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = 0 , SCREEN_HEIGHT // 2  + 200
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect[0] = SCREEN_WIDTH
        self.rect[0] -= FLOOR_SPEED

dino = Dino()
dino_group = pygame.sprite.Group()
dino_group.add(dino)

flying_dino = Flying_dino()
flying_dino_group = pygame.sprite.Group()
flying_dino_group.add(flying_dino)

obstacle = Obstacle()
obstacle_group = pygame.sprite.Group()
obstacle_group.add(obstacle)

numb_of_clouds = 5
clouds_group = pygame.sprite.Group()
for c in range(numb_of_clouds):
    clouds = Clouds()
    clouds_group.add(clouds)

floor_group = pygame.sprite.Group()
for c in range(-64, SCREEN_WIDTH, 60):
    floor = Floor()
    floor.rect[0] = c
    floor_group.add(floor)

clock = pygame.time.Clock()

obstacle_choice = choice([obstacle, flying_dino])

while True:
    sucess, img = cap.read()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(gray, 155, 105)
        
    model_prediction = convert_frame_to_model(imgCanny)
        
    if model_prediction == 0:
        msg = 'Not jumping'
    else:
        msg = 'Jumping'
            
    cv2.putText(imgCanny, f'{msg}', (480//2, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3) #msg, origin, font, scale_font, color, thickness
    cv2.imshow('Canny', imgCanny)
                
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                exit()
                '''
                if event.key == pygame.K_SPACE:
                    if dino.rect[1] < dino.ypos:
                        pass
                    else:
                        dino.jump()
                '''
            if event.key == pygame.K_r and GAME_OVER == True:
                GAME_SPEED = 10
                FLOOR_SPEED = 10
                points = 0
                song = 0
                obstacle.rect[0] = SCREEN_WIDTH
                flying_dino.rect[0] = SCREEN_WIDTH
                dino.stop = False
                dino.rect[1] = dino.ypos
                flying_dino.stop = False

    dino_group.draw(screen)
    dino_group.update()
    dino.collision()

    flying_dino_group.draw(screen)
    flying_dino_group.update()

    obstacle_group.draw(screen)
    obstacle_group.update()

    clouds_group.draw(screen)
    clouds_group.update()

    floor_group.draw(screen)
    floor_group.update()

    text = font.render(f'{points}', True, BLACK)
    screen.blit(text, (700, 40))
    
    if model_prediction == 1:
        if dino.rect[1] < dino.ypos:
            pass
        else:
            dino.jump()

    if obstacle_choice.rect.topright[0] < 0:
        flying_dino.rect[0] = SCREEN_WIDTH
        obstacle.rect[0] = SCREEN_WIDTH
        obstacle_choice = choice([obstacle, flying_dino])
    else:
        obstacle_choice.rect[0] -= GAME_SPEED

    if GAME_SPEED != 0:
        points += 1
        if (points % 100) == 0:
            if score_sound:
                score_sound.play()
            if GAME_SPEED == 46:
                pass
            else:
                GAME_SPEED += 2
    else:
        points += 0
        if song > 1:
            song = 2
        else:
            song += 1
        if dino.jump_sound:
            dino.jump_sound.stop()
        txt = ['GAME OVER', 'Press R to play again']
        line1 = font.render(txt[0], True, BLACK)
        line2 = font.render(txt[1], True, BLACK)
        screen.blit(line1, ((SCREEN_WIDTH // 2) - (line1.get_width()//2), (SCREEN_HEIGHT // 2) - 100))
        screen.blit(line2, ((SCREEN_WIDTH // 2) - (line2.get_width()//2), (SCREEN_HEIGHT // 2) - 50))
        GAME_OVER = True

    if song == 1:
        if dino.death_sound:
            dino.death_sound.play()

    pygame.display.flip()

#Release everything if job is finished
cap.release()
cv2.destroyAllWindows()