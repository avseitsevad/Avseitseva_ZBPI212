from tkinter import *
from random import randint

class Raindrop: #пишем класс для капель дождя
    def __init__(self, canvas, x, y, length, color = 'lightblue'):
        self.x = x
        self.y = y
        self.length = length
        self.canvas = canvas
        self.line = canvas.create_line(self.x, self.y, self.x, self.y + length, fill = color, width = 2)
        self.speed = length // 5 #чем больше длина (чем ближе капля), тем больше скорость
    def move(self):
        self.y += self.speed #изменение координаты равно скорости с которой движется капля
        self.canvas.move(self.line, 0, self.speed) #двигаем каплю на 0 по х и с нужной скоростью по у
        if self.y > size: #если капля выходит за нижнюю границу экрана, то передвигаем её обратно наверх
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
#генерируем капли с выбранной плотностью с рандомными координатами и длиной в диапазоне от 10 до 40
drops = [Raindrop(canvas, x = randint(0, size), y = randint(0, size), length = randint(10, 40)) for i in range (density)] 
redraw()

root.mainloop()
