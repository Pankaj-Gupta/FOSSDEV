
import pygame
from pygame.locals import *
import sys, os
import random
from math import *      #importing math libraries for using sin, square_root, etc in the 

import MenuClass        #importinf the menu from menu class
import Levels           #importing levels from level class

                           

pygame.mixer.pre_init(44100, -16, 2, 2048)  #setup mixer to avoid sound lag
pygame.init()       #initializing pygame

pygame.mixer.music.load(os.path.join('an-turr.ogg'))    #load music which runs throughout the background
jump = pygame.mixer.Sound(os.path.join('jump.wav'))     #load sound which is played during release of fire or ball  which has sticked to Paddle
ping = pygame.mixer.Sound(os.path.join('Ping.wav'))     #load sound which is collision of Paddle and ball
click = pygame.mixer.Sound(os.path.join('Click.wav'))   #load sound which is breaking of bricks



#stadium contains all the global variable of the code
#the use of stadium is that when the game finishes we can call stadium again so that all global variables are reseted
#hence we can begin again after finishinf the game
def stadium() :
    global Screen, Surface, icon, background, baackgroundrect, mypic, background0, Menu, white, black, clock, Font, Font2, Font3, Font4, CirclesInTheAir
    global Circles, Powers, Bullets, Life, Score, stick, ballshift, fire, all_levels, pall_levels, point, all_copy, max_levels, my_maze, pmy_maze
    global time, info_text, info_text_draw_pos
    pygame.mixer.music.play(-1)

    Screen = (800,600)
    Surface = pygame.display.set_mode(Screen)
    pygame.display.set_caption("BrickGame")                       
    icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
    background = pygame.Surface(Screen)
    backgroundrect = background.get_rect()
    mypic = pygame.image.load("im4.jpg")
    background.fill((0,0,0)) 
    background.blit(mypic, (0,0))
    background0 = background.copy()
    Surface.blit(background,(0,0))
    Menu = MenuClass.Menu

    white = [255, 255, 255]
    black = [0, 0, 0]
    clock = pygame.time.Clock()

    Font = pygame.font.Font(None,12)
    Font2 = pygame.font.Font(None,18)
    Font3 = pygame.font.Font(None,32)
    Font4 = pygame.font.Font(None,48)

    CirclesInTheAir = 1
    Circles = []    

    for x in xrange(CirclesInTheAir):
        Circles.append(Circle(Screen[0]/2,Screen[1]/2))
    
    Powers = []
    Paddles = []    
    Bullets = []

    Paddles.append(Paddle(Screen[0]/2,580,10,1))
    Life = 3      
    Score = 0     
    stick = False
    ballshift = True
    fire = False

    pall_levels = Levels.pall_levels
    point = Levels.point
    all_levels = all_copy
    max_levels = len(all_levels)
    my_maze = all_levels[0]
    pmy_maze = pall_levels[0]

    time = 0.0
    info_text = Font.render("Brick Game ",True,(255,255,255))
    info_text_draw_pos = ((Screen[0]/2)-(info_text.get_width()/2),10)
#end of stadium
        




pygame.mixer.music.play(-1)  #to play background music non-stop

Screen = (800,600)      #size of screen
Surface = pygame.display.set_mode(Screen)   #makes the surface of game

pygame.display.set_caption("BrickGame")                       
#icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
background = pygame.Surface(Screen)     #game surface of background
backgroundrect = background.get_rect()  #size of background
mypic = pygame.image.load("im4.jpg")    #background image
background.fill((0,0,0))                # fill black
background = background.convert()       #for faster blitting
background.blit(mypic, (0,0))           #blitting mypic on background
background0 = background.copy()         #copy of basic background which will be used during displaying
Surface.blit(background,(0,0))          #blitting background on Surface


Menu = MenuClass.Menu       #menu class which has been imported


white = [255, 255, 255]         #tuple for white
black = [0, 0, 0]               #tuple for black
clock = pygame.time.Clock()     


