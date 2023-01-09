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
    if direction * angle >= 360: #обнуляем угол если мы сделали полный круг
        angle = 0
    x = 200 * cos(radians(angle)) #считаем, на сколько изменятся координаты точки
    y = 200 * sin(radians(angle))
    angle += 1 * direction #увеличиваем угол, если идём по часовой и уменьшаем, если идём против
    canvas.coords(dot, 300 + x, 300 + y, 300 + x, 300 + y) #изменяем координаты точки
    root.after(1000 // speed, motion, angle)
root.after(1000 // speed, motion, 0) 

root.mainloop()
