import pygame
import random
from sys import exit
pygame.init()

# GAME constants and initialisation
FPS=32
WIDTH=288
HEIGHT=511
SPEED=5
GRAVITY=2
SCORE=0
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Font constants
text_font=pygame.font.SysFont('gabriola',40)
score_font=pygame.font.SysFont('gabriola',30)

# Sounds
die_sound=pygame.mixer.Sound('gallery/audio/die.wav')
point_sound=pygame.mixer.Sound('gallery/audio/point.wav')
fly_sound=pygame.mixer.Sound('gallery/audio/fly.wav')

# BACKGROUND and BASE constants
BACKGROUND=pygame.image.load('gallery/sprites/background.png').convert_alpha()
BASE=pygame.image.load('gallery/sprites/base.png').convert_alpha()
BASE_x=0
BASE_y=HEIGHT-BASE.get_height()+20

# BIRD constants
BIRD=pygame.image.load('gallery/sprites/bird.png').convert_alpha()
BIRD_x=WIDTH/4
BIRD_y=HEIGHT/3
BIRD_angle=0

# PIPE constants
PIPE=pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
GAP=PIPE.get_height()+HEIGHT/5
PIPE_x=WIDTH+300
PIPE_y=int((HEIGHT/3)-PIPE.get_height())

# Blits Game Over Screen
def game_over():
    global SCORE
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
        SCREEN.fill("darkkhaki")
        gameOver=text_font.render('~ Game Over  ~',False,'Mediumblue')
        SCREEN.blit(gameOver,((WIDTH/2-gameOver.get_width()/2),30))
        pressR=text_font.render('Press R to restart',False,'Mediumblue')
        SCREEN.blit(pressR,((WIDTH/2-pressR.get_width()/2),70))
        pressQ=text_font.render('Press Q to Quit',False,'Mediumblue')
        SCREEN.blit(pressQ,((WIDTH/2-pressQ.get_width()/2),110))
        
        scoreToShow="High Score: "+str(get_Highscore())
        scoreText=text_font.render(scoreToShow,False,'Mediumblue')
        SCREEN.blit(scoreText,((WIDTH-scoreText.get_width())/2,HEIGHT/2))
        scoreToShow="Score: "+str(SCORE)
        scoreText=text_font.render(scoreToShow,False,'Mediumblue')
        SCREEN.blit(scoreText,((WIDTH-scoreText.get_width())/2,HEIGHT/2+40))
         
        key=pygame.key.get_pressed()
        if key[pygame.K_q]:
            exit()
        if key[pygame.K_r] or key[pygame.K_SPACE]:
            restart()
        
        pygame.time.Clock().tick(10)    # to refresh slower when gameover screen is shown
        pygame.display.update()

# Restarts Game with default values
def restart():
    global GRAVITY, SPEED, SCORE, BASE_x, BIRD_y, PIPE_x, PIPE_y, BIRD_angle
    SPEED=5
    GRAVITY=1
    SCORE=0
    BASE_x=0
    BIRD_y=HEIGHT/3
    BIRD_angle=0
    PIPE_x=WIDTH+500
    PIPE_y=(HEIGHT/3)-PIPE.get_height()
    main()

# Birds Flies 
def jump():
    global GRAVITY
    GRAVITY=-10

# Gives random PIPE_y
def get_pipe():
    global PIPE_y
    seed=[-30,-60,-90,-120,-150,-180,-210]
    PIPE_y=int(random.choice(seed))

# Pauses the screen
def pause_screen():
    while(True):
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.time.Clock().tick(10)

# Returns the current highscore
def get_Highscore():
    global SCORE
    try:
        with open('highscore.txt','r') as f:
            highscore=int(f.read())
            if SCORE>highscore:
                with open('highscore.txt','w') as f1:
                    f1.write(str(SCORE))
                return SCORE
            else:
                with open('highscore.txt','r') as f1:
                    return f1.read()
    except FileNotFoundError:
        with open('highscore.txt','w') as f:
            f.write(str(0))
            return 0

# Prints Score at bottom of the screen during game
def print_score(): 
    scoreToShow="High Score: "+str(get_Highscore())+"   Score: "+str(SCORE)
    scoreText=score_font.render(scoreToShow,False,'Mediumblue')
    SCREEN.blit(scoreText,((WIDTH-scoreText.get_width())/2,(BASE_y+HEIGHT)/2))


# -------- MAIN PROGRAM ----------
def main():
    global GRAVITY, SCORE, BASE_x, BIRD_y, PIPE_x, BIRD_angle
    pause=True      # game is by default paused
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()

            # Jump bird by pressing UP key
            key=pygame.key.get_pressed()
            if key[pygame.K_UP] or key[pygame.K_SPACE]:
                fly_sound.play()
                jump()
            
            # Game pauses when P is pressed
            if(key[pygame.K_p]):
                pause=True

        # Blit Backgroud, Bird,2 Pipes, Baseground, Score
        SCREEN.blit(BACKGROUND,(0,0))
        SCREEN.blit(pygame.transform.rotate(BIRD,BIRD_angle),(BIRD_x,BIRD_y))
        SCREEN.blit(pygame.transform.rotate(PIPE,180),(PIPE_x,PIPE_y))
        SCREEN.blit(PIPE,(PIPE_x,PIPE_y+GAP))
        SCREEN.blit(BASE,(BASE_x,BASE_y))
        print_score()
        
        # Pause screen
        if(pause==True):
            pause_screen()
            pause=False

        # Add gravity to bird and change it's angle
        GRAVITY+=1
        BIRD_y+=GRAVITY
        if GRAVITY<2:   # Sink it downward
            if(BIRD_angle<30):
                BIRD_angle+=10
        elif BIRD_angle> -90:   # Raise it upward
            BIRD_angle-=5 

        # Moving Pipes and Baseground from right to left in a loop
        PIPE_x-=5
        if(PIPE_x==-PIPE.get_width()):
            PIPE_x=WIDTH
            get_pipe()
        BASE_x-=5
        if (BASE_x+BASE.get_width())<WIDTH:
            BASE_x=0

        # Increase score when bird crosses a pipe
        if PIPE_x+5>BIRD_x and PIPE_x<BIRD_x:
            SCORE+=1 
            point_sound.play()

        # If bird touches the ground or touches any of the pipe, game is over
        if BIRD_y>=BASE_y or (BIRD_x+BIRD.get_width()> PIPE_x and BIRD_x<PIPE_x+PIPE.get_width()) and (BIRD_y<PIPE_y+PIPE.get_height() or BIRD_y+BIRD.get_height()>PIPE_y+GAP):
            die_sound.play()         
            game_over()

        pygame.display.update() 
        pygame.time.Clock().tick(FPS)

if __name__=="__main__":
    main()
    