#various fonts for our use
Font = pygame.font.Font(None,12)
Font2 = pygame.font.Font(None,18)
Font3 = pygame.font.Font(None,32)
Font4 = pygame.font.Font(None,48)

CirclesInTheAir = 1  #number of ball which should be atleast present on screen


class Circle:           #class defining features of ball 
    def __init__(self,x,y):
        self.x = x              #x-coordinate of centre of ball
        self.y = y              #y-coordinate of centre of ball
        angle = random.randint(150,210)           #randomizing the angle at which ball is deflecting at the start
        self.speedy = 0.7*cos(radians(angle))   #To randomize speed
        self.speedx = 0.7*sin(radians(angle))   #To randomize speed
        self.placesbeen = []    # Recording places where ball had been for stroboscopic images
        self.radius = 5
        self.add = 0            #Number of stroboscopic ball
        self.stopped = False    
        self.stoppedtime = 0
        self.ballsurface = pygame.Surface((10,10)) #surface of ball
        self.ballsurface.set_colorkey((0, 0, 0))        #making black transparent
        pygame.draw.circle(self.ballsurface, (255, 255, 0), (5,5), 5)   
        self.ballsurface = self.ballsurface.convert_alpha()     #ball
        self.ballrect = self.ballsurface.get_rect()         #getting rect of ball


Circles = []    #Declaring list to store all the balls


#class defining features of paddle
class Paddle:
    def __init__(self,x,y,size,player):
        self.rect = [x,y,100,size]
        self.player = player        


#class defining features of power ups
class PowerUps:
    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.image = pygame.Surface((30,30))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))

        #loading images according to different type of powers
        if typ == 1:
            pic = pygame.image.load("D1.jpg")
        if typ == 2:
            pic = pygame.image.load("L1.jpg")
        if typ == 3:
            pic = pygame.image.load("S1.jpg")
        if typ == 4:
            pic = pygame.image.load("F1.jpg")
        self.image.blit(pic, (0,0))
        self.image.set_colorkey((0,0,0))
        
        self.down = 1
        self.typ = typ
        self.radius = 5

        
#class defining features of Bullet which is released from Paddle
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self. image = pygame.Surface((4, 5))
        self.image.set_colorkey((0,0,0))
        pygame.draw.rect(self.image, (20, 100, 150), (0,0,4,5) )
        pygame.draw.rect(self.image, (200,0,0), (0,0,4,2)) # point
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        self.up = 1

Powers = []     #Declaring list of Powers
Paddles = []    #Declaring list to store all the paddles
Bullets = []    #Declaring list of buullets

#To show paddles on the screen
Paddles.append(Paddle(Screen[0]/2,580,10,1))

Life = 3      #To store life left
Score = 0     #To store score
stick = False   #this variable is true when sticking is enabled
ballshift = True    #for controlling the ball stuck on paddle
fire = False        #this variable is true when fire is enabled

#Appear the balls
for x in xrange(CirclesInTheAir):
    Circles.append(Circle(Paddles[0].rect[0],Paddles[0].rect[1]))


#r,b,g,y, w for blocks
#l,s,d for powers


#creating brick
def createblock(length, height, color):
    tmpblock = pygame.Surface((length, height))     #surface of brick
    tmpblock.fill(color)                            #filling color of brick
    tmpblock.convert()
    return tmpblock                     #returning the brick



