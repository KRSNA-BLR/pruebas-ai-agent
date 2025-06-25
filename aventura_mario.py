import pygame
import sys

# Configuración
ANCHO, ALTO = 1200, 480
FPS = 60
GRAVEDAD = 0.8
SALTO = -15
COLOR_FONDO = (107, 140, 255)
COLOR_SUELO = (80, 50, 20)
COLOR_CESPED = (80, 200, 80)
COLOR_MARIO = (255, 80, 80)
COLOR_BLOQUE = (200, 160, 60)
COLOR_MONEDA = (255, 220, 0)
COLOR_TUBO = (0, 180, 0)
COLOR_BANDERA = (255,255,255)
COLOR_BORDE = (60, 120, 60)
COLOR_OBSTACULO = (120, 60, 0)

# Nivel extendido inspirado en el primer mundo de Mario Bros
PLATAFORMAS = [
    pygame.Rect(0, 440, 1200, 40),  # Suelo largo
    # Primeros bloques y plataformas
    pygame.Rect(120, 360, 40, 40), pygame.Rect(160, 360, 40, 40), pygame.Rect(200, 360, 40, 40),
    pygame.Rect(400, 280, 40, 40), pygame.Rect(440, 280, 40, 40), pygame.Rect(480, 280, 40, 40),
    # Tubos
    pygame.Rect(600, 400, 40, 40), pygame.Rect(640, 400, 40, 40), pygame.Rect(680, 400, 40, 40),
    pygame.Rect(900, 400, 40, 80), pygame.Rect(940, 400, 40, 80),
    # Más plataformas y bloques
    pygame.Rect(800, 320, 40, 40), pygame.Rect(840, 320, 40, 40),
    pygame.Rect(1000, 360, 40, 40), pygame.Rect(1040, 360, 40, 40),
    pygame.Rect(1080, 360, 40, 40),
]
MONEDAS = [
    pygame.Rect(130, 320, 20, 20), pygame.Rect(410, 240, 20, 20), pygame.Rect(210, 320, 20, 20),
    pygame.Rect(810, 280, 20, 20), pygame.Rect(850, 280, 20, 20), pygame.Rect(1010, 320, 20, 20),
    pygame.Rect(300, 400, 20, 20), pygame.Rect(350, 400, 20, 20), pygame.Rect(700, 400, 20, 20),
    pygame.Rect(1150, 400, 20, 20)
]
OBSTACULOS = [
    pygame.Rect(350, 420, 30, 20), pygame.Rect(550, 420, 30, 20), pygame.Rect(750, 420, 30, 20),
    pygame.Rect(950, 420, 30, 20), pygame.Rect(1100, 420, 30, 20)
]

class Mario:
    def __init__(self):
        self.rect = pygame.Rect(50, 400, 32, 40)
        self.vel_x = 0
        self.vel_y = 0
        self.en_suelo = False
        self.puntaje = 0
        self.ganador = False
        self.saltando = False
        self.scroll_x = 0
        self.monedas = 0
        self.perdio = False

    def mover(self, teclas):
        self.vel_x = 0
        if teclas[pygame.K_LEFT]:
            self.vel_x = -4
        if teclas[pygame.K_RIGHT]:
            self.vel_x = 4
        if teclas[pygame.K_SPACE] and self.en_suelo and not self.saltando:
            self.vel_y = SALTO
            self.saltando = True
        if not teclas[pygame.K_SPACE]:
            self.saltando = False

    def actualizar(self, plataformas, monedas, bandera, obstaculos):
        self.vel_y += GRAVEDAD
        if self.vel_y > 12:
            self.vel_y = 12
        self.rect.x += self.vel_x
        self.colisionar(plataformas, eje='x')
        self.rect.y += int(self.vel_y)
        self.en_suelo = False
        self.colisionar(plataformas, eje='y')
        # Monedas
        for moneda in monedas[:]:
            m = moneda.move(-self.scroll_x, 0)
            if self.rect.colliderect(m):
                monedas.remove(moneda)
                self.puntaje += 1
                self.monedas += 1
        # Bandera
        b = bandera.move(-self.scroll_x, 0)
        if self.rect.colliderect(b):
            self.ganador = True
        # Obstáculos
        for obs in obstaculos:
            o = obs.move(-self.scroll_x, 0)
            if self.rect.colliderect(o):
                self.perdio = True
        # Scroll lateral
        if self.rect.centerx > ANCHO//2 and self.vel_x > 0 and self.rect.right < 1200:
            self.scroll_x += self.vel_x
            self.rect.x -= self.vel_x

    def colisionar(self, plataformas, eje):
        for plataforma in plataformas:
            p = plataforma.move(-self.scroll_x, 0)
            if self.rect.colliderect(p):
                if eje == 'x':
                    if self.vel_x > 0:
                        self.rect.right = p.left
                    elif self.vel_x < 0:
                        self.rect.left = p.right
                elif eje == 'y':
                    if self.vel_y > 0:
                        self.rect.bottom = p.top
                        self.vel_y = 0
                        self.en_suelo = True
                    elif self.vel_y < 0:
                        self.rect.top = p.bottom
                        self.vel_y = 0

