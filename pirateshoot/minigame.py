from tkinter import *
import turtle
import random
import time
import sys
import math
from turtle import Turtle, Screen, Shape

#Customisable Variables
high_quality_mode = True

#Speed Variables
pSpeed = 40
pRate = 0.5
bSpeed = 60
eSpeed = 30
mSpeed = 0.25
bounceSpeed = 5
bouncePeak = 3

#Delta time chicanery variables
d1 = time.time()
d2 = time.time()
d3 = time.time()
d4 = time.time()
d5 = time.time()
d6 = time.time()
d7 = time.time()
d8 = time.time()
d9 = time.time()
d10 = time.time()
d11 = time.time()
d12 = time.time()

#Map/game variables
delay = 0.0000001
next_map = 5
difficulty = 0
pcorx = 0
pcory = 0
nxtInit = False
canEnd = False
rndStart = False
glblLoading = False
enem_pos = []
rstMode = False

#Common variables
screendim = [600, 300]

gui = Tk()
gui.resizable(False, False)
gui.geometry(f'{screendim[0]}x{screendim[1]}')
gui.title('Pirate Shoot Shoot')
cnv = Canvas(gui,width=screendim[0],height=screendim[1])
cnv.pack()
wn = turtle.TurtleScreen(cnv)
#Images
if high_quality_mode:
    print('preloading textures')
    imgp = 'assets//static//plr.gif'
    plrimg = PhotoImage(file=imgp).subsample(20,20)
    wn.addshape('playerball', Shape("image",plrimg))
    imgb = ''
    for i in range(16):
        imgb = 'assets//static//bullet//' + str(i+1)+'.png'
        bltimg = PhotoImage(file=imgb).subsample(30,30)
        wn.addshape('bullet'+str(i+1),Shape("image",bltimg))
main = turtle.RawTurtle(wn)
bulet = turtle.RawTurtle(wn)
pen = turtle.RawTurtle(wn)
door_pen = turtle.RawTurtle(wn)
choice_pen = turtle.RawTurtle(wn)
door = turtle.RawTurtle(wn)
end_pen = turtle.RawTurtle(wn)
btns = []
mainshd = turtle.RawTurtle(wn)
character_angle = 0

current_hp = 100 # Starter health for the player
loop_trigger = True # Allows the main game loop to run
door_close = True
door_message_displayed = False

main.hideturtle()
bulet.hideturtle()
pen.hideturtle()
door_pen.hideturtle()
choice_pen.hideturtle()
door.penup()
end_pen.hideturtle()
mainshd.hideturtle()

#Game map variables
curOcean = 0
oceandir = 'assets//dynamic//oceangif//'
oceans = [oceandir+'f0.gif',oceandir+'f1.gif',oceandir+'f2.gif',oceandir+'f3.gif',oceandir+'f4.gif',]

melee_enemies = [] # Sets the enemy count to zero
bulet_count = []

def load_map():# The map loading function
    global current_hp, mainshd,melee_enemies,next_map
    for enemy in melee_enemies:
        enemy.hideturtle()
    door_pen.clear()
    end_pen.clear()
    choice_pen.clear()
    mainshd.shape('circle')
    mainshd.color('light grey')
    mainshd.penup()
    mainshd.goto(0,-30)
    mainshd.showturtle()
    main.speed(0) # Makes the main player
    if high_quality_mode: main.shape('playerball')
    else:
        main.shape('circle')
        main.color('black')
    main.penup()
    main.goto(0,25)
    main.showturtle()
    main.direction = "stop"
    pen.showturtle()
    pen.speed(0) # Sets the pen that displays the player's health
    pen.clear()
    pen.shape("square")
    pen.penup()
    pen.hideturtle()
    pen.goto(0,-screendim[1]/2)
    pen.write("Health: 100", align="center", font=("Courier", 24, "normal"))
    door.showturtle()
    door.speed(0) # Makes the door to enter the next room
    door.color('brown')
    door.penup()
    door.goto(0,297)
    door.setheading(0)
    door.pendown()
    door.begin_fill()
    door.forward(40)
    door.right(90)
    door.forward(10)
    door.right(90)
    door.forward(80)
    door.right(90)
    door.forward(10)
    door.right(90)
    door.forward(40)
    door.end_fill()
    door.penup()
    door.shape('square')
    door.goto(0,screendim[1]/2)
    current_hp = 100

