from tkinter import *
import turtle
import random
import time
import sys
import math
from threading import *
from PIL import Image

#Images
imgp = 'plr.gif'
img = Image.open(imgp)

delay = 0.0000001
next_map = -1
difficulty = 10
pSpeed = 40
pRate = 0.5
bSpeed = 60
eSpeed = 50

#Delta time chicanery
d1 = time.time()
d2 = time.time()
d3 = time.time()
d4 = time.time()
d5 = time.time()
d6 = time.time()
d7 = time.time()
d8 = time.time()
d9 = time.time()

gui = Tk()
gui.geometry('600x600')
cnv = Canvas(gui,width=600,height=600)
cnv.pack()
wn = turtle.TurtleScreen(cnv)
wn.addshape(imgp)
main = turtle.RawTurtle(wn)
bulet = turtle.RawTurtle(wn)
pen = turtle.RawTurtle(wn)
door_pen = turtle.RawTurtle(wn)
choice_pen = turtle.RawTurtle(wn)
door = turtle.RawTurtle(wn)
end_pen = turtle.RawTurtle(wn)
easy_choice = turtle.RawTurtle(wn)
normal_choice = turtle.RawTurtle(wn)
hard_choice = turtle.RawTurtle(wn)
plr = turtle.RawTurtle(wn)
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
easy_choice.hideturtle()
normal_choice.hideturtle()
hard_choice.hideturtle()
plr.hideturtle()

melee_enemies = [] # Sets the enemy count to zero
bulet_count = []

def restart():# The main game function
    global current_hp
    global loop_trigger
    global melee_enemies
    global buletstate
    global next_map
   
    for enemy in melee_enemies:
        enemy.hideturtle()
   
    current_map() # Sets the next map
    door_pen.clear()
    end_pen.clear()
    choice_pen.clear()
    main.speed(0) # Makes the main player
    main.shape('circle')
    main.color("black")
    main.penup()
    main.goto(0,0)
    main.showturtle()
    main.direction = "stop"

    plr.speed(0)
    plr.shape(imgp)
    plr.penup()
    plr.goto(0,0)
    plr.showturtle()
    
    buletstate = "ready"
    pen.showturtle()
    pen.speed(0) # Sets the pen that displays the player's health
    pen.clear()
    pen.shape("square")
    pen.penup()
    pen.hideturtle()
    pen.goto(145,-270)
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
    door.hideturtle()
    door.goto(0,320)
    current_hp = 100
    loop_trigger = True
    for i in range(next_map): # Makes the amount of enemys required for a specific room in random spots
        enemy = turtle.RawTurtle(wn)
        enemy.speed(0)
        enemy.shape('square')
        enemy.color("red")
        enemy.penup()
        enemy.goto(random.randint(-300, 300), random.randint(-300, -50))
        melee_enemies.append(enemy)
    game_loop() # Calls the main while loop to run
   
def current_map(): # Sets the next map when the player interacts with the door
    global next_map, melee_enemies
    if len(melee_enemies) == 0:
        map = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#9B59B6", "#1ABC9C"]
        wn.bgcolor(map[next_map])
        wn.tracer(0)
        
        next_map += 1
       
        main.penup()
        main.goto(0,-270)

#We made a class for key presses to clean up the spaghetti code
#This code is heavily referenced from AI generated code but remains
#Solely written and applied by us :)
class KeyTracker:
    def __init__(self, root):
        self.gui = gui
        self.keys = set()
        # Bind key press and release events
        gui.bind("<KeyPress>", self.key_press)
        gui.bind("<KeyRelease>", self.key_release)
    def key_press(self, event):
        self.keys.add(event.keysym.lower())
        self.update_label()
    def key_release(self, event):
        self.keys.discard(event.keysym.lower())
        self.update_label()
    def update_label(self):
        self.label.config(text=f"Keys down: {self.keys}")
        self.gui.update()
    def run(self):
        self.label = Label(self.gui)
        self.label.place(x=5,y=5)
    def isPressed(self,keyPressed):
        if keyPressed in self.keys:
            return True
        else: return False

#Enemy movements

def En_movx():
    global d6, d7
    d6 = time.time()
    factor = d6 - d7
    for enemy in melee_enemies: # Controls the enemy's x-axis movement towards the player    
        x = main.xcor()
        bad_x = enemy.xcor()
        if x > bad_x:
            x = enemy.xcor()
            enemy.setx(eSpeed * factor)
        x = main.xcor()
        bad_x = enemy.xcor()
        if x < bad_x:
            x = enemy.xcor()
            enemy.setx(-eSpeed * factor)
    d7 = time.time()