#blitting the current level
def addlevel(level):
    global Surface, background, background0
    """this function read the layout of the level dictionary
           and blit it to the screen.
           recalculate and return variables like block, height etc.
           usage:
 

        """

    lines = len(level)
    columns = len(level[0])
    length = Screen[0] / columns
    height = Screen[1] / lines 
    background = background0.copy()

    redblock = createblock(length, height,(220,59,0))           #red colored brick
    greenblock = createblock(length, height, (50, 205, 40))     #green colored brick
    corseblock = createblock(length, height,(255,140,0))        #brick which breaks when hit twice
    yellowblock = createblock(length, height, (255, 215, 0))    #yellow colored brick
    hardblock = createblock(length, height, (238, 215, 233))    #white colored brick which never break  
    #stickblock = createblock(length, height, (0, 255, 255))     #red colored brick
    blueblock = createblock(length, height, (0, 191, 255))      #red colored brick

    #blitting bricks on background
    for y in range(lines):
            for x in range(columns):
                if level[y][x] == "r": # wall 
                    background.blit(redblock, (length * x, height * y))
                elif level[y][x] == "g": # wall
                    background.blit(greenblock, (length * x, height * y))
                elif level[y][x] == "b": # wall
                    background.blit(blueblock, (length * x, height * y))
                elif level[y][x] == "y": # wall
                    background.blit(yellowblock, (length * x, height * y))
                elif level[y][x] == "w":
                    background.blit(hardblock, (length * x, height * y))
                elif level[y][x] == "c": # wall
                    background.blit(corseblock, (length * x, height * y))



    Surface.blit(background0, (0,0))
    #pygame.display.flip()
    return length, height, lines, columns, background        
    
#all_levels = [startlevel, secondlevel]
all_levels = Levels.all_levels
pall_levels = Levels.pall_levels
point = Levels.point
all_copy = all_levels
max_levels = len(all_levels)
my_maze = all_levels[0]
pmy_maze = pall_levels[0]
length, height,  lines, columns, background = addlevel(my_maze)  #level according to value of my_maze


#To Display the menu
def menu():
        global Surface, black, white, clock, Menu, my_maze, pmy_maze
        titlemenu = Menu([20, 65], wordcolor=[255, 0, 0], selectedcolor=[255, 255, 0], data=['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Quit'])
        #Surface.fill(black)
        pygame.mouse.set_visible(True)
        font = pygame.font.Font(None, 32)
        Surface.blit(font.render('The controls are: Left-Right for Player', True, white, black), [0, 0])
        Surface.blit(font.render('The first to score 3 wins the game', True, white, black), [0, 32])
        pygame.display.flip()
        while not titlemenu.selected:           # Pausing till the input is recieved
                titlemenu.update(Surface, pygame.event.poll())
                clock.tick(30)
                pygame.display.flip()

        #selecting and displaying levels acoording to selected level
        if titlemenu.selected == 'Level 1':     
            my_maze = all_levels[0]
            pmy_maze = pall_levels[0]
            main()    
        elif titlemenu.selected == 'Level 2':
            my_maze = all_levels[1]
            pmy_maze = pall_levels[1]
            main()
        elif titlemenu.selected == 'Level 3':
            my_maze = all_levels[2]
            pmy_maze = pall_levels[2]
            main()
        elif titlemenu.selected == 'Level 4':
            my_maze = all_levels[3]
            pmy_maze = pall_levels[3]
            main()
        elif titlemenu.selected == 'Level 5':
            my_maze = all_levels[4]
            pmy_maze = pall_levels[4]
            main()
        elif titlemenu.selected == 'Level 6':
            my_maze = all_levels[5]
            pmy_maze = pall_levels[5]
            main()
        elif titlemenu.selected == 'Level 7':
            my_maze = all_levels[6]
            pmy_maze = pall_levels[6]
            main()
        else:
            pygame.quit()


time = 0.0      #variable in order to control the time after which fire will appear