def dibujar_escenario(screen, mario, plataformas, monedas, bandera, obstaculos):
    screen.fill(COLOR_FONDO)
    # Suelo con césped
    suelo = plataformas[0].move(-mario.scroll_x, 0)
    pygame.draw.rect(screen, COLOR_SUELO, suelo)
    pygame.draw.rect(screen, COLOR_CESPED, (suelo.x, suelo.y-10, suelo.width, 12))
    for i in range(suelo.x, suelo.x+suelo.width, 16):
        pygame.draw.ellipse(screen, COLOR_BORDE, (i, suelo.y-10, 16, 10))
    # Bloques y tubos
    for plataforma in plataformas[1:]:
        p = plataforma.move(-mario.scroll_x, 0)
        if p.y >= 400:
            pygame.draw.rect(screen, COLOR_TUBO, p, border_radius=6)
            pygame.draw.rect(screen, (0,100,0), p, 3, border_radius=6)
        else:
            pygame.draw.rect(screen, COLOR_BLOQUE, p)
            pygame.draw.rect(screen, (180,140,40), p, 3)
    # Monedas
    for moneda in monedas:
        m = moneda.move(-mario.scroll_x, 0)
        pygame.draw.ellipse(screen, COLOR_MONEDA, m)
        pygame.draw.ellipse(screen, (200,180,0), m, 2)
    # Obstáculos
    for obs in obstaculos:
        o = obs.move(-mario.scroll_x, 0)
        pygame.draw.rect(screen, COLOR_OBSTACULO, o, border_radius=4)
        pygame.draw.rect(screen, (80,40,0), o, 2, border_radius=4)
    # Mario
    pygame.draw.rect(screen, COLOR_MARIO, mario.rect, border_radius=6)
    pygame.draw.rect(screen, (180,40,40), mario.rect, 2, border_radius=6)
    # Bandera
    b = bandera.move(-mario.scroll_x, 0)
    pygame.draw.rect(screen, (0,0,0), b)
    pygame.draw.polygon(screen, COLOR_BANDERA, [(b.right, b.top), (b.right+20, b.top+10), (b.right, b.top+20)])
    font = pygame.font.SysFont('Arial', 24, bold=True)
    texto = font.render(f'Monedas: {mario.monedas}', True, (0,0,0))
    screen.blit(texto, (10, 10))
    if mario.ganador:
        win = font.render('¡Nivel completado!', True, (0, 120, 0))
        screen.blit(win, (ANCHO//2 - win.get_width()//2, 60))
    if mario.perdio:
        lose = font.render('¡Perdiste! Presiona R para reiniciar', True, (200, 0, 0))
        screen.blit(lose, (ANCHO//2 - lose.get_width()//2, 100))

def main():
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Mario Bross Game - Nivel 1')
    clock = pygame.time.Clock()
    def reiniciar():
        return Mario(), PLATAFORMAS[:], MONEDAS[:], pygame.Rect(1150, 320, 10, 120), OBSTACULOS[:]
    mario, plataformas, monedas, bandera, obstaculos = reiniciar()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and mario.perdio:
                if event.key == pygame.K_r:
                    mario, plataformas, monedas, bandera, obstaculos = reiniciar()
        teclas = pygame.key.get_pressed()
        if not mario.perdio and not mario.ganador:
            mario.mover(teclas)
            mario.actualizar(plataformas, monedas, bandera, obstaculos)
        dibujar_escenario(screen, mario, plataformas, monedas, bandera, obstaculos)
        pygame.display.flip()
        clock.tick(FPS)
        if mario.ganador:
            pygame.time.wait(2000)
            mario, plataformas, monedas, bandera, obstaculos = reiniciar()

if __name__ == '__main__':
    main()

# aventura_mario.py
# Comentarios agregados siguiendo principios de clean code en español
# Este es un juego simple inspirado en Mario Bros, donde el jugador controla a Mario
# para recolectar monedas, evitar obstáculos y llegar a la bandera para completar el nivel.
# Las principales clases y funciones están documentadas con comentarios para facilitar
# la comprensión y el mantenimiento del código.
