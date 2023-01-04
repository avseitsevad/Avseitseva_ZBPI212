from tkinter import *
from math import cos, sin, radians

root = Tk()
canvas = Canvas(root, width = 600, height = 600)
canvas.pack()
cirlce = canvas.create_oval(100, 100, 500, 500)
dot = canvas.create_oval(300, 300, 300, 300, width = 3, outline = 'red')

speed = int(input('Введите скорость движения точки (1 - 1000): '))
direction = int(input('Выберите направление: по часовой стрелке - 1, против - -1: '))

def motion(angle):
    if direction * angle >= 360:
        angle = 0
    x = 200 * cos(radians(angle))
    y = 200 * sin(radians(angle))
    angle += 1 * direction
    canvas.coords(dot, 300 + x, 300 + y, 300 + x, 300 + y)
    root.after(1000 // speed, motion, angle)
root.after(1000 // speed, motion, 0)

root.mainloop()