#To define functions of keyboard keys
def GetInput(seconds):
    global stick, time
    time = time + seconds
    key = pygame.key.get_pressed()      #stores pressed key
    for event in pygame.event.get():    # Taking Keyboard Event
        if event.type == QUIT or key[K_ESCAPE]:         # If exit button clicked
            pygame.mouse.set_visible(True)              # Or Esc key pressed
            pygame.quit();                   # Exit
    if key[K_RETURN]:                                    # If SPACE pressed
            pygame.display.flip();
            Score = 0
            Life = 3
            stadium()                                   # Rebuild the surface
            menu()                                      # Calling Menu

            
    # Player Controls
    if key[K_RIGHT]:            #if right key is pressed
        Paddles[0].rect[0] += 2;        #paddles moves to right
        if stick == True and ballshift == True:     #checking if stick feature is on
                for c in Circles:
                    if c.speedx == 0 and c.speedy == 0:
                        if c.x<Screen[0]:
                                c.x += 2
                                
    if key[K_LEFT]:     #if left key is pressed
        Paddles[0].rect[0] -= 2
        if stick == True and ballshift == True:
                for c in Circles:
                    if c.speedx == 0 and c.speedy == 0:
                        if c.x>0:
                                c.x -= 2
                                
    if key[K_SPACE]:        #if space is pressed
        if fire == True and time >0.5 :
            jump.play()
            Bullets.append(Bullet(Paddles[0].rect[0],Paddles[0].rect[1]))
            time = 0
        elif stick == True:
            for c in Circles:
                if c.speedx == 0 and c.speedy == 0:
                    jump.play()
                    xdiff = c.x - Paddles[0].rect[0]
                    xdiff = xdiff*(100.0/Paddles[0].rect[2])    #to normalize xdiff if length of paddle increases
                    c.speedy = - cos(radians((xdiff*5.0/4)))
                    c.speedx =  sin(radians((xdiff*5.0/4)))


#To update stroboscopic balls and moving the AI paddle
def Update():
    for c in Circles:
        if c.add == 0:
            c.placesbeen.append([c.x,c.y])      # Storing Last positions of the ball
            c.placesbeen.reverse()
            c.placesbeen = c.placesbeen[:25]
            c.placesbeen.reverse()
            c.add = 10
        else:
            c.add -= 1
        if c.stoppedtime == 200:    # After 200ms stroboscopic balls are deleted
            Circles.remove(c)
            continue
    if len(Circles) < CirclesInTheAir:  # Ball added
       stick = False
       Circles.append(Circle(Paddles[0].rect[0],Paddles[0].rect[1]))


#To update the position of the ball          
def Move():
    for p in Powers:
        p.y = p.y + p.down
        if p.y > Screen[1]: 
                del Powers[Powers.index(p)]
    for b in Bullets:
        b.y = b.y - b.up
        if b.y < 0:
            del Bullets[Bullets.index(b)]
    k = Paddles[0]
    for c in Circles:
            c.x += c.speedx
            c.y += c.speedy    
    Update()



