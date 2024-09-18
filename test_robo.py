import unittest
from labirinto import Labirinto
from robo import Robo
from unittest.mock import patch
import os

class TestLabirinto(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para os testes
        self.labirinto = Labirinto('mapa.txt')

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
                labirinto = Labirinto('mapa.txt')
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
        labirinto = Labirinto('mapa.txt')
        labirinto.posicao_entrada = (0, 3)
        labirinto.mapa[0][3] = ' '
        robo = Robo(labirinto)
        robo.posicao = (0, 3)
        robo.direcao = 'N'
        self.assertTrue(labirinto.is_saida(robo.posicao, robo.direcao))

    def test_is_saida_return_true_sul(self):
        # Robô na última linha olhando para o sul
        labirinto = Labirinto('mapa.txt')
        linha_max = labirinto.altura - 1
        labirinto.posicao_entrada = (linha_max, 3)
        labirinto.mapa[linha_max][3] = ' '
        robo = Robo(labirinto)
        robo.posicao = (linha_max, 3)
        robo.direcao = 'S'
        self.assertTrue(labirinto.is_saida(robo.posicao, robo.direcao))

    def test_is_saida_return_true_oeste(self):
        # Robô na primeira coluna olhando para o oeste
        labirinto = Labirinto('mapa.txt')
        labirinto.posicao_entrada = (4, 0)
        labirinto.mapa[4][0] = ' '
        robo = Robo(labirinto)
        robo.posicao = (4, 0)
        robo.direcao = 'W'
        self.assertTrue(labirinto.is_saida(robo.posicao, robo.direcao))

    def test_is_saida_return_true_leste(self):
        # Robô na última coluna olhando para o leste
        labirinto = Labirinto('mapa.txt')
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
        # Testa o comportamento ao tentar carregar um labirinto vazio
        with open('labirinto_vazio.txt', 'w') as f:
            pass  # Cria um arquivo vazio
        with self.assertRaises(ValueError):
            Labirinto('labirinto_vazio.txt')
        os.remove('labirinto_vazio.txt')

    def test_labirinto_corrompido(self):
        # Testa se o mapa corrompido gera exceção ou comportamento inesperado
        with open('mapa_corrompido.txt', 'w') as f:
            f.write('E*H\n*')  # Linha com comprimento irregular
        with self.assertRaises(ValueError):
            Labirinto('mapa_corrompido.txt')
        os.remove('mapa_corrompido.txt')

class TestRobo(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para os testes do robô
        self.labirinto = Labirinto('mapa.txt')
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
        # Testa a função de giro do robô
        direcoes = ['N', 'E', 'S', 'W']
        self.robo.direcao = 'N'
        for direcao_esperada in direcoes[1:] + ['N']:
            self.robo.girar()
            self.assertEqual(self.robo.direcao, direcao_esperada)

    def test_pegar_humano(self):
        # Posiciona o robô ao lado do humano
        self.robo.posicao = (self.labirinto.posicao_humano[0] - 1, self.labirinto.posicao_humano[1])
        self.robo.direcao = 'S'  # Olhando para o humano
        self.assertTrue(self.robo.pegar_humano())
        self.assertTrue(self.robo.com_humano)
        self.assertIsNone(self.labirinto.posicao_humano)
        # Tentar pegar novamente
        self.assertFalse(self.robo.pegar_humano())

    def test_pegar_humano_sem_humano(self):
        # Posiciona o robô em um local sem humano
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertFalse(self.robo.pegar_humano())
        # Verifica se o alarme foi registrado
        self.assertIn("Alarme: Tentativa de coleta sem humano a frente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_sensor_frente(self):
        # Testa o sensor frontal
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertEqual(self.robo.sensor_frente(), 'VAZIO')

        self.labirinto.mapa[2][1] = '*'  # Coloca uma parede à frente
        self.assertEqual(self.robo.sensor_frente(), 'PAREDE')

    def test_sensor_esquerda(self):
        # Testa o sensor esquerdo
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertEqual(self.robo.sensor_esquerda(), 'VAZIO')  # Posição depende do mapa

    def test_sensor_direita(self):
        # Testa o sensor direito
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.assertEqual(self.robo.sensor_direita(), 'PAREDE')  # Posição depende do mapa

    def test_bfs(self):
        # Testa a função de busca (BFS)
        caminho = self.robo.bfs(self.robo.posicao, self.labirinto.posicao_humano)
        self.assertIsNotNone(caminho)
        self.assertTrue(len(caminho) > 0)

    def test_bfs_sem_caminho(self):
        # Bloqueia o caminho até o humano
        self.labirinto.mapa[2][1] = '*'
        self.labirinto.mapa[1][2] = '*'
        self.labirinto.mapa[1][0] = '*'
        caminho = self.robo.bfs(self.robo.posicao, self.labirinto.posicao_humano)
        self.assertIsNone(caminho)

    def test_executar_missao(self):
        # Executa a missão e verifica se o humano foi coletado
        self.robo.executar_missao()
        self.assertFalse(self.robo.com_humano)  # Após a missão, o humano deve ter sido entregue

    def test_missao_falha(self):
        # Bloqueia o caminho até o humano para causar uma falha na missão
        self.labirinto.mapa[self.labirinto.posicao_humano[0]][self.labirinto.posicao_humano[1]-1] = '*'
        self.labirinto.mapa[self.labirinto.posicao_humano[0]][self.labirinto.posicao_humano[1]+1] = '*'
        self.labirinto.mapa[self.labirinto.posicao_humano[0]-1][self.labirinto.posicao_humano[1]] = '*'
        self.labirinto.mapa[self.labirinto.posicao_humano[0]+1][self.labirinto.posicao_humano[1]] = '*'
        self.robo.executar_missao()

        # Verifica se a mensagem de falha da missão está nos logs
        mensagens_log = [log[0] for log in self.robo.logs if isinstance(log, list) and len(log) > 0]
        self.assertIn("Missao falhou: Caminho nao encontrado", mensagens_log)

    def test_gerar_log_csv(self):
        # Testa a função de gerar o log CSV
        self.robo.executar_missao()
        nome_arquivo = 'log_robo_test.csv'
        self.robo.gerar_log_csv(nome_arquivo)
        with open(nome_arquivo, 'r') as file:
            lines = file.readlines()
        self.assertGreater(len(lines), 1)
        os.remove(nome_arquivo)

    def test_condicoes_adicionais(self):
        # Testa casos adicionais não cobertos
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
        self.robo.com_humano = True  # Suponha que o robô já coletou o humano
        self.robo.posicao = (1, 1)  # Define a posição do robô
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = '*'  # Parede à frente
        self.labirinto.mapa[1][0] = '*'  # Parede à esquerda
        self.labirinto.mapa[1][2] = '*'  # Parede à direita

        # Atualiza o mapa e verifica
        self.robo.verificar_beco_sem_saida()
        self.assertIn("Alarme: Beco sem saída após coleta do humano!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_alarme_ejecao_sem_humano(self):
        self.robo.com_humano = False  # O robô não tem humano
        self.robo.registrar_ejecao()
        self.assertIn("Alarme: Tentativa de ejeção sem humano presente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_alarme_coleta_sem_humano(self):
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = ' '  # Célula à frente está vazia
        self.robo.pegar_humano()
        self.assertIn("Alarme: Tentativa de coleta sem humano a frente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_atualizar_posicao_humano(self):
        # Verifica se a posição do humano é atualizada após a coleta
        self.robo.posicao = (self.labirinto.posicao_humano[0] - 1, self.labirinto.posicao_humano[1])
        self.robo.direcao = 'S'  # Olhando para o humano
        self.robo.pegar_humano()
        self.assertIsNone(self.labirinto.posicao_humano)
        self.assertEqual(self.labirinto.mapa[self.robo.posicao[0]+1][self.robo.posicao[1]], 'VAZIO')

    def test_direcao_para_posicao(self):
        # Testa a função que determina a direção necessária para uma posição
        self.robo.posicao = (2, 2)
        pos_alvo = (2, 3)
        direcao = self.robo.direcao_para_posicao(pos_alvo)
        self.assertEqual(direcao, 'E')

        pos_alvo = (1, 2)
        direcao = self.robo.direcao_para_posicao(pos_alvo)
        self.assertEqual(direcao, 'N')

    def test_seguir_caminho(self):
        # Testa se o robô segue o caminho corretamente
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
        # Testa a função de analisar posição
        self.assertEqual(self.robo.analisar_posicao((1, 1)), 'VAZIO')
        self.labirinto.mapa[1][1] = '*'
        self.assertEqual(self.robo.analisar_posicao((1, 1)), 'PAREDE')
        self.labirinto.mapa[1][1] = 'H'
        self.assertEqual(self.robo.analisar_posicao((1, 1)), 'HUMANO')

    def test_frente(self):
        # Testa a função que retorna a posição à frente do robô
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
        # Testa se o robô está próximo ao humano
        self.robo.posicao = (self.labirinto.posicao_humano[0], self.labirinto.posicao_humano[1] -1)
        self.assertTrue(self.robo.esta_proximo_ao_humano())
        self.robo.posicao = (self.labirinto.posicao_humano[0] -2, self.labirinto.posicao_humano[1])
        self.assertFalse(self.robo.esta_proximo_ao_humano())

    def test_verificar_ejecao_sem_humano(self):
        # Testa tentar ejetar sem humano
        self.robo.com_humano = False
        self.assertTrue(self.robo.verificar_ejecao_sem_humano())
        self.assertIn("Alarme: Tentativa de ejeção sem humano presente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_verificar_coleta_sem_humano(self):
        # Testa tentar coletar sem humano à frente
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = ' '
        self.robo.pegar_humano()
        self.assertIn("Alarme: Tentativa de coleta sem humano a frente!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_verificar_beco_sem_saida(self):
        # Testa se o robô identifica um beco sem saída após coletar o humano
        self.robo.com_humano = True
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'S'
        self.labirinto.mapa[2][1] = '*'
        self.labirinto.mapa[1][0] = '*'
        self.labirinto.mapa[1][2] = '*'
        self.assertTrue(self.robo.verificar_beco_sem_saida())
        self.assertIn("Alarme: Beco sem saída após coleta do humano!", [log[0] for log in self.robo.logs if isinstance(log, list)])

    def test_pegar_humano_lateral_direita(self):
        # Posiciona o humano à direita do robô
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
        # Posiciona o humano à esquerda do robô
        self.labirinto.posicao_humano = (2, 0)
        self.labirinto.mapa[2][0] = 'H'
        self.robo.posicao = (2, 1)
        self.robo.direcao = 'N'  # Robô olhando para o norte
        self.assertTrue(self.robo.pegar_humano())
        self.assertTrue(self.robo.com_humano)
        self.assertEqual(self.robo.direcao, 'W')  # O robô deve ter girado para o oeste
        # Verifica se o humano foi removido do mapa
        self.assertIsNone(self.labirinto.posicao_humano)
        self.assertEqual(self.labirinto.mapa[2][0], 'VAZIO')

    def test_seguir_caminho_sem_caminho(self):
        # Testa o caso em que self.caminho está vazio
        self.robo.caminho = []
        with patch.object(self.robo, 'avancar') as mock_avancar:
            self.robo.seguir_caminho()
            # avancar() não deve ser chamado
            mock_avancar.assert_not_called()

    def test_seguir_caminho_avancar_false(self):
        # Configura o robô com um caminho
        self.robo.caminho = [(1, 1), (1, 2), (1, 3)]
        self.robo.posicao = (1, 1)
        self.robo.direcao = 'E'

        # Mock avancar para retornar False na segunda chamada
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
