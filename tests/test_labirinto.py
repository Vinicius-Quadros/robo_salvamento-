import unittest
import sys
import os
from unittest.mock import patch

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from labirinto import Labirinto
from robo import Robo

class TestLabirinto(unittest.TestCase):

    def setUp(self):
        # Caminho absoluto para 'mapa.txt' baseado no local deste arquivo
        mapa_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa.txt'))
        self.labirinto = Labirinto(mapa_path)

    def test_carregar_mapa(self):
        # Testa se o mapa é carregado corretamente
        self.assertEqual(self.labirinto.altura, 9)
        self.assertEqual(self.labirinto.largura, 7)
        self.assertIsNotNone(self.labirinto.posicao_entrada)
        self.assertIsNotNone(self.labirinto.posicao_humano)

    def test_is_valida(self):
        # Testa se a função de validação de posição funciona corretamente
        self.assertTrue(self.labirinto.is_valida((1, 1)))
        self.assertFalse(self.labirinto.is_valida((0, 0)))
        self.assertFalse(self.labirinto.is_valida((-1, 0)))  # Fora dos limites
        self.assertFalse(self.labirinto.is_valida((self.labirinto.altura, self.labirinto.largura)))  # Fora dos limites
        self.assertFalse(self.labirinto.is_valida((1, 0)))  # Posição de parede

    def test_is_dentro_dos_limites(self):
        # Testa a função que verifica se a posição está dentro dos limites do labirinto
        self.assertTrue(self.labirinto.is_dentro_dos_limites((0, 0)))
        self.assertFalse(self.labirinto.is_dentro_dos_limites((-1, 0)))  # Fora dos limites
        self.assertFalse(self.labirinto.is_dentro_dos_limites((self.labirinto.altura, 0)))  # Fora dos limites

    def test_is_saida(self):
        # Dicionário para mapear direções e posições de entrada correspondentes
        direcoes_entradas = {
            'N': (self.labirinto.altura - 1, self.labirinto.largura // 2),  # Entrada na base
            'S': (0, self.labirinto.largura // 2),  # Entrada no topo
            'E': (self.labirinto.altura // 2, 0),  # Entrada na esquerda
            'W': (self.labirinto.altura // 2, self.labirinto.largura - 1),  # Entrada na direita
        }

        # Dicionário para mapear direções opostas
        direcoes_opostas = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

        for direcao_inicial, posicao_entrada in direcoes_entradas.items():
            with self.subTest(direcao=direcao_inicial):
                # Cria um novo labirinto e robô para cada direção
                labirinto = Labirinto(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa.txt')))
                labirinto.posicao_entrada = posicao_entrada
                linha, coluna = posicao_entrada
                # Garante que a posição não é uma parede
                labirinto.mapa[linha][coluna] = ' '
                robo = Robo(labirinto)
                robo.posicao = posicao_entrada
                robo.direcao = direcao_inicial

                # Determina a direção de saída (oposta à direção inicial)
                direcao_saida = direcoes_opostas[direcao_inicial]

                # Testa se a posição é uma saída
                self.assertTrue(labirinto.is_saida(robo.posicao, direcao_saida))

                # Testa uma posição que não é saída
                self.assertFalse(labirinto.is_saida((1, 1), direcao_inicial))

        # Testa o bloco else com uma direção inválida
        with self.assertRaises(ValueError):
            self.labirinto.is_saida(self.labirinto.posicao_entrada, 'DirecaoInvalida')

    def test_is_saida_return_true_norte(self):
        # Robô na primeira linha olhando para o norte
        mapa_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa.txt'))
        labirinto = Labirinto(mapa_path)
        labirinto.posicao_entrada = (0, 3)
        labirinto.mapa[0][3] = ' '
        robo = Robo(labirinto)
        robo.posicao = (0, 3)
        robo.direcao = 'N'
        self.assertTrue(labirinto.is_saida(robo.posicao, robo.direcao))

    def test_is_saida_return_true_sul(self):
        # Robô na última linha olhando para o sul
        mapa_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa.txt'))
        labirinto = Labirinto(mapa_path)
        linha_max = labirinto.altura - 1
        labirinto.posicao_entrada = (linha_max, 3)
        labirinto.mapa[linha_max][3] = ' '
        robo = Robo(labirinto)
        robo.posicao = (linha_max, 3)
        robo.direcao = 'S'
        self.assertTrue(labirinto.is_saida(robo.posicao, robo.direcao))

    def test_is_saida_return_true_oeste(self):
        # Robô na primeira coluna olhando para o oeste
        mapa_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa.txt'))
        labirinto = Labirinto(mapa_path)
        labirinto.posicao_entrada = (4, 0)
        labirinto.mapa[4][0] = ' '
        robo = Robo(labirinto)
        robo.posicao = (4, 0)
        robo.direcao = 'W'
        self.assertTrue(labirinto.is_saida(robo.posicao, robo.direcao))

    def test_is_saida_return_true_leste(self):
        # Robô na última coluna olhando para o leste
        mapa_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa.txt'))
        labirinto = Labirinto(mapa_path)
        coluna_max = labirinto.largura - 1
        labirinto.posicao_entrada = (4, coluna_max)
        labirinto.mapa[4][coluna_max] = ' '
        robo = Robo(labirinto)
        robo.posicao = (4, coluna_max)
        robo.direcao = 'E'
        self.assertTrue(labirinto.is_saida(robo.posicao, robo.direcao))

    def test_encontrar_humano_sem_humano(self):
        # Testa o caso em que o humano não está presente no mapa
        labirinto_sem_humano = Labirinto('mapa_sem_humano.txt')
        self.assertIsNone(labirinto_sem_humano.encontrar_humano())  # Deve retornar None quando não há humano

    def test_encontrar_entrada_sem_entrada(self):
        # Testa o caso em que a entrada não está presente no mapa
        labirinto_sem_entrada = Labirinto('mapa_sem_entrada.txt')
        self.assertIsNone(labirinto_sem_entrada.encontrar_entrada())  # Deve retornar None quando não há entrada

    def test_exibir_mapa(self):
        # Testa a exibição do mapa para garantir que a função print é chamada corretamente
        with patch('builtins.print') as mocked_print:
            self.labirinto.exibir_mapa()
            self.assertTrue(mocked_print.called)

    def test_labirinto_vazio(self):
        # Caminho para o arquivo 'labirinto_vazio.txt' na raiz do projeto
        vazio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'labirinto_vazio.txt'))
        # Cria um arquivo vazio
        with open(vazio_path, 'w') as f:
            pass
        with self.assertRaises(ValueError):
            Labirinto(vazio_path)
        os.remove(vazio_path)

    def test_labirinto_corrompido(self):
        # Caminho para o arquivo 'mapa_corrompido.txt' na raiz do projeto
        corrompido_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa_corrompido.txt'))
        # Cria um mapa corrompido
        with open(corrompido_path, 'w') as f:
            f.write('E*H\n*')  # Linha com comprimento irregular
        with self.assertRaises(ValueError):
            Labirinto(corrompido_path)
        os.remove(corrompido_path)

if __name__ == '__main__':
    unittest.main()
