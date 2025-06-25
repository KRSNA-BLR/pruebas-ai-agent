import pygame
import random
import os

# Configuración de la ventana
ANCHO = 300
ALTO = 600
TAM_BLOQUE = 30
COLUMNAS = ANCHO // TAM_BLOQUE
FILAS = ALTO // TAM_BLOQUE

# Colores
NEGRO = (0, 0, 0)
GRIS = (50, 50, 50)
BLANCO = (255, 255, 255)
AZUL = (0, 191, 255)
COLORES = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# Formas de las piezas (matrices 4x4)
PIEZAS = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],        # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]]   # Z
]

def crear_matriz():
    return [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

def colision(matriz, pieza, offset):
    off_x, off_y = offset
    for y, fila in enumerate(pieza):
        for x, celda in enumerate(fila):
            if celda:
                if (x + off_x < 0 or x + off_x >= COLUMNAS or y + off_y >= FILAS):
                    return True
                if y + off_y >= 0 and matriz[y + off_y][x + off_x]:
                    return True
    return False

def unir_pieza(matriz, pieza, offset, color):
    off_x, off_y = offset
    for y, fila in enumerate(pieza):
        for x, celda in enumerate(fila):
            if celda and y + off_y >= 0:
                matriz[y + off_y][x + off_x] = color

def eliminar_lineas(matriz):
    nuevas = [fila for fila in matriz if 0 in fila]
    lineas_eliminadas = FILAS - len(nuevas)
    for _ in range(lineas_eliminadas):
        nuevas.insert(0, [0 for _ in range(COLUMNAS)])
    return nuevas, lineas_eliminadas

def rotar(pieza):
    return [list(fila) for fila in zip(*pieza[::-1])]

class Tetris:
    def __init__(self):
        self.matriz = crear_matriz()
        self.nueva_pieza()
        self.puntaje = 0
        self.nivel = 1
        self.lineas = 0
        self.game_over = False

    def nueva_pieza(self):
        self.tipo = random.randint(0, len(PIEZAS) - 1)
        self.pieza = [fila[:] for fila in PIEZAS[self.tipo]]
        self.color = self.tipo + 1
        self.x = COLUMNAS // 2 - len(self.pieza[0]) // 2
        self.y = -len(self.pieza)
        if colision(self.matriz, self.pieza, (self.x, self.y)):
            self.game_over = True

    def mover(self, dx):
        if not colision(self.matriz, self.pieza, (self.x + dx, self.y)):
            self.x += dx

    def bajar(self):
        if not colision(self.matriz, self.pieza, (self.x, self.y + 1)):
            self.y += 1
        else:
            # Verificar si alguna parte de la pieza queda fuera del tablero al fijarla
            fuera = False
            for y, fila in enumerate(self.pieza):
                for x, celda in enumerate(fila):
                    if celda and self.y + y < 0:
                        fuera = True
            unir_pieza(self.matriz, self.pieza, (self.x, self.y), self.color)
            self.matriz, lineas = eliminar_lineas(self.matriz)
            self.puntaje += [0, 40, 100, 300, 1200][lineas] * self.nivel
            self.lineas += lineas
            self.nivel = 1 + self.lineas // 10
            if fuera:
                self.game_over = True
            else:
                self.nueva_pieza()

    def rotar(self):
        nueva = rotar(self.pieza)
        if not colision(self.matriz, nueva, (self.x, self.y)):
            self.pieza = nueva

    def caer(self):
        while not colision(self.matriz, self.pieza, (self.x, self.y + 1)):
            self.y += 1
        self.bajar()

def dibujar_tablero(screen, matriz, pieza, offset, color):
    for y, fila in enumerate(matriz):
        for x, celda in enumerate(fila):
            if celda:
                pygame.draw.rect(screen, COLORES[celda - 1], (x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE))
    if pieza:
        off_x, off_y = offset
        for y, fila in enumerate(pieza):
            for x, celda in enumerate(fila):
                if celda and y + off_y >= 0:
                    pygame.draw.rect(screen, COLORES[color - 1], ((x + off_x) * TAM_BLOQUE, (y + off_y) * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE))
    # Líneas de la cuadrícula
    for x in range(COLUMNAS):
        pygame.draw.line(screen, GRIS, (x * TAM_BLOQUE, 0), (x * TAM_BLOQUE, ALTO))
    for y in range(FILAS):
        pygame.draw.line(screen, GRIS, (0, y * TAM_BLOQUE), (ANCHO, y * TAM_BLOQUE))

def mostrar_texto(screen, texto, tam, color, x, y, centrado=True):
    font = pygame.font.SysFont('Arial', tam, bold=True)
    render = font.render(texto, True, color)
    rect = render.get_rect()
    if centrado:
        rect.center = (x, y)
        # Ajuste para que no se salga de la pantalla
        if rect.left < 0:
            rect.left = 0
        if rect.right > ANCHO:
            rect.right = ANCHO
        if rect.top < 0:
            rect.top = 0
        if rect.bottom > ALTO:
            rect.bottom = ALTO
    else:
        rect.topleft = (x, y)
        if rect.right > ANCHO:
            rect.right = ANCHO
        if rect.bottom > ALTO:
            rect.bottom = ALTO
    screen.blit(render, rect)

def menu_principal(screen):
    colores_titulo = [(0,191,255), (255,0,255), (255,255,0), (0,255,127), (255,69,0)]
    color_idx = 0
    anim = 0
    bloques = 8
    margen = (ANCHO - (bloques * 32 - 4)) // 2
    while True:
        screen.fill((20, 20, 30))
        color_titulo = colores_titulo[color_idx]
        mostrar_texto(screen, 'TETRIS', 70, color_titulo, ANCHO // 2, ALTO // 3)
        mostrar_texto(screen, 'Presiona', 30, (200, 200, 255), ANCHO // 2, ALTO // 2 - 25)
        mostrar_texto(screen, 'ENTER para', 30, (200, 200, 255), ANCHO // 2, ALTO // 2)
        mostrar_texto(screen, 'jugar', 30, (200, 200, 255), ANCHO // 2, ALTO // 2 + 25)
        mostrar_texto(screen, 'ESC para salir', 24, (180, 180, 180), ANCHO // 2, ALTO // 2 + 60)
        # Bloques superiores centrados
        for i in range(bloques):
            pygame.draw.rect(screen, COLORES[i % len(COLORES)], (margen + i*32, 40, 28, 28), border_radius=6)
        # Bloques inferiores centrados
        for i in range(bloques):
            pygame.draw.rect(screen, COLORES[(i+2) % len(COLORES)], (margen + i*32, ALTO-60, 28, 28), border_radius=6)
        pygame.display.flip()
        anim += 1
        if anim % 15 == 0:
            color_idx = (color_idx + 1) % len(colores_titulo)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def game_over_menu(screen, puntaje, record):
    while True:
        screen.fill(NEGRO)
        mostrar_texto(screen, 'GAME OVER', 44, (255, 0, 0), ANCHO // 2, ALTO // 3)
        mostrar_texto(screen, f'Puntaje: {puntaje}', 30, BLANCO, ANCHO // 2, ALTO // 2)
        mostrar_texto(screen, f'Record: {record}', 24, BLANCO, ANCHO // 2, ALTO // 2 + 40)
        mostrar_texto(screen, 'ENTER: Menú principal', 22, BLANCO, ANCHO // 2, ALTO // 2 + 90)
        mostrar_texto(screen, 'ESC: Salir', 22, BLANCO, ANCHO // 2, ALTO // 2 + 120)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def cargar_record():
    try:
        with open('tetris_record.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

def guardar_record(puntaje):
    with open('tetris_record.txt', 'w') as f:
        f.write(str(puntaje))

def main():
    pygame.init()
    # Música retro de fondo
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('tetris_theme.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Bucle infinito
    except Exception as e:
        print('No se pudo cargar la música:', e)
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Juego Tetris")
    clock = pygame.time.Clock()
    record = cargar_record()
    while True:
        menu_principal(screen)
        juego = Tetris()
        caida = pygame.USEREVENT + 1
        velocidad = 400
        pygame.time.set_timer(caida, velocidad)
        while not juego.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        juego.mover(-1)
                    elif event.key == pygame.K_RIGHT:
                        juego.mover(1)
                    elif event.key == pygame.K_DOWN:
                        juego.bajar()
                    elif event.key == pygame.K_UP:
                        juego.rotar()
                    elif event.key == pygame.K_SPACE:
                        juego.caer()
                if event.type == caida:
                    juego.bajar()
            # Ajustar velocidad según nivel
            nueva_vel = max(100, 400 - (juego.nivel - 1) * 30)
            if nueva_vel != velocidad:
                velocidad = nueva_vel
                pygame.time.set_timer(caida, velocidad)
            screen.fill(NEGRO)
            dibujar_tablero(screen, juego.matriz, juego.pieza, (juego.x, juego.y), juego.color)
            mostrar_texto(screen, f'Puntaje: {juego.puntaje}', 24, BLANCO, 10, 10, centrado=False)
            mostrar_texto(screen, f'Nivel: {juego.nivel}', 20, BLANCO, 10, 40, centrado=False)
            mostrar_texto(screen, f'Record: {record}', 20, BLANCO, 10, 70, centrado=False)
            pygame.display.flip()
            clock.tick(30)
        if juego.puntaje > record:
            record = juego.puntaje
            guardar_record(record)
        game_over_menu(screen, juego.puntaje, record)

if __name__ == "__main__":
    main()
