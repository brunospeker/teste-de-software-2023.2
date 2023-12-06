import pytest
from unittest.mock import MagicMock
import pygame
from frame import *
from game import *
from main import *

@pytest.fixture
def inicializar_pygame():
    pygame.init()

class TestTetris:
    def test_criar_grid(self, inicializar_pygame):
        grid = criar_grid({})
        assert isinstance(grid, list)

    def test_limpar_linhas(self, inicializar_pygame):
        grid = criar_grid({})
        bloqueado = {}
        linha = limpar_linhas(grid, bloqueado)
        assert isinstance(linha, int)

    def test_espaco_valido(self, inicializar_pygame):
        bloco = MagicMock()
        grid = criar_grid({})
        valido = espaco_valido(bloco, grid)
        assert isinstance(valido, bool)

    def tetris_instance():
        window_mock = MagicMock()
        tetris = Tetris(window_mock)
        return tetris

    def test_tetris_initialization(tetris_instance):
        assert tetris_instance.win is not None
        assert tetris_instance.tela_altura == c.tela_altura
        assert tetris_instance.tela_largura == c.tela_largura
        assert tetris_instance.posicao_bloqueada == {}
        # Fix: Use the correct attribute names
        assert tetris_instance.pico == 0
        assert tetris_instance.coluna_topo == [0] * 10

        # Add more assertions based on your initialization logic

    def test_tetris_queda(tetris_instance):
        # Mocking espaco_valido directly without using patch
        tetris_instance.espaco_valido = MagicMock(return_value=True)

        tetris_instance.queda(100)
        assert tetris_instance.tempo_queda == 100

        # Add more test cases for different scenarios

    def test_tetris_eventos_movimento(tetris_instance):
        # Mocking espaco_valido directly without using patch
        tetris_instance.espaco_valido = MagicMock(return_value=True)

        tetris_instance.eventos_movimento('left')
        assert tetris_instance.bloco_atual.x == 0

        # Add more test cases for different scenarios

    def test_tetris_pressionada(tetris_instance):
        tetris_instance.longo_click = {'left': True, 'right': False, 'down': False}
        tetris_instance.pressionada(200)
        assert tetris_instance.tempo_movimentacao == 200

        # Add more test cases for different scenarios

    def test_tetris_super_rotacao(tetris_instance):
        # Mocking espaco_valido directly without using patch
        tetris_instance.espaco_valido = MagicMock(return_value=True)

        result = tetris_instance.super_rotacao()
        assert result is True

        # Add more test cases for different scenarios

    def test_tetris_detectar(tetris_instance):
        # Mocking limpar_linhas directly without using patch
        tetris_instance.limpar_linhas = MagicMock(return_value=2)

        tetris_instance.detectar()
        assert tetris_instance.linha == 2

        # Add more test cases for different scenarios
