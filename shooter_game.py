from pygame import *
from random import randint
from time import time as timer


#música de fondo
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#fuentes y subtítulos
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)
win = font1.render("Ganaste!!", True, (255,255,255))
lose = font1.render("Perdiste..", True, (180,0,0))

#necesitamos las siguientes imágenes:
img_back = "galaxy.jpg" # fondo de juego
img_hero = "rocket.png" # héroe
img_enemy = "ufo.png" # enemigo
img_bullet = "bullet.png"
img_asteroid = "asteoride.png"

score = 0 #naves destruidas
lost = 0 #naves falladas
max_lost = 3
goal = 10
life = 5
#clase padre para los otros objetos
class GameSprite(sprite.Sprite):
 #constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Se llama al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)


       #cada objeto debe almacenar la propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


       #cada objeto debe tener la propiedad rect que representa el rectángulo en el que se encuentra
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #método de dibujo del personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#clase del jugador principal
class Player(GameSprite):
   #método para controlar el objeto con las flechas del teclado
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 #método para “disparar” (usar la posición del jugador para crear una bala)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#clase del objeto enemigo  
class Enemy(GameSprite):
   #movimiento del enemigo
    def update(self):
        self.rect.y += self.speed
        global lost
        #desaparece al llegar al borde de la pantalla
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#crea una ventana pequeña
win_width = 700
win_height = 500
display.set_caption("Tirador")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#crea objetos
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
for k in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
    

num_fire = 0
reload_time = False

reloads = font2.render("test", True, (255,0,0))

#la variable “juego terminado”: cuando sea True, los objetos dejan de funcionar en el ciclo principal
finish = False
#ciclo de juego principal:
run = True #la bandera es reiniciada con el botón de cerrar ventana
while run:
   #Evento de pulsado del botón “Cerrar”
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and reload_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and reload_time == False:
                    last_time = timer()
                    reload_time = True
        


    if not finish:
        
        #actualiza el fondo
        window.blit(background,(0,0))


        #escribe texto en la pantalla
        text = font2.render("Puntaje: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render("Fallados: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        #Movimientos del objeto
        ship.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        bullets.update()
        asteroids.update()

        #los actualiza en una nueva ubicación en cada iteración del ciclo
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        if reload_time == True:
            now_time = timer()
            if now_time - last_time <3:
                reload_font = font2.render("Recargando..", 1, (255,0,0))
                window.blit(reload_font,(260,460))
            else:
                num_fire = 0
                reload_time = False

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1
        if life <= 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            window.blit(win, (200,200))
            finish = True
        if life == 5:
            life_color = (0,150,0)
        if life == 3:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        tetx_life = font1.render(str(life),1,life_color)
        window.blit(tetx_life,(650,10))
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    else:
        finish = False
        score = 0
        lost = 0
        life = 5
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for j in range(1, 3):
            asteroid = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)
        
        



    display.update()
    #el ciclo se ejecuta cada 0.05 seg
    time.delay(50)