def En_movy():
    global d8, d9
    d8 = time.time()
    for enemy in melee_enemies: # Controls the enemy's y-axis movement towards the player
        y = main.ycor()
        bad_y = enemy.ycor()
        if y > bad_y:
            y = enemy.ycor()
            enemy.sety(eSpeed * factor)
        y = main.ycor()
        bad_y = enemy.ycor()
        if y < bad_y:
            y = enemy.ycor()
            enemy.sety(-eSpeed * factor)
    d9 = time.time()



def fire_bulet():  # Controls the bullet travelling
    global character_angle, bulet_count, d3
    d3 = time.time()
    x = main.xcor()
    y = main.ycor()
    bulet = turtle.RawTurtle(wn)
    bulet.showturtle()
    bulet.shape('square') # Makes the bullet
    bulet.color('yellow')
    bulet.penup()
    bulet.speed(0)
    bulet.showturtle()
    bulet.shapesize(0.5,0.5)
    bulet.setx(x)
    bulet.sety(y)
    bulet.setheading(character_angle)
    bulet_count.append(bulet)

def movingbulet():
    global bulet_count,d4,d5,bSpeed
    d4 = time.time()
    for bullet in bulet_count:
        bullet.forward(bSpeed*(d4-d5))
    d5 = time.time()
   
def end_game(): # Function to end game once the player completes the game or ends once died
    sys.exit()

def movement():
    global keyt, pSpeed, d1, d2, pRate, d3
    d1 = time.time()
    factor = d1-d2
    if keyt.isPressed('w'):
        main.sety(main.ycor()+pSpeed*factor)
    if keyt.isPressed('a'):
        main.setx(main.xcor()-pSpeed*factor)
    if keyt.isPressed('s'):
        main.sety(main.ycor()-pSpeed*factor)
    if keyt.isPressed('d'):
        main.setx(main.xcor()+pSpeed*factor)
    if keyt.isPressed('space'):
        if time.time()-d3 > pRate:
            fire_bulet()
    if keyt.isPressed('e'):
        if door_close and main.distance(door) < 80:
            current_map()
        
    d2 = time.time()

def game_loop(): # Main game loop
    global loop_trigger
    global current_hp
    global door_close
    global door_message_displayed
   
    while loop_trigger: # Enables and disables when needed with the "loop_trigger" variable
        movement()
        if next_map == 5:
            loop_trigger = False
           
            pen.clear()
           
            end_pen.penup()
            end_pen.goto(0,0)
            end_pen.pendown()
            end_pen.write("Congratulations! You Win!", align="center", font=("Courier", 25, "normal"))
           
            choice_pen.penup()
            choice_pen.goto(0,-80)
            choice_pen.pendown()
            choice_pen.write("Press 'R' to restart or Press 'P' to end game", align="center", font=("Courier", 14, "normal")) # Displays the options for the player
            choice_pen.penup()
            wn.onkey(restart_game, 'r') # Enables 'R' for the player to restart
            wn.onkey(end_game, 'p') # Enables 'P' for the player to end the program
           
        
        En_movx()
        En_movy()
        movingbulet()
        wn.update()  # Update the screen to show changes
        if current_hp > 0:
            pen.clear()
            pen.write("Health: {}".format(current_hp), align="center", font=("Courier", 24, "normal"))
       
        for enemy in melee_enemies:
            if main.distance(enemy) < 20: # Sends enemy back (Bounces the enemy back) and damages the player
                current_hp -= difficulty
                y = main.ycor()
                bad_y = enemy.ycor()
                if y > bad_y and y != bad_y: # Sends the enemy back straight instead of diagonal if x or y is = to the enemy
                    y = enemy.ycor()
                    enemy.sety(y - 30)
                y = main.ycor()
                bad_y = enemy.ycor()
                if y < bad_y and y != bad_y:
                    y = enemy.ycor()
                    enemy.sety(y + 30)
                   
                x = main.xcor()
                bad_x = enemy.xcor()
                if x > bad_x and x != bad_x:
                    x = enemy.xcor()
                    enemy.setx(x - 30)
                x = main.xcor()
                bad_x = enemy.xcor()
                if x < bad_x and x != bad_x:
                    x = enemy.xcor()
                    enemy.setx(x + 30)
            if bulet.distance(enemy) < 20:
                enemy.hideturtle()
                melee_enemies.remove(enemy)
            
            
        if current_hp == 0: # Checks if the player's health is at zero, and if so it stops the game and displays "GAME OVER"
            pen.clear()
           
            main.hideturtle()
            enemy.hideturtle()
            bulet.hideturtle()
           
            pen.penup()
            pen.goto(0,0)
            pen.pendown()
            pen.write("GAME OVER", align="center", font=("Courier", 24, "normal")) # Displays "GAME OVER"
            pen.penup()
            choice_pen.penup()
            choice_pen.goto(0,-80)
            choice_pen.pendown()
            choice_pen.write("Press 'R' to restart or Press 'P' to end game", align="center", font=("Courier", 14, "normal")) # Displays the options for the player
            choice_pen.penup()
            current_hp -= 1
            loop_trigger = False
            wn.onkey(restart_game, 'r') # Enables 'R' for the player to restart
            wn.onkey(end_game, 'p') # Enables 'P' for the player to end the program
           
        if door_close and main.distance(door) < 80: # Checks if the player is near the door to interact with
            if not door_message_displayed:
                door_pen.penup()
                door_pen.goto(0, 270)
                door_pen.pendown()
                door_pen.write("Press 'E' to open door", align="center", font=("Courier", 10, "normal"))
                door_pen.penup()
                wn.onkeypress(restart, 'e')
                door_message_displayed = True # Sets the variable to true to allow the text to display to interact with the door
        elif door_close and main.distance(door) > 80: # Checks if the player is far enough from the door to keep them from going to the next room unintentionally
            if door_message_displayed:
                door_pen.clear()
                door_message_displayed = False # Sets the variable to false to remove the text for interacting with the door

