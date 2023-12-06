import pygame
import constantes as c
from frame import *

pygame.init()


class Tetris:

    def __init__(self, window):
        self.win = window
        self.tela_altura = c.tela_altura
        self.tela_largura = c.tela_largura
        self.posicao_bloqueada = {}
        self.grid = criar_grid(self.posicao_bloqueada)

        self.mudar_bloco = False
        self.estado_bloqueado = False

        self.grupo_atual = get_blocos()
        self.proximo_grupo = get_blocos()
        self.blocos_index = 0
        self.bloco_pos = []
        self.proximo_index = 1
        self.bloco_atual = self.grupo_atual[self.blocos_index]
        self.proximo_bloco = self.grupo_atual[self.proximo_index]
        self.bloco_bloqueado = 0

        self.pico = 0
        self.coluna_topo = [0] * 10
        self.vazio = [0] * 10
        self.dif = [0] * 10

        self.linha = 0
        self.toda_linha = 0
        self.placar_pontos = c.placar_pontos
        self.placar = 0
        self.placar_atual = 0
        self.tempo_atraso = 0
        self.atraso_tempo = 200
        self.tempo_queda = 0
        self.velocidade_queda = 0
        self.nivel_tempo = 0
        self.ultimo_placar = maior_placar()
        self.nivel = 0
        self.tempo_movimentacao = 0
        self.velocidade_movimentacao = 0.03
        self.longo_click = {'down': False, 'left': False, 'right': False}
        self.aguardar_movimento = False
        self.terminar_movimento = False
        self.humano = False

    def queda(self, tempo):
        self.tempo_queda += tempo
        self.nivel_tempo += tempo
        if self.nivel_tempo / 1000 >= 10:
            nivel_tempo = 0
            if self.velocidade_queda > 0.15:
                self.velocidade_queda -= self.nivel

        if self.tempo_queda / 1000 >= self.velocidade_queda:
            self.tempo_queda = 0
            self.bloco_atual.y += 1
            if not (espaco_valido(self.bloco_atual, self.grid)) and self.bloco_atual.y > 0:
                self.bloco_atual.y -= 1
                if self.humano and not self.terminar_movimento:
                    self.aguardar_movimento = True

                if not self.aguardar_movimento:
                    self.mudar_bloco = True
                    self.terminar_movimento = False

    def eventos_movimento(self, evento):

        if evento == 'left':
            self.longo_click['left'] = True

            self.bloco_atual.x -= 1
            if not (espaco_valido(self.bloco_atual, self.grid)):
                self.bloco_atual.x += 1

        if evento == 'right':
            self.longo_click['right'] = True
            self.bloco_atual.x += 1
            if not (espaco_valido(self.bloco_atual, self.grid)):
                self.bloco_atual.x -= 1

        if evento == 'down':
            self.longo_click['down'] = True
            self.bloco_atual.y += 1
            if not (espaco_valido(self.bloco_atual, self.grid)):
                self.bloco_atual.y -= 1

        if evento == 'rotation_clock':
            self.bloco_atual.rotacao += 1

            if not (espaco_valido(self.bloco_atual, self.grid)):
                if not self.super_rotacao():
                    self.bloco_atual.rotacao -= 1

        if evento == 'rotation_cnclock':
            self.bloco_atual.rotacao -= 1

            if not (espaco_valido(self.bloco_atual, self.grid)):
                if not self.super_rotacao():
                    self.bloco_atual.rotacao += 1

        if evento == 'down_imd':
            self.bloco_atual.y += 1
            while espaco_valido(self.bloco_atual, self.grid) and self.bloco_atual.y > 0:
                self.bloco_atual.y += 1
            self.bloco_atual.y -= 1
            self.mudar_bloco = True

        if evento == 'hold':
            if self.bloco_bloqueado == 0:
                self.bloco_bloqueado = self.bloco_atual
                self.mudar_bloco = True
                self.estado_bloqueado = True

            else:
                self.bloco_bloqueado, self.bloco_atual = self.bloco_atual, self.bloco_bloqueado
                self.bloco_atual.x, self.bloco_atual.y = 5, 0

        if evento == 'left_kup':
            self.longo_click['left'] = False
            self.tempo_atraso = 0

        if evento == 'right_kup':
            self.longo_click['right'] = False
            self.tempo_atraso = 0

        if evento == 'down_kup':
            self.longo_click['down'] = False
            self.tempo_atraso = 0

    def pressionada(self, tempo):
        for evento in self.longo_click:
            if self.longo_click[evento]:
                self.tempo_movimentacao += tempo
                self.tempo_atraso += tempo
                if self.tempo_atraso >= self.atraso_tempo:
                    if self.tempo_movimentacao / 1000 >= self.velocidade_movimentacao:
                        self.tempo_movimentacao = 0
                        if evento == 'left':
                            self.bloco_atual.x -= 1
                            if not (espaco_valido(self.bloco_atual, self.grid)):
                                self.bloco_atual.x += 1

                        if evento == 'right':
                            self.bloco_atual.x += 1
                            if not (espaco_valido(self.bloco_atual, self.grid)):
                                self.bloco_atual.x -= 1

                        if evento == 'down':
                            self.bloco_atual.y += 1
                            if not (espaco_valido(self.bloco_atual, self.grid)):
                                self.bloco_atual.y -= 1

    def super_rotacao(self, rot=True):
        ind_s = self.bloco_atual.index
        if rot:
            ind_r = self.bloco_atual.rotacao + 1

        ind_r = ind_r % 4

        if ind_s == 3:
            dic_i = 'O'
        elif ind_s == 2:
            dic_i = 'I'
        else:
            dic_i = 'Other'

        for x in c.SRS_dic[dic_i][ind_r]:
            self.bloco_atual.x += x[0]
            self.bloco_atual.y += x[1]
            if not (espaco_valido(self.bloco_atual, self.grid)):
                self.bloco_atual.x -= x[0]
                self.bloco_atual.y -= x[1]
            else:
                return True
        return False

    def detectar(self):
        vazio = [0] * 10

        # pico = 0
        for i in range(20):
            for j in range(10):
                if self.grid[i][j] != (0, 0, 0):
                    if i < 19:
                        if self.grid[i + 1][j] == (0, 0, 0):
                            vazio[j] += 1
                    self.pico = max(self.pico, 20 - i)
                    self.coluna_topo[j] = max(self.coluna_topo[j], 20 - i)
        # vazio_net = vazio - self.vazio
        self.vazio = vazio
        for i in range(1, 10):
            self.dif[i] = self.coluna_topo[i] - self.coluna_topo[i - 1]

        self.min_altura = min(self.coluna_topo)

    def detectar_novo(grid):
        vazio = [0] * 10
        coluna_topo = [0] * 10
        dif = [0] * 10

        clear_row = []
        for i in range(20):
            for j in range(10):
                k = 1
                if grid[i][j] != (0, 0, 0) and j not in clear_row:
                    while i + k < 20:
                        if grid[i + k][j] == (0, 0, 0):
                            vazio[j] += 1
                        k += 1
                    clear_row.append(j)
                    # pico = max(pico, 20-i)
                    coluna_topo[j] = max(coluna_topo[j], 20 - i)
        # vazio_net = vazio - self.vazio

        for i in range(1, 10):
            dif[i] = abs(coluna_topo[i] - coluna_topo[i - 1])

        min_altura = min(coluna_topo)
        max_altura = max(coluna_topo)
        max_vazio = sum(vazio)
        max_dif = sum(dif)
        # print(vazio)

        return max_vazio, max_dif, max_altura, min_altura

    def pre_detectar(bloco, grid, bloqueado, proximo_estado=False, bloco2=0, pre_i=-1, pre_j=-1):
        pre_lista = []
        lista_atual = []

        win2 = 0
        for i in range(10):

            for j in range(4):
                newgame = Tetris(win2)
                newgame.bloco_atual.bloco = bloco.bloco
                newgame.grid = list(grid)
                newgame.posicao_bloqueada = dict(bloqueado)
                pre_bloco = newgame.bloco_atual
                pre_grid = newgame.grid
                pre_bloquado = newgame.posicao_bloqueada
                pre_bloco.x = i
                pre_bloco.rotacao = j % len(pre_bloco.bloco)
                if espaco_valido(pre_bloco, pre_grid):
                    if pre_bloco.y < 0:
                        pre_bloco.y += 3
                    while espaco_valido(pre_bloco, pre_grid):
                        pre_bloco.y += 1
                    pre_bloco.y -= 1
                    pre_pos = converte_formato_bloco(pre_bloco)
                    for pos in pre_pos:
                        p = (pos[0], pos[1])
                        pre_bloquado[p] = bloco.cor
                    pre_grid = criar_grid(pre_bloquado)
                    linha = limpar_linhas(pre_grid, pre_bloquado)
                    pre_grid = criar_grid(pre_bloquado)

                    if proximo_estado:
                        proxima_lista = Tetris.pre_detectar(bloco2, pre_grid, bloqueado, pre_i=i, pre_j=j)
                        pre_lista.append(proxima_lista)

                    else:
                        # coluna_topo,vazio,dif,max_altura,min_altura = Tetris.detectar_novo(pre_grid)
                        max_vazio, max_dif, max_altura, min_altura = Tetris.detectar_novo(pre_grid)
                        # lista_atual += coluna_topo + vazio + dif + [max_altura] + [min_altura] +[linha]
                        lista_atual += [max_vazio] + [max_dif] + [max_altura] + [min_altura] + [linha]
                        if pre_i != -1 and pre_j != -1:
                            lista_atual += [pre_i, pre_j]
                        else:
                            lista_atual += [i, j]
                        pre_lista.append(lista_atual)
                        # print(pre_pos)
                        lista_atual = []

        return pre_lista

    def test(bloco):
        bloco.y += 1

    def mudar(self):
        if self.mudar_bloco:
            if self.estado_bloqueado == False:
                for pos in self.bloco_pos:
                    p = (pos[0], pos[1])
                    self.posicao_bloqueada[p] = self.bloco_atual.cor

            self.estado_bloqueado = False

            self.grid = criar_grid(self.posicao_bloqueada)

            self.blocos_index = self.proximo_index
            self.proximo_index += 1
            if self.proximo_index == 7:
                self.grupo_atual = self.proximo_grupo
                self.proximo_grupo = get_blocos()

            self.proximo_index = self.proximo_index % 7

            # print(proximo_index)
            self.bloco_atual = self.proximo_bloco
            self.proximo_bloco = self.grupo_atual[self.proximo_index]
            self.mudar_bloco = False
            self.linha = limpar_linhas(self.grid, self.posicao_bloqueada)
            self.grid = criar_grid(self.posicao_bloqueada)
            self.detectar()
            # self.grid = create_grid(self.posicao_bloqueada)
            self.toda_linha += self.linha
            self.placar_atual = self.placar_pontos[self.linha]
            self.placar += self.placar_atual
            return True

    def desenhar(self):
        # self.bloco_pos = converte_formato_bloco(self.bloco_atual)
        desenhar_previsao(self.posicao_bloqueada, self.bloco_pos, self.grid)
        for i in range(len(self.bloco_pos)):
            x, y = self.bloco_pos[i]
            if y > -1:
                self.grid[y][x] = self.bloco_atual.cor

        # self.mudar()
        desenhar_janela(self.win, self.grid)
        desenhar_proximos_tetraminos(self.grupo_atual, self.proximo_grupo, self.win, 5, self.proximo_index)
        desenhar_guardar_bloco(self.win, self.bloco_bloqueado)
        desenhar_placar(self.win, self.placar, self.ultimo_placar)

    def derrota(self):
        if checar_perda(self.posicao_bloqueada):
            desenhar_texto_meio(self.win, 'Você perdeu!', 60, (255, 255, 255))

            atualizar_placar(self.placar)

    def reset(self):
        self.placar = 0
        self.posicao_bloqueada = {}
        self.grid = criar_grid(self.posicao_bloqueada)
        self.pico = 0
        self.coluna_topo = [0] * 10

    def loop(self, tempo):
        self.grid = criar_grid(self.posicao_bloqueada)
        # print(self.posicao_bloqueada)
        self.queda(tempo)

        # print(self.bloco_atual.y)
        self.bloco_pos = converte_formato_bloco(self.bloco_atual)

        mudar = self.mudar()
        if checar_perda(self.posicao_bloqueada):
            # draw_middle_text(self.win, 'Você perdeu!', 60, (255,255,255))

            atualizar_placar(self.placar)
        game_information = self.placar

        return game_information, checar_perda(self.posicao_bloqueada), mudar, self.placar_atual