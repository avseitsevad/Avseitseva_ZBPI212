import pygame, random, math, time

pygame.init()
pygame.mixer.init()
width = 800
height = 600
FPS = 60
lives = 3
score = 0
game_over = False
game_started = False

# изображения для фона и заставки, звук
background = pygame.image.load('ricerocks/images/nebula_blue.f2014.png')
moving_background = pygame.image.load('ricerocks/images/debris2_blue.png')
moving_background = pygame.transform.scale(moving_background, (800, 600))
moving_background_x = 0
splash = pygame.image.load('ricerocks/images/splash.png')
soundtrack = pygame.mixer.Sound('ricerocks/sounds/soundtrack.mp3')
soundtrack.play()

# изображения корабля
ship_image = pygame.image.load('ricerocks/images/ship.png')
ship_thrust_image = pygame.image.load('ricerocks/images/ship_thrust.png')
thrust_sound = pygame.mixer.Sound('ricerocks/sounds/thrust.mp3')
thrust_sound.set_volume(0.2)
# изображение и звук ракеты
bullet_image = pygame.image.load('ricerocks/images/shot.png')
bullet_sound = pygame.mixer.Sound('ricerocks/sounds/missile.mp3')
bullet_sound.set_volume(0.2)

# изображения и звук взрыва астероидов
asteroid_image = pygame.image.load('ricerocks/images/asteroid.png')
explosion_sound = pygame.mixer.Sound('ricerocks/sounds/explosion.mp3')
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
font = pygame.font.SysFont('segoui', 36)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.vel = 0
        self.angle = 0
        self.x = width // 2
        self.y = height // 2
        self.thrust = False
        self.last_shot = 0
        self.cooldown = 0.2
        self.image = ship_image
        self.rect = self.image.get_rect(center = (self.x, self.y))
    def update(self):
        global asteroid_sprites, lives, game_over, game_started
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 0.3
        if keys[pygame.K_RIGHT]:
            self.angle += -0.3
        if keys[pygame.K_UP]:
            self.thrust = True
        if keys[pygame.K_SPACE]:
            if time.time() - self.last_shot > self.cooldown:
                bullet = Bullet(self.x, self.y, self.direction)
                all_sprites.add(bullet)
                self.last_shot = time.time()
                bullet_sound.play()
        self.direction += self.angle
        self.x += self.vel * math.cos(math.radians(-self.direction))
        self.y += self.vel * math.sin(math.radians(-self.direction))
        self.x %= width
        self.y %= height
        if self.thrust:
            self.vel += 0.5
            self.image = ship_thrust_image
            self.thrust = False
            thrust_sound.play()
        else:
            self.image = ship_image
            thrust_sound.stop()
        self.vel *= 0.95
        self.angle *= 0.95
        self.image = pygame.transform.rotate(self.image, self.direction)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        hit = pygame.sprite.spritecollide(self, asteroid_sprites, True)
        if hit and lives >= 1:
            lives -= 1
            self.x = width // 2
            self.y = height // 2
        elif hit:
            game_over = True
            game_started = False
        
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.randint(-300, 300)
        self.y = random.randint(-200, 200)
        self.direction = random.randint(1, 360)
        self.vel = random.uniform(0.5, 3)
        self.rotation = random.randint(-5, 5)
        self.angle = 0
        self.size = random.randint(40, 100)
        self.image = pygame.transform.scale(asteroid_image, (self.size, self.size))
        self.orig_image = self.image
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):   
        self.x += self.vel * math.cos(math.radians(-self.direction))
        self.y += self.vel * math.sin(math.radians(-self.direction))
        self.x %= width
        self.y %= height
        self.angle += self.rotation
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
    def hit(self):
        self.kill()
        explosion_sound.play()
        asteroid = Asteroid()
        asteroid_sprites.add(asteroid)
        all_sprites.add(asteroid)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = 7
        self.direction = direction
        self.lifespan = min(width, height) // 2
        self.image = bullet_image
        self.rect = self.image.get_rect(right = ship.rect.w)

    def update(self):
        global score
        self.lifespan -= self.vel
        if self.lifespan < 0:
            self.kill()
        else:
            self.x += self.vel * math.cos(math.radians(-self.direction))
            self.y += self.vel * math.sin(math.radians(-self.direction))
            self.rect = self.image.get_rect(center = (
                self.x + ship.rect.w / 2 * math.cos(math.radians(-self.direction)),
                 self.y + ship.rect.h / 2 * math.sin(math.radians(-self.direction))))
            hitlist = pygame.sprite.spritecollide(self, asteroid_sprites, True, pygame.sprite.collide_mask)
            if hitlist:
                hitlist += pygame.sprite.spritecollide(self, asteroid_sprites, True, pygame.sprite.collide_mask)
                if hitlist:
                    for i in hitlist:
                        i.hit()
                    score +=1
                    self.kill()

def new_game():
    global all_sprites, asteroid_sprites, ship, asteroids
    ship = Ship()
    all_sprites = pygame.sprite.Group() 
    all_sprites.add(ship)

    asteroids = [Asteroid() for i in range (10)]
    asteroid_sprites = pygame.sprite.Group()
    asteroid_sprites.add(asteroids)
    all_sprites.add(asteroids)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    
    screen.blit(background, (0, 0))
    screen.blit(moving_background, (moving_background_x, 0))
    screen.blit(moving_background, (-width + moving_background_x, 0))
    moving_background_x += 1
    if moving_background_x == width:
        moving_background_x = 0
    if not game_started:
        screen.blit(splash, (width // 2 - 200, height // 2 - 150))
        thrust_sound.stop()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (width // 2 - 200) <= mouse_x <= (width // 2 + 200) \
                and (height // 2 - 150) <= mouse_y <= (height // 2 + 150):
                game_started = True
                game_over = False
                lives = 3
                score = 0
                new_game()
    elif game_started and game_over == False:
        all_sprites.update()
        all_sprites.draw(screen)
    text_lives = font.render("Lives: " + str(lives), True, (55, 255, 55))
    screen.blit(text_lives, (20, 20))
    text_score = font.render('Score: ' + str(score), True, (55, 255, 55))
    screen.blit(text_score, (width - 20 - text_score.get_width(), 20))
    pygame.display.update()
    clock.tick(FPS)
