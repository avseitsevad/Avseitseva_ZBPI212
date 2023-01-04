from tkinter import *

root = Tk()
size = 800
center = size // 2
canvas = Canvas(root, width = size, height = size, bg = 'black')
canvas.pack()
gravitaion = 0.1 #величина с которой изменяется скорость падения при отскоке от пола

class Ball():
    def __init__(self, canvas, radius = 30):
        #создаём частицу
        self.canvas = canvas
        self.x0 = center - radius
        self.y0 = center - radius
        self.x1 = center + radius
        self.y1 = center + radius
        self.speedY = 0
        self.oval = canvas.create_oval(self.x0, self.y0, self.x1, self.y1, width = 3, fill = 'grey', outline = 'white')
    def move(self):
        self.speedY += gravitaion
        self.y1 += self.speedY
        self.canvas.move(self.oval, 0, self.speedY)
        if self.y1 >= size and self.y1 - self.speedY <= size:
            self.speedY = -self.speedY #отскакиваем обратно при соприкосновении с полом


ball = Ball(canvas)
def redraw():
    if ball.y1 + ball.speedY >= size and ball.y1 - ball.speedY >= size: 
        return
        #вовремя выходим чтобы частица не начала бесконечно прыгать на границе окна
    ball.move()
    root.after(10, redraw)

redraw()
root.mainloop()