import unittest
import sys
import os
from unittest.mock import patch

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from labirinto import Labirinto
from robo import Robo

class TestRobo(unittest.TestCase):

    def setUp(self):
        mapa_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mapa.txt'))
        self.labirinto = Labirinto(mapa_path)
        self.robo = Robo(self.labirinto)


    def test_direcao_inicial(self):
        # Testa a direção inicial do robô
        self.assertEqual(self.robo.direcao, 'S')

    def test_direcao_labirinto_diferentes_entradas(self):
        # Testa a direção inicial do robô com diferentes posições de entrada
        entradas_direcoes = {
            (0, 3): 'S',  # Entrada no topo
            (8, 3): 'N',  # Entrada na parte inferior
            (4, 0): 'E',  # Entrada na esquerda
            (4, 6): 'W',  # Entrada na direita
        }
        for pos_entrada, direcao_esperada in entradas_direcoes.items():
            self.labirinto.posicao_entrada = pos_entrada
            direcao = self.robo.direcao_labirinto(pos_entrada)
            self.assertEqual(direcao, direcao_esperada)

    def test_avancar(self):
        # Configura o robô para avançar para uma posição válida
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertTrue(self.robo.avancar())
        self.assertEqual(self.robo.posicao, (2, 1))
        # Testa avançar contra uma parede
        self.robo.direcao = 'W'
        self.assertFalse(self.robo.avancar())

    def test_girar(self):
        direcoes = ['N', 'E', 'S', 'W']
        self.robo.direcao = 'N'
        for direcao_esperada in direcoes[1:] + ['N']:
            self.robo.girar()
            self.assertEqual(self.robo.direcao, direcao_esperada)

    def test_pegar_humano(self):
        self.robo.posicao = (self.labirinto.posicao_humano[0] - 1, self.labirinto.posicao_humano[1])
        self.robo.direcao = 'S'  # Olhando para o humano
        self.assertTrue(self.robo.pegar_humano())
        self.assertTrue(self.robo.com_humano)
        self.assertIsNone(self.labirinto.posicao_humano)
        self.assertFalse(self.robo.pegar_humano())

    def test_pegar_humano_sem_humano(self):
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertFalse(self.robo.pegar_humano())
        # Verifica se o alarme foi registrado
        self.assertIn("Alarme: Tentativa de coleta sem humano a frente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_sensor_frente(self):
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertEqual(self.robo.sensor_frente(), 'VAZIO')
        self.labirinto.mapa[2][1] = '*'  # Coloca uma parede à frente
        self.assertEqual(self.robo.sensor_frente(), 'PAREDE')

    def test_sensor_esquerda(self):
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertEqual(self.robo.sensor_esquerda(), 'VAZIO')

    def test_sensor_direita(self):
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertEqual(self.robo.sensor_direita(), 'PAREDE')

    def test_bfs(self):
        caminho = self.robo.bfs(self.robo.posicao, self.labirinto.posicao_humano)
        self.assertIsNotNone(caminho)
        self.assertTrue(len(caminho) > 0)

    def test_bfs_sem_caminho(self):
        self.labirinto.mapa[2][1] = '*'
        self.labirinto.mapa[1][2] = '*'
        self.labirinto.mapa[1][0] = '*'
        caminho = self.robo.bfs(self.robo.posicao, self.labirinto.posicao_humano)
        self.assertIsNone(caminho)

    def test_executar_missao(self):
        self.robo.executar_missao()
        self.assertFalse(self.robo.com_humano)

    def test_missao_falha(self):
        self.labirinto.mapa[self.labirinto.posicao_humano[0]][self.labirinto.posicao_humano[1]-1] = '*'
        self.labirinto.mapa[self.labirinto.posicao_humano[0]][self.labirinto.posicao_humano[1]+1] = '*'
        self.labirinto.mapa[self.labirinto.posicao_humano[0]-1][self.labirinto.posicao_humano[1]] = '*'
        self.labirinto.mapa[self.labirinto.posicao_humano[0]+1][self.labirinto.posicao_humano[1]] = '*'
        self.robo.executar_missao()

        mensagens_log = [log[0] for log in self.robo.logs if isinstance(log, list) and len(log) > 0]
        self.assertIn("Missao falhou: Caminho nao encontrado", mensagens_log)

    def test_gerar_log_csv(self):
        self.robo.executar_missao()
        nome_arquivo = 'log_robo_test.csv'
        self.robo.gerar_log_csv(nome_arquivo)
        with open(nome_arquivo, 'r') as file:
            lines = file.readlines()
        self.assertGreater(len(lines), 1)
        os.remove(nome_arquivo)

    def test_condicoes_adicionais(self):
        self.robo.posicao = (0, 0)  # Testa uma posição limite
        self.assertFalse(self.robo.avancar())  # Testa avanço em posição inválida
        self.robo.direcao = 'N'
        self.robo.girar()
        self.assertEqual(self.robo.direcao, 'E')  # Verifica o giro

    def test_excecoes(self):
        # Testa uma situação em que uma exceção deve ser lançada
        with self.assertRaises(ValueError):
            self.robo.direcao_labirinto((-1, -1))  # Simula uma entrada inválida

    def test_alarme_colisao_parede(self):
        self.robo.posicao = (1, 1)  # Suponha que (1, 1) esteja livre
        self.labirinto.mapa[2][1] = '*'  # Coloca uma parede à frente
        self.robo.direcao = 'S'
        self.robo.avancar()
        self.assertIn("Alarme: Colisão com parede!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_alarme_atropelamento_humano(self):
        self.robo.posicao = (1, 1)
        self.labirinto.mapa[2][1] = 'H'  # Coloca um humano à frente
        self.robo.direcao = 'S'
        self.robo.avancar()
        self.assertIn("Alarme: Atropelamento de humano!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_alarme_beco_sem_saida(self):
        self.robo.com_humano = True
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = '*'
        self.labirinto.mapa[1][0] = '*'
        self.labirinto.mapa[1][2] = '*'

        self.robo.verificar_beco_sem_saida()
        self.assertIn("Alarme: Beco sem saída após coleta do humano!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_alarme_ejecao_sem_humano(self):
        self.robo.com_humano = False
        self.robo.registrar_ejecao()
        self.assertIn("Alarme: Tentativa de ejeção sem humano presente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_alarme_coleta_sem_humano(self):
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = ' '
        self.robo.pegar_humano()
        self.assertIn("Alarme: Tentativa de coleta sem humano a frente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_atualizar_posicao_humano(self):
        self.robo.posicao = (self.labirinto.posicao_humano[0] - 1, self.labirinto.posicao_humano[1])
        self.robo.direcao = 'S'
        self.robo.pegar_humano()
        self.assertIsNone(self.labirinto.posicao_humano)
        self.assertEqual(self.labirinto.mapa[self.robo.posicao[0]+1][self.robo.posicao[1]], 'VAZIO')

    def test_direcao_para_posicao(self):
        self.robo.posicao = (2, 2)
        pos_alvo = (2, 3)
        direcao = self.robo.direcao_para_posicao(pos_alvo)
        self.assertEqual(direcao, 'E')

        pos_alvo = (1, 2)
        direcao = self.robo.direcao_para_posicao(pos_alvo)
        self.assertEqual(direcao, 'N')

    def test_seguir_caminho(self):
        self.robo.caminho = [(1, 1), (1, 2)]
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'E'
        self.robo.seguir_caminho()
        self.assertEqual(self.robo.posicao, (1, 2))

    def test_registrar_log(self):
        # Testa se os logs são registrados corretamente, incluindo alarmes
        self.robo.posicao = (2, 2)
        self.robo.direcao = 'E'
        self.robo.avancar()  # Tentativa de avançar para (2, 3), mas há uma parede
        self.robo.girar()  # Vira para o sul
        self.robo.avancar()  # Avança para (3, 2)
        self.assertEqual(len(self.robo.logs), 4)
        comandos = [log[0] for log in self.robo.logs if isinstance(log, list) and len(log) > 0]
        self.assertEqual(comandos, ['LIGAR', 'Alarme: Colisão com parede!', 'G', 'A'])

    def test_analisar_posicao(self):
        self.assertEqual(self.robo.analisar_posicao((1, 1)), 'VAZIO')
        self.labirinto.mapa[1][1] = '*'
        self.assertEqual(self.robo.analisar_posicao((1, 1)), 'PAREDE')
        self.labirinto.mapa[1][1] = 'H'
        self.assertEqual(self.robo.analisar_posicao((1, 1)), 'HUMANO')

    def test_frente(self):
        self.robo.posicao = (2, 2)
        self.robo.direcao = 'N'
        self.assertEqual(self.robo.frente(), (1, 2))
        self.robo.direcao = 'S'
        self.assertEqual(self.robo.frente(), (3, 2))
        self.robo.direcao = 'E'
        self.assertEqual(self.robo.frente(), (2, 3))
        self.robo.direcao = 'W'
        self.assertEqual(self.robo.frente(), (2, 1))

    def test_esta_proximo_ao_humano(self):
        self.robo.posicao = (self.labirinto.posicao_humano[0], self.labirinto.posicao_humano[1] -1)
        self.assertTrue(self.robo.esta_proximo_ao_humano())
        self.robo.posicao = (self.labirinto.posicao_humano[0] -2, self.labirinto.posicao_humano[1])
        self.assertFalse(self.robo.esta_proximo_ao_humano())

    def test_verificar_ejecao_sem_humano(self):
        self.robo.com_humano = False
        self.assertTrue(self.robo.verificar_ejecao_sem_humano())
        self.assertIn("Alarme: Tentativa de ejeção sem humano presente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_verificar_coleta_sem_humano(self):
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = ' '
        self.robo.pegar_humano()
        self.assertIn("Alarme: Tentativa de coleta sem humano a frente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_verificar_beco_sem_saida(self):
        self.robo.com_humano = True
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = '*'
        self.labirinto.mapa[1][0] = '*'
        self.labirinto.mapa[1][2] = '*'
        self.assertTrue(self.robo.verificar_beco_sem_saida())
        self.assertIn("Alarme: Beco sem saída após coleta do humano!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_pegar_humano_lateral_direita(self):
        self.labirinto.posicao_humano = (2, 2)
        self.labirinto.mapa[2][2] = 'H'
        self.robo.posicao = (2, 1)
        self.robo.direcao = 'N'  # Robô olhando para o norte
        self.assertTrue(self.robo.pegar_humano())
        self.assertTrue(self.robo.com_humano)
        self.assertEqual(self.robo.direcao, 'E')  # O robô deve ter girado para o leste
        # Verifica se o humano foi removido do mapa
        self.assertIsNone(self.labirinto.posicao_humano)
        self.assertEqual(self.labirinto.mapa[2][2], 'VAZIO')

    def test_pegar_humano_lateral_esquerda(self):
        self.labirinto.posicao_humano = (2, 0)
        self.labirinto.mapa[2][0] = 'H'
        self.robo.posicao = (2, 1)
        self.robo.direcao = 'N'
        self.assertTrue(self.robo.pegar_humano())
        self.assertTrue(self.robo.com_humano)
        self.assertEqual(self.robo.direcao, 'W')
        # Verifica se o humano foi removido do mapa
        self.assertIsNone(self.labirinto.posicao_humano)
        self.assertEqual(self.labirinto.mapa[2][0], 'VAZIO')

    def test_seguir_caminho_sem_caminho(self):
        self.robo.caminho = []
        with patch.object(self.robo, 'avancar') as mock_avancar:
            self.robo.seguir_caminho()
            # avancar() não deve ser chamado
            mock_avancar.assert_not_called()

    def test_seguir_caminho_avancar_false(self):
        self.robo.caminho = [(1, 1), (1, 2), (1, 3)]
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'E'

        original_avancar = self.robo.avancar

        def avancar_side_effect():
            if self.robo.posicao == (1, 2):
                return False  # Simula falha ao avançar de (1,2) para (1,3)
            else:
                return original_avancar()

        with patch.object(self.robo, 'avancar', side_effect=avancar_side_effect) as mock_avancar:
            self.robo.seguir_caminho()
            # avancar deve ser chamado duas vezes
            self.assertEqual(mock_avancar.call_count, 2)
            # O robô deve ter parado na posição (1,2)
            self.assertEqual(self.robo.posicao, (1, 2))


if __name__ == '__main__':
    unittest.main()
