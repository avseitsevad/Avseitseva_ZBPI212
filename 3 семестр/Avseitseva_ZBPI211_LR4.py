import pygame, sys, random, math

pygame.init()

width = 1200
height = 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
FPS = 30
clock = pygame.time.Clock()
pygame.display.set_caption("Agar.io")

cell_count = 3000 # количество клеток для поедания на поле
map_size = 2000 # размер карты на которой генерируются клетки для поедания
spawn_size = 25 # размер клетки игрока на спавне
respawn_cells = True
player_color = (255, 0, 0)
background_color = (0, 0, 0)

# описываем класс для клеток
class Cell:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
    def collide_check(player):
        for cell in cells:
            # если расстояние между игроком и обычной клеткой меньше суммы их радиусов:
            if math.sqrt(((player.x - width // 2 + cell.x) ** 2) + (player.y - height / 2 + cell.y) ** 2) <= cell.radius + player.radius:
                # съедаем клетку: убираем её из списка
                cells.remove(cell)
                # увеличиваем радиус игроку
                player.radius += 1
                if respawn_cells:
                    # вместо съеденной клетки спавним ещё одну
                    cells.append(Cell(random.randint(-map_size, map_size), random.randint(-map_size, map_size), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5))
    def draw(self, surface, x, y):
        # функция для рисования клеток - кругов
        pygame.draw.circle(surface, self.color, (x, y), self.radius)

# генерируем клетки для поедания: в координатах (-map_size, map_size), с рандомным цветом и радиусом 5
cells = [Cell(random.randint(-map_size, map_size), random.randint(-map_size, map_size), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5) for i in range (cell_count)]
# создаём клетку-игрока в центре поля с заданным цветом и радиусом
player_cell = Cell(0, 0, player_color, spawn_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION: # двигаемся за мышкой
            mouse_x, mouse_y = event.pos
    
    player_cell.collide_check() # проверяем, не столкнулись ли мы с другими клетками

    # двигаем клетку игрока: чем дальше от неё курсор, тем больше скорость
    # также чем больше наша масса (радиус), тем скорость меньше 
    player_cell.x += (width // 2 - mouse_x) // player_cell.radius 
    player_cell.y += (height // 2 - mouse_y) // player_cell.radius 
    # т. к. клетка игрока остаётся неподвижной по центру, отрисовываем остальные клетки относительно неё
    for cell in cells:
        cell.draw(screen, cell.x + player_cell.x, cell.y + player_cell.y)
    #рисуем клетку игрока по центру экрана
    player_cell.draw(screen, width / 2, height / 2) 
    pygame.display.update()
    clock.tick(FPS)
    screen.fill(background_color)

