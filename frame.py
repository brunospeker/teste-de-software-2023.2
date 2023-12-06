import random

import pygame

import constantes as c

s_width = c.tela_largura
s_height = c.tela_altura
play_width = c.jogo_largura
play_height = c.jogo_altura

top_left_x = (s_width - play_width) // 2 #espaçamento horizontal
top_left_y = s_height - play_height      #espacamento vertical

score_dic = {0: 5, 1: 100, 2: 200, 3: 400, 4: 800}
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]


class tetramino(object):
    colunas = 5 #posicao coluna
    linhas = 0 #posicao linha

    def __init__(self, colunas, linhas, bloco):
        self.x = colunas
        self.y = linhas
        self.bloco = bloco
        self.cor = c.blocos_cores[c.blocos.index(bloco)]
        self.rotacao = 0
        self.index = c.blocos.index(bloco)


def criar_grid(posicao_bloqueada={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in posicao_bloqueada:
                c = posicao_bloqueada[(j, i)]
                grid[i][j] = c

    return grid


def get_bloco():
    return tetramino(5, 0, random.choice(c.blocos))

def get_blocos():
    group = []
    for x in grupo_atual():
        one_shape = tetramino(5, 0, c.blocos[x])
        group.append(one_shape)
    return group

def index_blocos(index):
    #possivelmente tirar esta função
    index = index % 7
    return index

def converte_formato_bloco(objeto_bloco):
    posicao = []
    formato = objeto_bloco.bloco[objeto_bloco.rotacao % len(objeto_bloco.bloco)]

    for i, linha in enumerate(formato):
        r = list(linha)
        for j, coluna in enumerate(r):
            if coluna == '0':
                posicao.append((objeto_bloco.x + j, objeto_bloco.y + i))

    for i, pos in enumerate(posicao):
        posicao[i] = (pos[0] - 2, pos[1] - 4)

    return posicao


def espaco_valido(bloco, grid):
    posicao_aceita = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    posicao_aceita = [j for sub in posicao_aceita for j in sub]
    # print(accepted_pos)

    formatado = converte_formato_bloco(bloco)

    for pos in formatado:
        if pos not in posicao_aceita:
            if pos[1] > -1 or pos[0] >= 10 or pos[0] < 0:
                # print('alert')
                return False
    return True


def checar_perda(posicoes):
    for pos in posicoes:
        x, y = pos
        if y < 1:
            return True

    return False


def grupo_atual():
    grupo = [i for i in range(7)]

    aleatorio = random.sample(grupo, 7)

    return aleatorio

def desenhar_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * c.bloco_tamanho), (sx + play_width, sy + i * c.bloco_tamanho))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * c.bloco_tamanho, sy),
                             (sx + j * c.bloco_tamanho, sy + play_height))


def limpar_linhas(grid, bloqueado):
    inc = 0
    ind = []
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind.append(i)
            for j in range(len(row)):
                try:
                    del bloqueado[(j, i)]
                except:
                    continue
    if inc > 0:
        for i in range(len(ind)):
            for chave in sorted(list(bloqueado), key=lambda x: x[1])[::-1]:
                x, y = chave
                if y < ind[i] + i:
                    novaChave = (x, y + 1)
                    bloqueado[novaChave] = bloqueado.pop(chave)

    return inc


def desenhar_tetraminos(numero, formato, surface, cor, x, y):
    novo_tamanho_bloco = c.bloco_tamanho * 0.9
    for a in range(numero):

        for i, linha in enumerate(formato):
            r = list(linha)
            for j, coluna in enumerate(r):
                if coluna == '0':
                    pygame.draw.rect(surface, cor,
                                     (x + j * novo_tamanho_bloco, y + i * novo_tamanho_bloco, novo_tamanho_bloco, novo_tamanho_bloco), 0)
                    pygame.draw.line(surface, (0, 0, 0), (x + j * novo_tamanho_bloco, y + i * novo_tamanho_bloco),
                                     (x + j * novo_tamanho_bloco + novo_tamanho_bloco, y + i * novo_tamanho_bloco))
                    pygame.draw.line(surface, (0, 0, 0), (x + j * novo_tamanho_bloco, y + i * novo_tamanho_bloco),
                                     (x + j * novo_tamanho_bloco, y + i * novo_tamanho_bloco + novo_tamanho_bloco))

        y += 100