#To detect the collisions of the ball with wall or the paddles
def CollisionDetect():
    global Life, Score, height, lines, length, columns, my_maze, pmy_maze, x1, stick, ballshift, fire
    for c in Circles:


        
        if c.y <= 0-c.radius:                   #To detect the collision with AI paddle
            c.y = 0
            c.speedy *=-1

                        
        if c.x <=0-c.radius:                             #To detect the collision with left wall
            c.x = 0
            c.speedx *= -1
            #Click.play(0)
        if c.y >= Screen[1]+c.radius:           #To detect the collision with player paddle
            if not c.stopped:
                c.stopped = True
                c.speedx = 0
                c.speedy = 0
                del Circles[Circles.index(c)]
                if Life>0:      # Check for current scores
                        Life -= 1             # Update score
            else:
                c.stoppedtime += 1
        
        if c.x >= Screen[0]:                   #To detect the collision with right wall
            c.x = Screen[0]
            c.speedx *= -1
            #Click.play(0)                       #Play sound


        if c.speedx > 0:
            pointx = c.x
        else:
            pointx = c.x
        if c.speedy > 0:
            pointy = c.y
        else:
            pointy = c.y


        # ------- find out if probing point is inside wall
        # make sure proing point does not produce out of index error
        y1 = (int)((c.y+2*c.speedy)/height)
        y1 = max(0,y1) # be never smaller than 0
        y1 = min(y1,lines-1) # be never bigger than lines
        
        y2 = (int)(c.y/height)
        y2 = max(0,y2)
        y2 = min(y2,lines-1)
        
        x1 = (int)((c.x + 2*c.speedx)/length)
        x1 = max(0,x1) # be never smaller than 0
        x1 = min(x1,columns-1)
        
        x2 = (int)(c.x/length)
        x2 = max(0,x2)
        x2 = min(x2,columns-1)
 


        # -------------- check the type of tile where the ball is ------
        actual = all_levels.index(my_maze)
        if my_maze[y2][x1] != '.':
            if pmy_maze[y2][x1] == "d":
                Powers.append(PowerUps(c.x, c.y, 1))
            if pmy_maze[y2][x1] == 'l':
                Powers.append(PowerUps(c.x, c.y, 2))
            if pmy_maze[y2][x1] == "s":
                Powers.append(PowerUps(c.x, c.y, 3))
            if pmy_maze[y2][x1] == "f":
                Powers.append(PowerUps(c.x, c.y, 4))
            c.speedx = -c.speedx
            if my_maze[y2][x1] != "w":
                click.play()
                if my_maze[y2][x1] == 'c':
                        my_maze[y2] = my_maze[y2][0:x1]+"y" + my_maze[y2][x1+1:]
                        pmy_maze[y2] = pmy_maze[y2][0:x1]+"y" + pmy_maze[y2][x1+1:]
                else:
                        my_maze[y2]=my_maze[y2][0:x1]+"."+my_maze[y2][x1+1:]
                        Score = Score + 10
                        point[actual]=point[actual]-1
            length, height,  lines, columns,background = addlevel(my_maze)
        else:
            c.x += c.speedx
            
        if my_maze[y1][x2] != "." :
            if pmy_maze[y1][x2] == "d":
                Powers.append(PowerUps(c.x, c.y, 1))
            if pmy_maze[y1][x2] == 'l':
                 Powers.append(PowerUps(c.x, c.y, 2))
            if pmy_maze[y1][x2] == "s":
                Powers.append(PowerUps(c.x, c.y, 3))
            if pmy_maze[y1][x2] == "f":
                Powers.append(PowerUps(c.x, c.y, 4))
            c.speedy = -c.speedy
            if my_maze[y1][x2] != "w":
                click.play()
                if my_maze[y1][x2] == 'c':
                        my_maze[y1] = my_maze[y1][0:x2]+ "y" + my_maze[y1][x2+1:]
                        pmy_maze[y1] = pmy_maze[y1][0:x2]+ "y" + pmy_maze[y1][x2+1:]
                else:
                        my_maze[y1] = my_maze[y1][0:x2]+"." + my_maze[y1][x2+1:]
                        Score = Score + 10
                        point[actual]=point[actual]-1           
            length, height, lines, columns,background = addlevel(my_maze)
        else:
            c.y += c.speedy



        if point[actual]==0:
            my_maze = all_levels[(max_levels + actual+1) % max_levels]
            for c in  Circles:
                del Circles[Circles.index(c)]
            Circles.append(Circle(Paddles[0].rect[0], Paddles[0].rect[1]))
            Paddles[0].rect[2]=100
            length, height, lines, columns,background = addlevel(my_maze)



    for b in Bullets:
        xb = int(1.0*b.x/length)
        yb = int((1.0*b.y)/height)
 

        if my_maze[yb][xb] != '.':
            if pmy_maze[yb][xb] == "d":
                Powers.append(PowerUps(c.x, c.y, 1))
            if pmy_maze[yb][xb] == 'l':
                Powers.append(PowerUps(c.x, c.y, 2))
            if pmy_maze[yb][xb] == "s":
                Powers.append(PowerUps(c.x, c.y, 3))
            if pmy_maze[yb][xb] == "f":
                Powers.append(PowerUps(c.x, c.y, 4))
            if my_maze[yb][xb] != "w":
                click.play()
                if my_maze[yb][xb] == 'c':
                        my_maze[yb] = my_maze[yb][0:xb]+"y" + my_maze[yb][xb+1:]
                        pmy_maze[yb] = pmy_maze[yb][0:xb]+"y" + pmy_maze[yb][xb+1:]
                else:
                        my_maze[yb]=my_maze[yb][0:xb]+"."+my_maze[yb][xb+1:]
                        Score = Score + 10
                        point[actual]=point[actual]-1
            del Bullets[Bullets.index(b)]
            length, height,  lines, columns,background = addlevel(my_maze)
        else:
            b.y = b.y - b.up
            
        if point[actual]==0:
            my_maze = all_levels[(max_levels + actual+1) % max_levels]
            for c in  Circles:
                del Circles[Circles.index(c)]
            Circles.append(Circle(Paddles[0].rect[0], Paddles[0].rect[1]))
            Paddles[0].rect[2]=100
            length, height, lines, columns,background = addlevel(my_maze)








            
    ##This for loop checks left and right limit of paddle.
    for p in Paddles:
        if p.rect[0]-(p.rect[2]/2) < 0:
            p.rect[0] = (p.rect[2]/2)
            ballshift = False
        elif p.rect[0]+(p.rect[2]/2) > Screen[0]:
            p.rect[0] = Screen[0] - (p.rect[2]/2)
            ballshift = False
        else:
                ballshift = True


    #this loop checks collision of power with paddle
    for k in Powers:
            xdiff = k.x - p.rect[0]
            ydiff = k.y - p.rect[1]
            p = Paddles[0]
            if abs(xdiff) <= (p.rect[2]/2) + k.radius and abs(ydiff) <= (p.rect[3]/2) + k.radius:
                if k.typ == 1:
                    q = len(Circles)
                    for c in Circles:
                        if q>0:
                            Circles.append(Circle(c.x,c.y))
                            q = q - 1
                            Life = Life + 1
                    del Powers[Powers.index(k)]
                elif k.typ == 2:
                    p.rect[2] = p.rect[2] + 50
                    del Powers[Powers.index(k)]
                elif k.typ == 3:
                    stick = True
                    fire = False
                    del Powers[Powers.index(k)]
                elif k.typ == 4:
                    if stick == True:       #only one power at a time
                        jump.play()
                        for c in Circles:
                            if c.speedx == 0 and c.speedy == 0:
                                xdiff = c.x - Paddles[0].rect[0]
                                xdiff = xdiff*(100.0/Paddles[0].rect[2])    #to normalize xdiff if length of paddle increases
                                c.speedy = - cos(radians((xdiff*5.0/4)))
                                c.speedx =  sin(radians((xdiff*5.0/4)))
                    stick = False
                    fire = True
                    del Powers[Powers.index(k)]
                       


    

    #This for loop detects the collision of the ball with paddle
    for p in Paddles:
        r = PygameRectFromRect(p.rect)
        for c in Circles:
            xdiff = c.x - p.rect[0]
            ydiff = c.y - p.rect[1]

            if abs(xdiff) <= (p.rect[2]/2) + c.radius and abs(ydiff) <= (p.rect[3]/2) + c.radius: #collision
                #Ping.play(0)
                if stick == True:
                    c.speedx = 0
                    c.speedy = 0
                else:
                    ping.play()
                    if ydiff > 0:#lower
                        c.y = r[1] + r[3] + c.radius
                    if ydiff < 0:#upper
                        c.y = r[1]-r[3]-c.radius
                    xdiff = xdiff*(100.0/p.rect[2])    #to normalize xdiff if length of paddle increases
                    sp = sqrt(c.speedx*c.speedx + c.speedy*c.speedy)
                    c.speedy = -sp * cos(radians((xdiff*5.0/4)))
                    c.speedx = sp * sin(radians((xdiff*5.0/4)))

                