#Classes (wow so cool)
        
#We made a class for key presses to clean up the spaghetti code
#This code is heavily referenced from AI generated code but remains
#Solely written and applied by us :)
class KeyTracker:
    def __init__(self, gui):
        self.gui = gui
        self.keys = set()
        # Bind key press and release events
        gui.bind("<KeyPress>", self.key_press)
        gui.bind("<KeyRelease>", self.key_release)
    def key_press(self, event):
        self.keys.add(event.keysym.lower())
    def key_release(self, event):
        self.keys.discard(event.keysym.lower())
    def isPressed(self,keyPressed):
        if keyPressed in self.keys:
            return True
        else: return False
#Create a "button" class
class turtleButton:
    def __init__(self,x,y,color,width,height,shape='square'):
        global screendim
        self.button = turtle.RawTurtle(wn)
        self.fnction = {}
        self.fnction['function'] = None
        self.active = True
        self.button.color(color)
        self.button.shape(shape)
        self.button.shapesize(height,width,1)
        self.button.penup()
        self.button.goto(x,y)
        x += screendim[0]/2
        y = screendim[1]/2 - y
        self.minx,self.maxx,self.miny,self.maxy = x-width*20,x+width*20,y-height*20,y+height*20
    def inBounds(self,x,y):
        if self.active:
            if x > self.minx and x < self.maxx:
                if y > self.miny and y < self.maxy:
                    if self.fnction['function'] != None:
                        self.fnction['function']()
                    return True
        return False
    def remove(self):
        self.active = False
        self.button.hideturtle()
        self.button.clear()
    def activate(self):
        self.active = True
        self.button.showturtle()
    def assign(self, fnc):
        self.fnction['function'] = fnc

#Casual on click function
def onClick(event):
    global btns, loop_trigger
    x,y=event.x,event.y
    flag = False
    for btn in btns:
        temp = btn.inBounds(x,y)
        if temp:
            flag = True
    if flag:
        for btn in btns:
            btn.remove()
        load_map()
        game_loop()
        
        
cnv.bind('<Button-1>',onClick)

#Enemy movements
def en_mov():
    global d6,d7,eSpeed,melee_enemies,enem_pos,current_hp,difficulty,glblLoading
    d6 = time.time()
    x = main.xcor()
    y = main.ycor()
    factor = d6-d7
    indxs = []
    rmvd = []
    nonstationary = not glblLoading
    lowposx = 0
    lowposy = 0
    hiposx = 0
    hiposy = 0
    if nonstationary:
        for i in range(len(melee_enemies)):
            enem = melee_enemies[i]
            ex = enem.xcor()
            ey = enem.ycor()
            if abs(ex-x) < 20 and abs(ey-y)<20: #Takes enemy and adds to list for removal
                rmvd.append([i,enem])
            else:
                if ex < x: enem.setx(ex+(eSpeed*factor))
                else: enem.setx(ex-(eSpeed * factor))
                if ey < y: enem.sety(ey+(eSpeed * factor))
                else: enem.sety(ey-(eSpeed * factor))
                if ex < lowposx: lowposx = ex
                elif ex > hiposx: hiposx = ex
                if ey < lowposy: lowposy = ey
                elif ey > hiposy: hiposy = ey
                enem_pos.append([ex,ey])
            wn.update()
        enem_pos.append([lowposx,lowposy,hiposx,hiposy])
    n = len(rmvd)
    for i in range(len(rmvd)):
        subj = rmvd[n-(i+1)]
        kill_enemy(subj[0],subj[1])
        dmg1 = (random.random()*difficulty/2)
        dmg = math.floor(13*dmg1)
        current_hp -= dmg #crit chance
    d7 = time.time()

#Spawn Enemy
def spawn_enemy():
    global screendim, melee_enemies,wn
    ene = turtle.RawTurtle(wn)
    ene.hideturtle()
    ene.penup()
    ene.goto(random.randint(-screendim[0]/2,screendim[0]/2),random.randint(-screendim[1]/2,screendim[1]/2))
    ranSize = random.random()+0.5
    ene.shapesize(ranSize,ranSize,1)
    ene.speed(0)
    ene.color('dark red')
    ene.shape('square')
    ene.showturtle()
    ene.penup()
    melee_enemies.append(ene)
    return

