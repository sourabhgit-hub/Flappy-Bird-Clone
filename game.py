import pygame
import random
from sys import exit
pygame.init()

# GAME constants and initialisation
FPS=32
WIDTH=288
HEIGHT=511
SCREEN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
SPEED=5
GRAVITY=2
SCORE=0

# Font constants
textfont=pygame.font.SysFont('gabriola',40)
scoreFont=pygame.font.SysFont('gabriola',30)

# Sounds
die_sound=pygame.mixer.Sound('gallery/audio/die.wav')
point_sound=pygame.mixer.Sound('gallery/audio/point.wav')
fly_sound=pygame.mixer.Sound('gallery/audio/fly.wav')


# BACKGROUND and BASE constants
BACKGROUND=pygame.image.load('gallery/sprites/background.png').convert_alpha()
BASE=pygame.image.load('gallery/sprites/base.png').convert_alpha()
base_x=0
base_y=HEIGHT-BASE.get_height()+20

# BIRD constants
BIRD=pygame.image.load('gallery/sprites/bird.png').convert_alpha()
bird_x=WIDTH/4
bird_y=HEIGHT/2
print(BIRD.get_height())
print(BIRD.get_width())

# PIPE constants
PIPE=pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
GAP=PIPE.get_height()+HEIGHT/5
pipe_x=WIDTH+300
pipe_y=int((HEIGHT/3)-PIPE.get_height())

# Birds Flies 
def jump():
    global GRAVITY
    GRAVITY=-10

# Gives random pipe_y
def get_pipe():
    global pipe_y
    seed=[-30,-60,-90,-120,-150,-180,-210]
    pipe_y=int(random.choice(seed))

# Restarts Game with default values
def restart():
    global GRAVITY, SPEED, SCORE, base_x, bird_y, pipe_x, pipe_y
    SPEED=5
    GRAVITY=1
    SCORE=0
    base_x=0
    bird_y=HEIGHT/2
    pipe_x=WIDTH+500
    pipe_y=(HEIGHT/3)-PIPE.get_height()
    main()

# Blits Game Over Screen
def game_over():
    global SCORE
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
        SCREEN.fill("darkkhaki")
        gameOver=textfont.render('~ Game Over  ~',False,'Mediumblue')
        SCREEN.blit(gameOver,((WIDTH/2-gameOver.get_width()/2),30))
        pressR=textfont.render('Press R to restart',False,'Mediumblue')
        SCREEN.blit(pressR,((WIDTH/2-pressR.get_width()/2),70))
        pressQ=textfont.render('Press Q to Quit',False,'Mediumblue')
        SCREEN.blit(pressQ,((WIDTH/2-pressQ.get_width()/2),110))
        
        scoreToShow="High Score: "+str(get_Highscore())
        scoreText=textfont.render(scoreToShow,False,'Mediumblue')
        SCREEN.blit(scoreText,((WIDTH-scoreText.get_width())/2,HEIGHT/2))
        scoreToShow="Score: "+str(SCORE)
        scoreText=textfont.render(scoreToShow,False,'Mediumblue')
        SCREEN.blit(scoreText,((WIDTH-scoreText.get_width())/2,HEIGHT/2+40))
        
        key=pygame.key.get_pressed()
        if key[pygame.K_q]:
            exit()
        if key[pygame.K_r] or key[pygame.K_SPACE]:
            restart()
        pygame.display.update()

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
    scoreText=scoreFont.render(scoreToShow,False,'Mediumblue')
    SCREEN.blit(scoreText,((WIDTH-scoreText.get_width())/2,(base_y+HEIGHT)/2))


# -------- MAIN PROGRAM ----------
def main():
    global GRAVITY, SCORE, base_x, bird_y, pipe_x
    birdAngle=0
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()

            # Jump bird by pressing UP key
            key=pygame.key.get_pressed()
            if key[pygame.K_UP] or key[pygame.K_SPACE]:
                fly_sound.play()
                jump()

        # Blit Backgroud and Bird and add gravity to it
        SCREEN.blit(BACKGROUND,(0,0))
        SCREEN.blit(pygame.transform.rotate(BIRD,birdAngle),(bird_x,bird_y))
        GRAVITY+=1
        bird_y+=GRAVITY

        # Rise the bird when it flies and Sink it when it drops
        if GRAVITY<2:
            if(birdAngle<30):
                birdAngle+=10
        elif birdAngle> -90:
            birdAngle-=5 


        # Blit two pipes on one another with some GAP in between and start moving them to left in continuous cycle
        SCREEN.blit(pygame.transform.rotate(PIPE,180),(pipe_x,pipe_y))
        SCREEN.blit(PIPE,(pipe_x,pipe_y+GAP))
        pipe_x-=5
        if(pipe_x==-PIPE.get_width()):
            pipe_x=WIDTH
            get_pipe()

        # Increase score when bird crosses a pipe
        if pipe_x+5>bird_x and pipe_x<bird_x:
            SCORE+=1 
            point_sound.play()

        # Blit BaseGround and move it backward continuosly in loop
        SCREEN.blit(BASE,(base_x,base_y))
        base_x-=5
        if (base_x+BASE.get_width())<WIDTH:
            base_x=0

        # prints score on bottom of the screen
        print_score()

        # If bird touches the ground or touches any of the pipe, game is over
        if bird_y>=base_y or (bird_x+BIRD.get_width()> pipe_x and bird_x<pipe_x+PIPE.get_width()) and (bird_y<pipe_y+PIPE.get_height() or bird_y+BIRD.get_height()>pipe_y+GAP):
            die_sound.play()         
            game_over()


        pygame.display.update() 
        pygame.time.Clock().tick(FPS)

if __name__=="__main__":
    main()
        