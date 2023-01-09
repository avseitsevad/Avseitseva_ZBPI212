from tkinter import *

root = Tk()
size = 800
center = size // 2
canvas = Canvas(root, width = size, height = size, bg = 'black')
canvas.pack()
gravitaion = 0.1 #величина с которой изменяется скорость падения при отскоке от пола

class Ball(): #создаём класс для частицы
    def __init__(self, canvas, radius = 30):
        self.canvas = canvas
        self.x0 = center - radius
        self.y0 = center - radius
        self.x1 = center + radius
        self.y1 = center + radius
        self.speedY = 0 #собственной скорости у неё пока нет, но появится как только она начнёт падать
        self.oval = canvas.create_oval(self.x0, self.y0, self.x1, self.y1, width = 3, fill = 'grey', outline = 'white') 
    def move(self):
        self.speedY += gravitaion #благодаря гравитации у частицы появляется скорость
        self.y1 += self.speedY #координата по у меняется на полученную скорость
        self.canvas.move(self.oval, 0, self.speedY) #двигаем частицу
        if self.y1 >= size and self.y1 - self.speedY <= size:
            self.speedY = -self.speedY #отскакиваем обратно при соприкосновении с полом


ball = Ball(canvas)
def redraw():
    if ball.y1 + ball.speedY >= size and ball.y1 - ball.speedY >= size: #вовремя выходим чтобы частица не начала бесконечно прыгать на границе окна
        return
    ball.move()
    root.after(10, redraw)

redraw()
root.mainloop()