#Despawn All Enemies
def despawnAll():
    global melee_enemies
    num = len(melee_enemies)
    if num != 0:
        for i in range(len(melee_enemies)):
            n = num-i
            enemy = melee_enemies[n]
            enemy.hideturtle()
            enemy.clear()
            melee_enemies.pop(n)
    return

#Kill specific enemy
def kill_enemy(indx, enem):
    global melee_enemies
    melee_enemies.pop(indx)
    enem.hideturtle()
    enem.clear()
    wn.update()

#BULLETS --------------------------------------------------------------

def fire_bulet():  # Controls the bullet travelling
    global character_angle, bulet_count, d3, high_quality_mode
    d3 = time.time()
    x = main.xcor()
    y = main.ycor()
    bulet = turtle.RawTurtle(wn)
    bulet.hideturtle()
    bulet.penup()
    bulet.goto(x,y)
    if high_quality_mode:
        bulet.shape('bullet'+calcBulletTexture(character_angle,16))
    else:
        bulet.shape('square') # Makes the bullet
        bulet.color('yellow')
    bulet.speed(0)
    bulet.showturtle()
    bulet.shapesize(0.5,0.5)
    bulet.setheading(character_angle)
    bulet_count.append(bulet)

def calcBulletTexture(angle, spriteRange):
    spriteRange -= 1
    angle -= 90
    if angle < 0:
        angle += 360
    
    incre = 360/spriteRange
    newC = angle/incre
    res = 0
    if (newC - math.floor(newC)) > 0.49:
        res = math.ceil(newC)
    else: res = math.floor(newC)
    
    result = spriteRange-res
    return str(result+1)

def testCollision(x,y):
    global melee_enemies
    rmvd = []
    for i in range(len(melee_enemies)):
        enem = melee_enemies[i]
        ex = enem.xcor()
        if abs(ex-x) < 15: #5 is collision radius for x
            ey = enem.ycor()
            if abs(ey-y) < 15: #5 is collision radius for y
                rmvd.append([i,enem])
    n = len(rmvd)
    for i in range(n):
        kill_enemy(rmvd[n-(i+1)][0],rmvd[n-(i+1)][1])

def movingbulet():
    global bulet_count,d4,d5,bSpeed,enem_pos, melee_enemies
    #Semi-efficient collision detection...
    #Checks if even in range of the xcor of all bullets by comparing to the range
    #Then checks the ycor range
    #Only if both are in range, then tests for collision testCollision
    d4 = time.time()
    m = len(enem_pos)-1
    lox,loy,hix,hiy = 0,0,0,0
    if m >= 0:
        lox = enem_pos[m][0]
        loy = enem_pos[m][1]
        hix = enem_pos[m][2]
        hiy = enem_pos[m][3]
    for bullet in bulet_count:
        bullet.forward(bSpeed*(d4-d5))
        bx = bullet.xcor()
        if bx > lox-15 and bx < hix+15:
            by = bullet.ycor()
            if by > loy-15 and by < hiy+15:
                testCollision(bx,by) #Piercing shot
        wn.update()
    d5 = time.time()
   
def end_game(): # Function to end game once the player completes the game or ends once died
    sys.exit()

def bounceOffset():
    global d12, bounceSpeed,bouncePeak
    temp = time.time()-d12
    if temp > bounceSpeed:
        d12 = time.time()
        temp = time.time()-d12
    res = 360/bounceSpeed
    return bouncePeak*math.sin(math.radians(temp*res))
    
def movement():
    global keyt, pSpeed, d1, d2, pRate, d3,pcorx,pcory,nxtInit, canEnd, rstMode
    d1 = time.time()
    factor = d1-d2
    if keyt.isPressed('w'):
        pcory += pSpeed*factor
    if keyt.isPressed('a'):
        pcorx -= pSpeed*factor
    if keyt.isPressed('s'):
        pcory -= pSpeed*factor
    if keyt.isPressed('d'):
        pcorx += pSpeed*factor
    if keyt.isPressed('space'):
        if time.time()-d3 > pRate:
            fire_bulet()
    if keyt.isPressed('e'):
        if not nxtInit:
            if door_close and main.distance(door) < 80:
                current_map()
            nxtInit = True
    if keyt.isPressed('r'):
        if canEnd:
            rstMode = True
            canEnd = False
    grabOffset = bounceOffset()
    main.sety(pcory+grabOffset)
    main.setx(pcorx)
    mainshd.setx(main.xcor())
    mainshd.sety(main.ycor()-(55+grabOffset*1.6))
        
    d2 = time.time()

