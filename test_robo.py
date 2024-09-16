import unittest
from labirinto import Labirinto
from robo import Robo

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
        self.assertFalse(self.labirinto.is_valida((self.labirinto.altura, self.labirinto.largura)))  # Outra posição fora dos limites

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
        # Use unittest.mock para capturar a saída do print
        from unittest.mock import patch
        with patch('builtins.print') as mocked_print:
            self.labirinto.exibir_mapa()
            mocked_print.assert_called()  # Verifica se print foi chamado pelo menos uma vez

    def test_labirinto_vazio(self):
        # Testa o comportamento ao tentar carregar um labirinto inexistente
        with self.assertRaises(FileNotFoundError):
            Labirinto('arquivo_inexistente.txt')

    def test_labirinto_corrompido(self):
        # Testa se o mapa corrompido gera exceção ou comportamento inesperado
        with self.assertRaises(Exception):
            Labirinto('mapa_corrompido.txt')

class TestRobo(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para os testes do robô
        self.labirinto = Labirinto('mapa.txt')
        self.robo = Robo(self.labirinto)

    def test_direcao_inicial(self):
        # Testa a direção inicial do robô
        self.assertEqual(self.robo.direcao, 'S')

    def test_avancar(self):
        # Configura o robô para avançar contra uma parede
        self.robo.posicao = (0, 0)  # Posiciona o robô no canto superior esquerdo
        self.robo.direcao = 'N'  # Direção Norte, onde há uma parede
        self.assertFalse(self.robo.avancar())  # Deve retornar False, indicando colisão

    def test_girar(self):
        # Testa a função de giro do robô
        direcoes = ['N', 'E', 'S', 'W']
        for direcao in direcoes:
            self.robo.direcao = direcao
            self.robo.girar()
        self.assertEqual(self.robo.direcao, 'N')

    def test_pegar_humano(self):
        # Testa a função de pegar o humano
        self.robo.posicao = self.labirinto.posicao_humano
        self.robo.pegar_humano()
        self.assertTrue(self.robo.com_humano)
        self.robo.pegar_humano()  # Tentar pegar novamente
        self.assertTrue(self.robo.com_humano)

    def test_bfs(self):
        # Testa a função de busca (BFS)
        caminho = self.robo.bfs(self.robo.posicao, self.labirinto.posicao_humano)
        self.assertIsNotNone(caminho)
        self.assertTrue(len(caminho) > 0)

    def test_executar_missao(self):
        # Executa a missão e verifica se o humano foi coletado
        self.robo.executar_missao()
        if self.robo.com_humano:
            self.assertFalse(self.robo.com_humano)  # Verifica se o robô está com o humano após a missão

    def test_missao_falha(self):
        # Bloqueia o caminho até o humano para causar uma falha na missão
        self.labirinto.mapa[7][5] = '*'  # Adiciona uma parede na posição do humano
        self.robo.executar_missao()

        # Verifica se a mensagem de falha da missão está nos logs
        mensagens_log = [log[0] for log in self.robo.logs if isinstance(log, list) and len(log) > 0]
        print("Logs gerados:", mensagens_log)  # Adicione esta linha para depuração
        self.assertIn("Missao falhou: Caminho nao encontrado", mensagens_log)

    def test_gerar_log_csv(self):
        # Testa a função de gerar o log CSV
        self.robo.executar_missao()
        self.robo.gerar_log_csv('log_robo_test.csv')
        with open('log_robo_test.csv', 'r') as file:
            lines = file.readlines()
        self.assertGreater(len(lines), 1)

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
        self.assertTrue(self.robo.verificar_colisao((2, 1)))
        self.assertIn("Alarme: Colisão com parede!", [log[0] for log in self.robo.logs])

    def test_alarme_atropelamento_humano(self):
        self.robo.posicao = (1, 1)
        self.labirinto.mapa[2][1] = 'H'  # Coloca um humano à frente
        self.assertTrue(self.robo.verificar_atropelamento((2, 1)))
        self.assertIn("Alarme: Atropelamento de humano!", [log[0] for log in self.robo.logs])

    def test_alarme_beco_sem_saida(self):
        self.robo.com_humano = True  # Suponha que o robô já coletou o humano
        self.robo.posicao = (1, 1)  # Define a posição do robô
        self.labirinto.mapa[1][0] = '*'  # Parede à esquerda
        self.labirinto.mapa[1][2] = '*'  # Parede à direita
        self.labirinto.mapa[0][1] = '*'  # Parede à frente

        # Atualiza o mapa e verifica novamente
        self.assertTrue(self.robo.verificar_beco_sem_saida())
        self.assertIn("Alarme: Beco sem saída após coleta do humano!", [log[0] for log in self.robo.logs])

    def test_alarme_ejecao_sem_humano(self):
        self.robo.com_humano = False  # O robô não tem humano
        self.assertTrue(self.robo.verificar_ejecao_sem_humano())
        self.assertIn("Alarme: Tentativa de ejeção sem humano presente!", [log[0] for log in self.robo.logs])

    def test_alarme_coleta_sem_humano(self):
        self.robo.posicao = (1, 1)
        self.labirinto.mapa[2][1] = ' '  # Célula à frente está vazia
        self.assertTrue(self.robo.verificar_coleta_sem_humano())
        self.assertIn("Alarme: Tentativa de coleta sem humano à frente!", [log[0] for log in self.robo.logs])

if __name__ == '__main__':
    unittest.main()