def rotAngle(set1,set2):
    dx = set1[0] - set2[0]
    dy = set1[1] - set2[1]
    angle = math.degrees(math.atan2(dy,dx))
    return angle

#Get Live Mouse Position Using Tkinter -------
def mouse_pos(event):
    global character_angle
    character_angle = 0
    chrx = main.xcor()
    chry = main.ycor()
    cursor_x, cursor_y = event.x-300,300-event.y

    character_angle = rotAngle([chrx,chry],[cursor_x,cursor_y])-180
    if character_angle < 0:
        character_angle = 360+character_angle
cnv.bind("<Motion>", mouse_pos)

def restart_game():
    global next_map
    next_map = -1
    restart()

def title_screen():
    
    wn.bgcolor("#ADD8E6")
    pen.penup()
    pen.goto(0,100)
    pen.pendown()
    pen.write("Welcome to Pirate Shoot Shoot!", align="center", font=("Courier", 20, "normal"))
    
    easy_choice.penup()
    easy_choice.speed(0)
    easy_choice.goto(-85,10)
    easy_choice.setheading(180)
    easy_choice.color("green")
    easy_choice.pendown()
    easy_choice.begin_fill()
    for i in range(2):
        easy_choice.forward(80)
        easy_choice.left(90)
        easy_choice.forward(40)
        easy_choice.left(90)
    easy_choice.end_fill()
    
    normal_choice.penup()
    normal_choice.speed(0)
    normal_choice.goto(40,10)
    normal_choice.setheading(180)
    normal_choice.color("yellow")
    normal_choice.pendown()
    normal_choice.begin_fill()
    for i in range(2):
        normal_choice.forward(80)
        normal_choice.left(90)
        normal_choice.forward(40)
        normal_choice.left(90)
    normal_choice.end_fill()  
    
    hard_choice.penup()
    hard_choice.speed(0)
    hard_choice.goto(165,10)
    hard_choice.setheading(180)
    hard_choice.color("red")
    hard_choice.pendown()
    hard_choice.begin_fill()
    for i in range(2):
        hard_choice.forward(80)
        hard_choice.left(90)
        hard_choice.forward(40)
        hard_choice.left(90)
    hard_choice.end_fill()
    
    def on_click(x,y):
        global difficulty
        if -165 <= x and x <= -85 and -30 <= y and y <= 10:
            difficulty = 5
            pen.clear()
            easy_choice.clear()
            normal_choice.clear()
            hard_choice.clear()
            restart()
            x = 0
            y = 0
        elif -40 <= x and x <= 40 and -30 <= y and y <= 10:
            difficulty = 10
            pen.clear()
            easy_choice.clear()
            normal_choice.clear()
            hard_choice.clear()
            restart()
            x = 0
            y = 0
        elif 85 <= x and x <= 165 and -30 <= y and y <= 10:
            difficulty = 20
            pen.clear()
            easy_choice.clear()
            normal_choice.clear()
            hard_choice.clear()
            restart()
            x = 0
            y = 0
    
    wn.onclick(on_click)

#Key Tracking Class Call
keyt = KeyTracker(gui)
keyt.run()

title_screen()    

gui.mainloop()
