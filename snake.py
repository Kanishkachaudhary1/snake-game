import pygame
import random
import os
pygame.mixer.init()

pygame.init()

#colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
lightgreen = (155,204,0)
lightblue = (155,204,0)
lightgrey = (200,200,200)

screen_width = 900
screen_height = 600

#creating window
gameWindow =pygame.display.set_mode((screen_width ,screen_height))
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font=pygame.font.SysFont("none",55)

# background image
bging =pygame.image.load("c:/snake game/bg.jpg")
bging =pygame.transform.scale(bging,(screen_width,screen_height)).convert_alpha()

# game over image
gameover_img = pygame.image.load("c:/snake game/gmo.jpg")
gameover_img = pygame.transform.scale(gameover_img, (screen_width, screen_height)).convert_alpha()

# welcome page background
# welcome screen background
welcome_bg = pygame.image.load("c:/snake game/welc.jpg")  # Use your actual image path
welcome_bg = pygame.transform.scale(welcome_bg, (screen_width, screen_height)).convert_alpha()



def text_screen(text,color,x,y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x, y))

def plot_snake(gameWindow, color,snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, (x,y,snake_size,snake_size))

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,220,229))
        gameWindow.blit(welcome_bg, (0, 0))
        text_screen("Welcome to Snake!",black,400,250)
        text_screen("press space bar to play!", black, 370, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('c:/snake game/background.MP3')
                    pygame.mixer.music.play(-1)
                    gameloop()

        pygame.display.update()
        clock.tick(60)



#game loop
def gameloop ():
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # checks if hiscore file exists
    if (not os.path.exists('hiscore.txt')):
        with open('hiscore.txt', 'w') as f:
            f.write("0")

    with open("hiscore.txt","r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)
    score = 0
    init_velocity = 5
    snake_size = 10
    fps = 60
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(score))
            gameWindow.fill(white)
            gameWindow.blit(gameover_img, (0,0))
            text_screen("Game Over ! press enter to continue...",black, 100,450)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = + init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                       velocity_x = - init_velocity
                       velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y =- init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = + init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 5
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x)<6 and  abs(snake_y - food_y) < 6:
                beep_sound = pygame.mixer.Sound("c:/snake game/beep.mp3")

                score += 10
                beep_sound.play()
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snk_length += 5
                if score> int(hiscore):
                    hiscore = score

            gameWindow.fill((233,210,229))
            gameWindow.blit(bging, (0,0))
            text_screen("score:"+ str(score) +"hiscore: "+ str(hiscore), black, 5, 5)
            pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                if head in snk_list[
                    :-1] or snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                    game_over = True
                    pygame.mixer.music.stop()  # ⛔ Stop background music
                pygame.mixer.music.load('c:/snake game/explosion.MP3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('c:/snake game/explosion.MP3')
                pygame.mixer.music.play()

            #pygame.draw.rect(gameWindow, black,(snake_x,snake_y,snake_size,snake_size))
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()
welcome()