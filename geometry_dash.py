import pygame
import sys
import math
import random

# Configuración
ANCHO, ALTO = 800, 400
FPS = 60
COLOR_FONDO = (30, 30, 40)
COLOR_SUELO = (60, 60, 80)
COLOR_CUBO = (0, 200, 255)
COLOR_OBSTACULO = (255, 80, 80)
COLOR_OBSTACULO2 = (255, 200, 0)
COLOR_OBSTACULO3 = (120, 255, 120)
COLOR_ITEM = (180, 0, 255)
COLOR_TEXTO = (255, 255, 255)
GRAVEDAD = 1
SALTO = -16
VELOCIDAD_INICIAL = 6

class Cubo:
    def __init__(self):
        self.rect = pygame.Rect(80, ALTO-100, 40, 40)
        self.vel_y = 0
        self.en_suelo = False
        self.vivo = True
        self.saltando = False
        self.angulo = 0
        self.gravedad_invertida = False

    def saltar(self):
        if self.en_suelo and not self.saltando:
            self.vel_y = -SALTO if self.gravedad_invertida else SALTO
            self.saltando = True

    def actualizar(self, obstaculos, gravedad, suelo_y, techo_y):
        self.vel_y += gravedad
        if self.vel_y > 16:
            self.vel_y = 16
        if self.vel_y < -16:
            self.vel_y = -16
        self.rect.y += int(self.vel_y)
        self.en_suelo = False
        if not self.gravedad_invertida:
            if self.rect.bottom >= suelo_y:
                self.rect.bottom = suelo_y
                self.vel_y = 0
                self.en_suelo = True
                self.angulo = 0
            else:
                self.angulo = (self.angulo + 12) % 360
        else:
            if self.rect.top <= techo_y:
                self.rect.top = techo_y
                self.vel_y = 0
                self.en_suelo = True
                self.angulo = 0
            else:
                self.angulo = (self.angulo + 12) % 360
        for obs in obstaculos:
            if self.rect.colliderect(obs):
                self.vivo = False

    def dibujar(self, screen):
        surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(surf, COLOR_CUBO, (0, 0, 40, 40), border_radius=8)
        rot = pygame.transform.rotate(surf, self.angulo)
        rect = rot.get_rect(center=self.rect.center)
        screen.blit(rot, rect)

class Obstaculo:
    def __init__(self, x, tipo=1, en_techo=False):
        self.tipo = tipo
        self.en_techo = en_techo
        if tipo == 1:
            if en_techo:
                self.rect = pygame.Rect(x, 0, 30, 60)
            else:
                self.rect = pygame.Rect(x, ALTO-80, 30, 60)
        elif tipo == 2:
            if en_techo:
                self.rect = pygame.Rect(x, 0, 60, 20)
            else:
                self.rect = pygame.Rect(x, ALTO-60, 60, 20)
        elif tipo == 3:
            if en_techo:
                self.rect = pygame.Rect(x, 0, 20, 100)
            else:
                self.rect = pygame.Rect(x, ALTO-100, 20, 100)
    def mover(self, velocidad):
        self.rect.x -= velocidad
    def fuera_pantalla(self):
        return self.rect.right < 0
    def dibujar(self, screen):
        if self.tipo == 1:
            pygame.draw.rect(screen, COLOR_OBSTACULO, self.rect, border_radius=6)
        elif self.tipo == 2:
            pygame.draw.rect(screen, COLOR_OBSTACULO2, self.rect, border_radius=10)
        elif self.tipo == 3:
            pygame.draw.rect(screen, COLOR_OBSTACULO3, self.rect, border_radius=2)

class ItemGravedad:
    def __init__(self, x):
        self.rect = pygame.Rect(x, ALTO//2-20, 30, 30)
        self.tiempo = 0
    def mover(self, velocidad):
        self.rect.x -= velocidad
    def fuera_pantalla(self):
        return self.rect.right < 0
    def dibujar(self, screen):
        pygame.draw.ellipse(screen, COLOR_ITEM, self.rect)
        pygame.draw.ellipse(screen, (255,255,255), self.rect, 2)

def dibujar_escenario(screen, cubo, obstaculos, items, score, gravedad_invertida):
    screen.fill(COLOR_FONDO)
    if not gravedad_invertida:
        pygame.draw.rect(screen, COLOR_SUELO, (0, ALTO-40, ANCHO, 40))
    else:
        pygame.draw.rect(screen, COLOR_SUELO, (0, 0, ANCHO, 40))
    cubo.dibujar(screen)
    for obs in obstaculos:
        obs.dibujar(screen)
    for item in items:
        item.dibujar(screen)
    font = pygame.font.SysFont('Arial', 28, bold=True)
    texto = font.render(f'Score: {score}', True, COLOR_TEXTO)
    screen.blit(texto, (10, 10))
    if gravedad_invertida:
        texto2 = font.render('¡Gravedad invertida!', True, (180,0,255))
        screen.blit(texto2, (ANCHO-260, 10))
    if not cubo.vivo:
        lose = font.render('¡Perdiste! Presiona R para reiniciar', True, (255, 180, 0))
        screen.blit(lose, (ANCHO//2 - lose.get_width()//2, ALTO//2 - 30))

def main():
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Geometry Dash - Clon Retro')
    clock = pygame.time.Clock()
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('tetris_theme.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print('No se pudo cargar la música:', e)
    def reiniciar():
        return Cubo(), [], [], 0, 0, VELOCIDAD_INICIAL, False
    cubo, obstaculos, items, score, frame, velocidad, gravedad_invertida = reiniciar()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and cubo.vivo:
                    cubo.saltar()
                if event.key == pygame.K_r and not cubo.vivo:
                    cubo, obstaculos, items, score, frame, velocidad, gravedad_invertida = reiniciar()
                if event.key == pygame.K_RIGHT:
                    velocidad = min(velocidad+1, 15)
                if event.key == pygame.K_LEFT:
                    velocidad = max(velocidad-1, 2)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    cubo.saltando = False
        if cubo.vivo:
            frame += 1
            # Obstáculos variados
            if frame % 60 == 0:
                tipo = 1
                if frame % 180 == 0:
                    tipo = 2
                elif frame % 300 == 0:
                    tipo = 3
                obs_techo = cubo.gravedad_invertida
                obstaculos.append(Obstaculo(ANCHO + 40, tipo, en_techo=obs_techo))
            # Item de gravedad
            if frame % 500 == 0:
                items.append(ItemGravedad(ANCHO + 100))
            for obs in obstaculos[:]:
                obs.mover(velocidad)
                if obs.fuera_pantalla():
                    obstaculos.remove(obs)
                    score += 1
            for item in items[:]:
                item.mover(velocidad)
                if item.fuera_pantalla():
                    items.remove(item)
                if cubo.rect.colliderect(item.rect):
                    cubo.gravedad_invertida = not cubo.gravedad_invertida
                    gravedad_invertida = cubo.gravedad_invertida
                    # Cambia la posición del cubo al invertir gravedad
                    if gravedad_invertida:
                        cubo.rect.bottom = 40
                    else:
                        cubo.rect.top = ALTO-100
                    items.remove(item)
            # Física según gravedad
            if cubo.gravedad_invertida:
                cubo.actualizar([o.rect for o in obstaculos], -GRAVEDAD, 40, 0)
            else:
                cubo.actualizar([o.rect for o in obstaculos], GRAVEDAD, ALTO-40, 0)
        dibujar_escenario(screen, cubo, obstaculos, items, score, gravedad_invertida)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
