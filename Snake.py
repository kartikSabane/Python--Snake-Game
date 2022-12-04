import os
import pygame
import random

#Complusory to add 
pygame.init()

#for music 
pygame.mixer.init()

#Colors
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)

#initializing screen width and height
screen_width=900
screen_height=500

#creating window
gameWindow=pygame.display.set_mode((screen_width,screen_height))

#Background Image
bgimage=pygame.image.load("Python Project/image/Snake.JPG")
bgimage=pygame.transform.scale(bgimage,(screen_width,screen_height)).convert_alpha()
bgimage.set_alpha(150)  #Setting opacity of image

#Game over image
GameOverimage=pygame.image.load("Python Project/image/GameOver.JPG")
GameOverimage=pygame.transform.scale(GameOverimage,(screen_width,screen_height)).convert_alpha()

#Welcome image
Welcome=pygame.image.load("Python Project/image/Welcome.JPEG")
Welcome=pygame.transform.scale(Welcome,(screen_width,screen_height)).convert_alpha()

#initializing title of game
pygame.display.set_caption("Snake with Kartik")
pygame.display.update()

#Setting FPS
clock=pygame.time.Clock()

# Showing Score in screen 
font=pygame.font.SysFont(None,30)
def textScreen(text,color,x,y):
    Screen_text=font.render(text,True,color)
    gameWindow.blit(Screen_text,[x,y])

#Increasing length of snake
def Plot_Snake(gameWindow,color,Snk_list,Snake_Size):
    for x,y in Snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,Snake_Size,Snake_Size])

#Welcome Screen
def WelcomeScreen():
    exit_game=False
    while not exit_game:
        gameWindow.fill((240,220,229))
        gameWindow.blit(Welcome,(0,0))
        textScreen("Welcome to Snake Game",black,250,200)
        textScreen("Press Space Bar to continue",black,250,250)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    #Playing background music
                    pygame.mixer.music.load("Python Project/Audio/SnakeBackground.mp3")
                    pygame.mixer.music.play()
                    GameLoop()

        pygame.display.update()
        clock.tick(30)

#Game loop
def GameLoop():
    # Game specific variable 
    exit_game=False
    game_over=False
    SnakeX=50
    SnakeY=60
    Snake_Size=15
    fps=30
    VelocityX=0
    VelocityY=0
    FoodX=random.randint(20,screen_width)
    FoodY=random.randint(20,screen_height)
    FoodR=5
    Score=0
    Snk_list=[]
    Snk_length=1

    #Check if SnakeHighScore file exists
    if (not os.path.exists("SnakeHighScore.txt")):
        with open("SnakeHighScore.txt","w") as f:
            f.write("0")
        
    with open("SnakeHighScore.txt","r") as f:
        HighScore=f.read()

    while not exit_game:
        #Game over
        if game_over:
            #After Game over updating High Score
            with open("SnakeHighScore.txt","w") as f:
                f.write(str(HighScore))

            gameWindow.fill(white)
            gameWindow.blit(GameOverimage,(0,0))

            # if Score<100:
            #     textScreen("Nhi Hora Kya ! Enter to continue",red,200,200)        
            # else:
            #     textScreen("Game Over! Enter to continue",red,200,200)

            textScreen("Enter to continue",red,330,300)
            textScreen("Your Score:"+str(Score)+"  HighScore:"+str(HighScore),red,280,330)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True  

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        WelcomeScreen() 
        else:
            for event in pygame.event.get():
                # print(event)
                if event.type==pygame.QUIT:
                    exit_game=True

                #moving Snake
                if event.type==pygame.KEYDOWN:  #KEYDOWN=pressing any key  
                    #moving snake at right
                    if event.key==pygame.K_RIGHT:
                        VelocityX=10
                        VelocityY=0
                        # SnakeX=SnakeX+10

                    #Moving snake at left
                    if event.key==pygame.K_LEFT:
                        VelocityX=-10
                        VelocityY=0
                        # SnakeX=SnakeX-10

                    #moving snake at up
                    if event.key==pygame.K_UP:
                        VelocityY=-10
                        VelocityX=0
                        # SnakeY=SnakeY-10

                    #Moving snake at down
                    if event.key==pygame.K_DOWN:
                        VelocityY=10
                        VelocityX=0
                        # SnakeY=SnakeY+10
                    
                    #Cheat Code Increasing Score
                    if event.key==pygame.K_q:
                        Score+=20

            #Giving speed to snake
            SnakeX=SnakeX+VelocityX
            SnakeY=SnakeY+VelocityY

            #Printing the score 
            if abs(SnakeX-FoodX)<9 and abs(SnakeY-FoodY)<9 :
                Score=Score+10
                # print("Score is :",Score*10)

                #Generating new food
                FoodX=random.randint(20,screen_width)
                FoodY=random.randint(20,screen_height)

                Snk_length=Snk_length+3
                # print(HighScore)
                if Score>int(HighScore):
                    HighScore=Score

            gameWindow.fill(white)
            gameWindow.blit(bgimage,(0,0))
            
            textScreen("Score:"+str(Score),red,5,5)
            #Creating Head of snake
            
            head=[]
            head.append(SnakeX)
            head.append(SnakeY)
            Snk_list.append(head)

            if len(Snk_list)>Snk_length:
                del Snk_list[0]
            
            #Collision Snake
            if head in Snk_list[:-1]:
                game_over=True
                pygame.mixer.music.load("Python Project/Audio/Dumpster Door Hit.mp3")
                pygame.mixer.music.play()

            #Collision at game window
            if SnakeX<0 or SnakeX>screen_width or SnakeY<0 or SnakeY>screen_height:
                game_over=True
                pygame.mixer.music.load("Python Project/Audio/Dumpster Door Hit.mp3")
                pygame.mixer.music.play()
                # print("Game Over")

            # pygame.draw.rect(gameWindow,black,[SnakeX,SnakeY,Snake_Size,Snake_Size])
            Plot_Snake(gameWindow,black,Snk_list,Snake_Size)

            #Creating food for snake
            pygame.draw.circle(gameWindow,red,[FoodX,FoodY],FoodR)
        pygame.display.update()
        clock.tick(fps)

        
    pygame.quit()
    quit()

WelcomeScreen()