#To find size to Render the Rectangle 
def PygameRectFromRect(r):
    tl = (  r[0]-(r[2]/2),  (r[1]+(r[3]/2))  )
    dim = (  r[2],  r[3]  )
    r2 = (tl[0],tl[1],dim[0],dim[1])
    return r2

#To convert the point to the integer
def IntegerisePoint(point):
    returnpoint = [int(round(point[0])),int(round(point[1]))]
    return returnpoint
#To print on the stadium screen the name.
info_text = Font.render("Brick Game ",True,(255,255,255))
info_text_draw_pos = ((Screen[0]/2)-(info_text.get_width()/2),10)

#To Display the result of the match
def Result():
        global Surface, Screen, Score, Life, Font, Font2, Font3, Font4, my_maze, pmy_maze, all_levels, all_copy, length, height, columns, background, startlevel_copy
        for c in Circles:       #so that during point display it doesnt increases
                c.speedx = 0
                c.speedy = 0
        all_levels = all_copy
        my_maze = all_levels[0]
        pmy_levels = pall_levels[0]
        length, height,  lines, columns, background = addlevel(my_maze)
        #p1_score_text = Font3.render("Player, Score "+str(Life),True,(255,255,255))
        p2_score_text = Font3.render("Your Score "+str(Score),True,(255,255,255))
        p4_text = Font2.render("Press enter to return to MAIN MENU ",True,(255,0,255))
        #Surface.blit(p1_score_text,(Screen[0]/2-p1_score_text.get_width()-20,290))
        Surface.blit(p2_score_text,(Screen[0]/2-p2_score_text.get_width()-20,310))
        #Surface.blit(p3_text,(Screen[0]/2+p2_score_text.get_width()-20,300))
        Surface.blit(p4_text,(Screen[0]/2-p2_score_text.get_width()-20,360))
        pygame.display.flip()
        #Ping.set_volume(0)
        #Click.set_volume(0)
        #menu()


