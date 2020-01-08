import tkinter as tk
import random

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400

GAME_TICK = int(1000/30)

class Paddles:
    def __init__(self,x,y,v):
        self.x = int(x)
        self.y = int(y)
        self.v = int(v)

        self.action_state = "idle"

        self.img = tk.PhotoImage(file="sprites/Paddle.gif")

        self.imageID = canvas.create_image(x,y,image= self.img)

        self.update_image()

    def update_image(self):
        if self.action_state == "move up" and self.y - int(125/2) >0:
            canvas.move(self.imageID,0,-1 * self.v)
            self.y -= self.v

        if self.action_state == "move down" and self.y + int(125/2) < SCREEN_HEIGHT:
            canvas.move(self.imageID,0, self.v)
            self.y += self.v

        self.action_state = "idle"

        win.after(GAME_TICK, self.update_image)

    def move_up(self,event):
        self.action_state = "move up"
        
    def move_down(self,event):
        self.action_state = "move down"

class PlayerPaddles(Paddles):
    def __init__(self,x,y,v):
        Paddles.__init__(self,x,y,v)
        
        win.bind('<Up>',self.move_up)
        win.bind('<Down>',self.move_down)

class EnemyPaddles(Paddles):
    def __init__(self,x,y,v,b):
        Paddles.__init__(self,x,y,v)

        self.b = b

        self.checkPos()

    def checkPos(self):
        if self.b.y > self.y:
            self.action_state = "move down"
        if self.b.y < self.y:
            self.action_state = "move up"

        win.after(GAME_TICK, self.checkPos)

        
class Ball:
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.vx = (-1)**random.randrange(2) * 3
        self.vy = (-1)**random.randrange(2) * 5

        self.img = tk.PhotoImage(file="sprites/Ball.gif")

        self.imageID = canvas.create_image(x,y,image= self.img)

        self.update_image()
        
    def update_image(self):
        
        canvas.move(self.imageID,self.vx,self.vy)

        self.x = self.vx + self.x
        self.y = self.vy + self.y

        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.vy = -1 * self.vy

        win.after(GAME_TICK, self.update_image)

    def bounce(self,Paddle):
        if self.x - Paddle.x < 23 and self.x - Paddle.x < 0 and abs(self.y - Paddle.y) < int(125/2 + 10):
            self.vx *= -1
        

class Game:
    def __init__(self):

        self.img0 = tk.PhotoImage(file="sprites/background.gif")
        
        canvas.create_image(0,0,image = self.img0)

        self.player = PlayerPaddles(SCREEN_WIDTH / 14 ,SCREEN_HEIGHT/2, 10)

        self.ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.enemy = EnemyPaddles(SCREEN_WIDTH - SCREEN_WIDTH / 14 ,SCREEN_HEIGHT/2,10, self.ball)

        self.update_image()

    def update_image(self):
        bounced  = False

        if self.ball.x < SCREEN_WIDTH / 7 and self.ball.x > 0:
            bounced = self.bounce(self.ball,self.player)

        if self.ball.x > (SCREEN_WIDTH / 7) * 6 and self.ball.x < (SCREEN_WIDTH):
            bounced = self.bounce(self.ball,self.enemy)

        if bounced == True:
            win.after(GAME_TICK*30, self.update_image)
        else:
            win.after(GAME_TICK, self.update_image)

    def bounce(self,ball,Paddle):
        if abs(ball.x - Paddle.x) < 23 and abs(ball.y - Paddle.y) < int(125/2 + 10):
            ball.vx *= -1.1
            ball.vy *= 1.1
            return True
        return False

        


        

        

    


win = tk.Tk()
win.minsize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
win.maxsize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

win.title("PONG")
canvas = tk.Canvas(win, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

g = Game() 

tk.mainloop()