def desenhar_proximos_tetraminos(grupo_atual, proximo_grupo, surface, numero, next_index):

    proximos_rect = pygame.Rect(580, 20, 200, 660)
    pygame.draw.rect(surface, (0, 120, 162), proximos_rect, 0, 10)

    font = pygame.font.SysFont('Times New Roman', 20)
    label = font.render('PRÓXIMAS PEÇAS', 1, (0, 0, 0))

    text_width, text_height = font.size('PRÓXIMAS PEÇAS')

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 300

    y = sy

    text_x = proximos_rect.x + (proximos_rect.width - text_width) // 2


    for i in range(numero):
        objeto_bloco = grupo_atual[next_index]
        formato = objeto_bloco.bloco[objeto_bloco.rotacao % len(objeto_bloco.bloco)]
        desenhar_tetraminos(1, formato, surface, objeto_bloco.cor, sx, y)
        y += 110

        next_index += 1
        if next_index == 7:
            grupo_atual = proximo_grupo
            next_index = 0


    surface.blit(label, (text_x , 40))


def desenhar_guardar_bloco(surface, guardar_bloco):

    guardar_rect = pygame.Rect(20, 320, 200, 200)
    pygame.draw.rect(surface, (0, 120, 162), guardar_rect, 0, 10)

    font = pygame.font.SysFont('Times New Roman', 20)
    label = font.render('GUARDAR', 1, (0, 0, 0))

    text_width, text_height = font.size('GUARDAR')

    text_x = guardar_rect.x + (guardar_rect.width - text_width) // 2
    text_y = guardar_rect.y + (guardar_rect.height - text_height) // 2

    if guardar_bloco != 0:
        objeto_bloco = guardar_bloco

        formato = objeto_bloco.bloco[objeto_bloco.rotacao % len(objeto_bloco.bloco)]

        objeto_width = len(formato[0]) * 30
        objeto_height = len(formato) * 30

        objeto_x = guardar_rect.x + (guardar_rect.width - objeto_width) // 2
        objeto_y = guardar_rect.y + (guardar_rect.height - objeto_height) // 2

        #desenhar_tetraminos(1, formato, surface, objeto_bloco.cor, 60, 420)
        desenhar_tetraminos(1, formato, surface, objeto_bloco.cor, objeto_x, objeto_y+20)

    surface.blit(label, (text_x, 350))

    imagem_path = "img/Logo_UFF.png"
    imagem = pygame.image.load(imagem_path)
    imagem = pygame.transform.scale(imagem, (100, 50))

    surface.blit(imagem, (60, 620))


def desenhar_placar(surface, placar, ultimo_placar):

    placar_rect = pygame.Rect(20, 20, 200, 100)
    pygame.draw.rect(surface, (0, 120, 162), placar_rect, 0, 10)

    font = pygame.font.SysFont('Times New Roman', 20)
    label = font.render('Placar:' + str(placar), 1, (0, 0, 0))

    surface.blit(label, (40, 40))

    font = pygame.font.SysFont('Times New Roman', 20)
    label1 = font.render('Maior Placar:' + str(ultimo_placar), 1, (0, 0, 0))

    surface.blit(label1, (40, 80))

def desenhar_texto_meio(surface, texto, tamanho, cor):
    font = pygame.font.SysFont('Times New Roman', tamanho, bold=True)
    label = font.render(texto, 1, cor)

    surface.blit(label, (
    top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))


def atualizar_placar(nplacar):
    placar = maior_placar()

    with open('score.txt', 'w') as f:
        f.write(str(max(int(placar), nplacar)))


def maior_placar():
    try:
        with open('score.txt', 'r') as f:
            linhas = f.readlines()
            placar = linhas[0].strip()
            # print(score)
    except:
        placar = 0

    return placar


def desenhar_previsao(bloqueado, posicao, grid):
    registro = []
    nova_posicao = []
    for a in posicao:
        temp = []
        for c in a:
            temp.append(c)
        nova_posicao.append(temp)

    for i in range(len(nova_posicao)):
        x, y = nova_posicao[i][0], posicao[i][1]
        while (x, y) not in bloqueado and y < 20:
            y += 1

        y -= 1

        registro.append(y - posicao[i][1])

    down = min(registro)
    for i in range(len(nova_posicao)):
        x, y = nova_posicao[i][0], posicao[i][1] + down
        # print(x,y)
        if y > -1 and y < 20 and x >= 0 and x < 10:
            grid[y][x] = (70, 70, 70, 240)


def desenhar_janela(surface, grid):
    surface.fill((241, 243, 255))

    font = pygame.font.SysFont('Times New Roman', 60)
    label = font.render('TETRIS', 1, (12, 72, 117))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 25))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    pygame.draw.rect(surface, (0, 53, 71), (top_left_x, top_left_y, play_width, play_height), 6)

    desenhar_grid(surface, grid)
    # pygame.display.update()