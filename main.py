import os
import pickle
import random
import time

import neat
import pygame

import constantes as c
from game import Tetris

import pytest
from testcase import *

shape_list = c.blocos


class tetris_game:

    def __init__(self, window):
        self.game = Tetris(window)
        self.bloco_atual = self.game.bloco_atual
        self.posicao_bloqueada = self.game.posicao_bloqueada
        self.proximo_bloco = self.game.proximo_bloco

    def jogador(self):

        clock = pygame.time.Clock()
        self.game.velocidade_queda = 0.3

        run = True
        while run:
            clock.tick(600)
            time1 = clock.get_rawtime()
            game_info, derrota, change, current_score = self.game.loop(time1)

            if derrota:
                self.game.reset()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    SystemExit

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.game.eventos_movimento('left')

                    if event.key == pygame.K_RIGHT:
                        self.game.eventos_movimento('right')

                    if event.key == pygame.K_DOWN:
                        self.game.eventos_movimento('down')

                    if event.key == pygame.K_UP:
                        self.game.eventos_movimento('rotation_clock')

                    if event.key == pygame.K_z:
                        self.game.eventos_movimento('rotation_cnclock')

                    if event.key == pygame.K_SPACE:
                        self.game.eventos_movimento('down_imd')

                    if event.key == pygame.K_c:
                        self.game.eventos_movimento('hold')

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT:
                        self.game.eventos_movimento('left_kup')

                    if event.key == pygame.K_RIGHT:
                        self.game.eventos_movimento('right_kup')

                    if event.key == pygame.K_DOWN:
                        self.game.eventos_movimento('down_kup')

            self.game.desenhar()

            time2 = clock.get_rawtime()
            self.game.pressionada(time2)

            pygame.display.update()

    def test_ai(self, winner_net):
        run = True
        clock = pygame.time.Clock()
        clock.tick(60)
        net = winner_net
        action = True

        self.game.velocidade_queda = 0

        max_score = 5000

        while run:
            time4 = clock.get_rawtime()
            game_info, derrota, change, current_score = self.game.loop(time4)
            if change:
                action = True

            if derrota:
                print(self.game.placar)

                self.game.reset()
                #break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
            if action:
                self.AI_move(net)
                action = False

            self.game.desenhar()

            pygame.display.update()

            pytest.main(['-v', 'testcase.py'])

    def AI_train(self, gen, config, desenhar=True):

        run = True

        start_time = time.time()
        clock = pygame.time.Clock()

        net = neat.nn.FeedForwardNetwork.create(gen, config)

        self.gen = gen
        self.game.velocidade_queda = 0
        action = True

        max_score = 10000000

        while run:
            time4 = clock.get_rawtime()
            # clock.tick(10)
            game_info, derrota, change, current_score = self.game.loop(time4)
            # print(self.game.bloco_atual.x)
            if change:
                action = True

            if derrota or self.game.placar > max_score:
                # self.game.desenhar()
                self.calculate_fitness(game_info, duration, current_score)
                self.game.reset()
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

            if action:
                self.AI_move(net)
                action = False

            if desenhar:
                self.game.desenhar()

            pygame.display.update()

            duration = time.time() - start_time

        return False

    def AI_move(self, net):

        output = [-99]
        output_list = []
        # action2 = [99,99]
        # x_lisy = []

        for x in Tetris.pre_detectar(self.game.bloco_atual, self.game.grid, self.game.posicao_bloqueada):
            output_new = net.activate(x[:5])
            if output_new[0] >= output[0]:
                action2 = x[5:]
                output = output_new
                # x_list = x


        if action2 != [99, 99]:
            x, rotacao = action2[0], action2[1]

            x_move = x - self.game.bloco_atual.x
            rot_move = rotacao - self.game.bloco_atual.rotacao

            for j_ in range(abs(rot_move)):

                if rot_move > 0:
                    self.game.eventos_movimento('rotation_clock')
                else:
                    self.game.eventos_movimento('rotation_cnclock')

            for i_ in range(abs(x_move)):

                if x_move > 0:
                    self.game.eventos_movimento('right')
                else:
                    self.game.eventos_movimento('left')

            self.game.eventos_movimento('down_imd')

    def calculate_fitness(self, game_info, duration, current_score):
        self.gen.fitness += game_info


def eval_gens(gens, config):
    width, height = 800, 700
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tetris')

    for i, (gem_id, gen) in enumerate(gens):

        gen.fitness = 0
        tetris = tetris_game(win)

        force_quit = tetris.AI_train(gen, config, desenhar=True)
        if force_quit:
            quit()

def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('test-1_allline_relu_check_point_128')

    p = neat.Population(config)
    p.config.fitness_threshold = 10000000
    #p.config.fitness_threshold = 100
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10, filename_prefix='test-1_allline_relu_check_point_'))

    #winner = p.run(eval_gens)
    winner = p.run(eval_gens, 10)
    with open("treinos/20-ia.pickle", "wb") as f:
        pickle.dump(winner, f)


def jogar_melhor_ia(config):
    with open("treinos/melhor-ia.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 800, 700
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tetris')
    tetris = tetris_game(win)
    tetris.test_ai(winner_net)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config1.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    largura, altura = c.tela_largura, c.tela_altura
    win = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Tetris')
    tetris = tetris_game(win)

    #Jogador normal
    #tetris.jogador()

    #Jogar com a IA
    jogar_melhor_ia(config)

    #Treinar a IA
    #run_neat(config)