#To draw the balls and the paddles and update the scores  
def Draw():
    global Surface, Screen, Score, Life, Font, Font2, Font3, Font4, background
    #Surface.fill((0,0,0))
    Surface.blit(background, (0,0))
    if Life>0:
        for c in Circles:
                light = 0
                for p in c.placesbeen:
                        point = IntegerisePoint((p[0],p[1]))
                        pygame.draw.circle(Surface,(light,0,0),point,c.radius)
                        light += 2
                point = IntegerisePoint((c.x,c.y))
                Surface.blit(c.ballsurface, point)
                #pygame.draw.circle(Surface,(255,255,255),point,c.radius)

        for z in Powers:
                Surface.blit(z.image, ((int)(z.x), (int)(z.y)))
                #pygame.draw.circle(Surface, (100, 50, 0), ((int)(z.x), (int)(z.y)), 10, 2)
        p=Paddles[0]

        for b in Bullets:
            Surface.blit(b.image0, (b.x, b.y))
        r = PygameRectFromRect(p.rect)
        pygame.draw.rect(Surface,(240,120,0),(r[0],r[1],r[2],r[3]),0)
        #pygame.draw.rect(Surface,(240,120,0),(r[0],r[1],r[2],r[3]),0)
        Surface.blit(info_text,info_text_draw_pos)
        p1_score_text = Font2.render("Life "+str(Life),True,(255,255,255))
        p2_score_text = Font2.render("Score "+str(Score),True,(255,255,255))
        Surface.blit(p1_score_text,(0+20,20))
        Surface.blit(p2_score_text,(Screen[0]-p2_score_text.get_width()-20,20))
        pygame.display.flip()
        
    else:
        Result()
        
FPS = 200       
#main function determining the order of the calls made to different function        
def main():
    global my_maze
    while True:
        milliseconds = clock.tick(FPS)
        seconds = milliseconds/1000.0
        length, height,  lines, columns, background = addlevel(my_maze)
        GetInput(seconds)
        Move()
        CollisionDetect()
        Draw()

    
if __name__ == '__main__': menu()