def oceanRender():
    global oceans, curOcean,wn,d10,d11, mSpeed
    d11 = time.time()
    if d11-d10 > mSpeed:
        if curOcean == len(oceans):
            curOcean = 0
        wn.bgpic(oceans[curOcean])
        curOcean += 1
        d10 = time.time()

def rotAngle(set1,set2):
    dx = set1[0] - set2[0]
    dy = set1[1] - set2[1]
    angle = math.degrees(math.atan2(dy,dx))
    return angle

#Get Live Mouse Position Using Tkinter -------
def mouse_pos(event):
    global character_angle,screendim
    character_angle = 0
    chrx = main.xcor()
    chry = main.ycor()
    cursor_x, cursor_y = event.x-(screendim[0]/2),(screendim[1]/2)-event.y

    character_angle = rotAngle([chrx,chry],[cursor_x,cursor_y])-180
    if character_angle < 0:
        character_angle = 360+character_angle
cnv.bind("<Motion>", mouse_pos)

def restart_game():
    global next_map
    next_map = -1
    restart()

def game_loop(): # Main game loop
    global current_hp, difficulty,next_map, melee_enemies,glblLoading,rstMode,canEnd
    global door_close
    global door_message_displayed
    round_state = False
    peaceful_mode = False
    formerhp = 0
    while True: # Runs entire game :0000000
        movement()
        if rstMode:
            rstMode = False
            next_map = 0
            main.hideturtle()
            break
        wn.update()
        if high_quality_mode:
            oceanRender()
            wn.update()
        if next_map == 5:
            loop_trigger = False
           
            pen.clear()
           
            end_pen.penup()
            end_pen.goto(0,0)
            end_pen.pendown()
            end_pen.write("That's the end...", align="center", font=("Courier", 25, "normal"))
           
            choice_pen.penup()
            choice_pen.goto(0,-80)
            choice_pen.pendown()
            choice_pen.write("Press 'R' to restart", align="center", font=("Courier", 14, "normal")) # Displays the options for the player
            canEnd = True
            choice_pen.penup()
        else:
            en_mov()
            wn.update()
            movement()
            wn.update()
            movingbulet()
            wn.update()
            if formerhp != current_hp:
                pen.clear()
                pen.write("Health: {}".format(current_hp), align="center", font=("Courier", 24, "normal"))
                formerhp = current_hp
                if current_hp <=0:
                    next_map = 5
                    despawnAll()
            wn.update()
            if not peaceful_mode:
                if not round_state:
                    if next_map > 0:
                        glblLoading = True
                        for i in range(next_map+random.randint(0,difficulty)):
                            spawn_enemy()
                        round_state = True
                        glblLoading = False
                    else:
                        next_map += 1
                elif len(melee_enemies) == 0:
                    main.goto(0,0)
                    next_map += 1
                    round_state = False
    title_screen()

#Decisions Decisions...
def easychoice():
    global difficulty
    difficulty = 1
def mediumchoice():
    global difficulty
    difficulty = 2
def hardchoice():
    global difficulty
    difficulty = 4

def title_screen():
    global btns, difficulty
    wn.bgpic('')
    wn.bgcolor("#ADD8E6")
    pen.penup()
    pen.goto(0,100)
    pen.pendown()
    end_pen.clear()
    choice_pen.clear()
    pen.write("Welcome to Pirate Shoot Shoot!", align="center", font=("Courier", 20, "normal"))
    ezbtn = turtleButton(-screendim[1]/2,-screendim[1]/3,'green',5,2)
    mdbtn = turtleButton(0,-screendim[1]/3,'yellow',5,2)
    hdbtn = turtleButton(screendim[1]/2,-screendim[1]/3,'red',5,2)
    ezbtn.assign(easychoice)
    mdbtn.assign(mediumchoice)
    hdbtn.assign(hardchoice)
    btns.append(ezbtn)
    btns.append(mdbtn)
    btns.append(hdbtn)
    wn.update()

#Key Tracking Class Call
keyt = KeyTracker(gui)
title_screen()    
gui.mainloop()
