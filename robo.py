# robo.py
from collections import deque
import csv

class Robo:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.posicao = labirinto.posicao_entrada
        self.direcao = self.direcao_labirinto(self.posicao)
        self.com_humano = False
        self.logs = []
        self.caminho = []

        # Registra o log de inicialização
        self.registrar_log("LIGAR")

    def direcao_labirinto(self, posicao_entrada):
        linha, coluna = posicao_entrada
        if linha == 0:
            return "S"
        elif linha == self.labirinto.altura - 1:
            return "N"
        elif coluna == 0:
            return "E"
        elif coluna == self.labirinto.largura - 1:
            return "W"

    def registrar_log(self, comando):
        esquerda = self.sensor_esquerda()
        direita = self.sensor_direita()
        frente = self.sensor_frente()
        carga = "COM HUMANO" if self.com_humano else "SEM CARGA"
        self.logs.append([comando, esquerda, direita, frente, carga])

    def sensor_frente(self):
        return self.analisar_posicao(self.frente())

    def sensor_esquerda(self):
        linha, coluna = self.posicao
        if self.direcao == "N":
            return self.analisar_posicao((linha, coluna - 1))  # Oeste
        elif self.direcao == "S":
            return self.analisar_posicao((linha, coluna + 1))  # Leste
        elif self.direcao == "E":
            return self.analisar_posicao((linha - 1, coluna))  # Norte
        elif self.direcao == "W":
            return self.analisar_posicao((linha + 1, coluna))  # Sul

    def sensor_direita(self):
        linha, coluna = self.posicao
        if self.direcao == "N":
            return self.analisar_posicao((linha, coluna + 1))  # Leste
        elif self.direcao == "S":
            return self.analisar_posicao((linha, coluna - 1))  # Oeste
        elif self.direcao == "E":
            return self.analisar_posicao((linha + 1, coluna))  # Sul
        elif self.direcao == "W":
            return self.analisar_posicao((linha - 1, coluna))  # Norte

    def analisar_posicao(self, pos):
        if not self.labirinto.is_valida(pos):
            return "PAREDE"
        elif pos == self.labirinto.posicao_humano:
            return "HUMANO"
        else:
            return "VAZIO"

    def girar(self):
        if self.direcao == "N":
            self.direcao = "E"
        elif self.direcao == "E":
            self.direcao = "S"
        elif self.direcao == "S":
            self.direcao = "W"
        elif self.direcao == "W":
            self.direcao = "N"
        self.registrar_log("G")

    def frente(self):
        linha, coluna = self.posicao
        if self.direcao == "N":
            return (linha - 1, coluna)
        elif self.direcao == "S":
            return (linha + 1, coluna)
        elif self.direcao == "E":
            return (linha, coluna + 1)
        elif self.direcao == "W":
            return (linha, coluna - 1)

    def avancar(self):
        nova_posicao = self.frente()
        if self.labirinto.is_valida(nova_posicao):
            self.posicao = nova_posicao
            self.registrar_log("A")
            return True
        else:
            self.registrar_log("A")
            return False

    def pegar_humano(self):
        if self.posicao == self.labirinto.posicao_humano:
            self.com_humano = True
            self.registrar_log("P")
        else:
            self.registrar_log("P")

    def gerar_log_csv(self, nome_arquivo):
        with open(nome_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Comando', 'Sensor Esquerdo', 'Sensor Direito', 'Sensor Frente', 'Carga'])
            writer.writerows(self.logs)

    def bfs(self, inicio, objetivo):
        queue = deque()
        queue.append((inicio, [inicio]))
        visitado = set()
        visitado.add(inicio)

        while queue:
            current, path = queue.popleft()
            if current == objetivo:
                return path

            movimentos = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            for movimento in movimentos:
                next_pos = (current[0] + movimento[0], current[1] + movimento[1])
                if self.labirinto.is_valida(next_pos) and next_pos not in visitado:
                    visitado.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

        return None

    def encontrar_caminho(self):
        caminho = self.bfs(self.posicao, self.labirinto.posicao_humano)
        if caminho:
            self.caminho = caminho
            self.logs.append("Caminho encontrado")
            return True
        else:
            self.logs.append("Missão falhou: Caminho não encontrado")
            return False

    def seguir_caminho(self):
        if not self.caminho:
            return

        for pos in self.caminho[1:]:
            direcao_necessaria = self.direcao_para_posicao(pos)
            while self.direcao != direcao_necessaria:
                self.girar()
            self.avancar()

    def direcao_para_posicao(self, pos):
        linha_atual, coluna_atual = self.posicao
        linha_dest, coluna_dest = pos
        if linha_dest < linha_atual:
            return "N"
        elif linha_dest > linha_atual:
            return "S"
        elif coluna_dest > coluna_atual:
            return "E"
        elif coluna_dest < coluna_atual:
            return "W"

    def executar_missao(self):
        encontrado = self.encontrar_caminho()
        if not encontrado:
            return

        self.logs.append("Iniciando missão de resgate")
        self.seguir_caminho()
        self.pegar_humano()

        self.caminho = list(reversed(self.caminho))
        self.logs.append("Iniciando retorno à entrada")
        self.seguir_caminho()

        # Ejeção do humano ao final da missão
        self.registrar_ejecao()
        self.logs.append("Missão concluída")

    def registrar_ejecao(self):
        """Registra o comando de ejeção do humano"""
        self.com_humano = False  # Após ejeção, o compartimento fica sem carga
        self.registrar_log("E")
