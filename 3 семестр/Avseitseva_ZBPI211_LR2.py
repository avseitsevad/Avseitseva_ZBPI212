from tkinter import *
from random import randint
class Raindrop:
    def __init__(self, canvas, x, y, length, color = 'lightblue'):
        self.x = x
        self.y = y
        self.length = length
        self.canvas = canvas
        self.line = canvas.create_line(self.x, self.y, self.x, self.y + length, fill = color, width = 2)
        self.speed = length // 5
    def move(self):
        self.y += self.speed
        self.canvas.move(self.line, 0, self.speed)
        if self.y > size:
            self.canvas.move(self.line, 0, -(size + self.length))
            self.y -= size + self.length

def redraw():
    for drop in drops:
        drop.move()
    root.after(10, redraw)

root = Tk()
size = 800
canvas = Canvas(root, width = 800, height = 800, bg = '#000064')
canvas.pack()

density = int(input('Выберите плотность капель (100 - 1000): '))
drops = [Raindrop(canvas, x = randint(0, size), y = randint(0, size),
length = randint(10, 40)) for i in range (density)]

redraw()

root.mainloop()
