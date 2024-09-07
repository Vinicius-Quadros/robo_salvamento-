class Labirinto:
    def __init__(self, arquivo_de_entrada):
        self.mapa = self.carregar_mapa(arquivo_de_entrada)
        self.posicao_do_humano = self.encontrar_humano()
        self.posicao_do_robo = self.encontrar_entrada()
        self.tamanho_horizontal = self.calcular_tamanho_horizontal()
        self.tamanho_vertical = self.calcular_tamanho_vertical()

    @staticmethod
    def carregar_mapa(arquivo_de_entrada):
        with open(arquivo_de_entrada, 'r') as ler:
            mapa = [list(linha.strip()) for linha in ler.readlines()]
        return mapa

    def encontrar_humano(self):
        for i, linhas in enumerate(self.mapa):
            if "H" in linhas:
                return i, linhas.index('H')

    def encontrar_entrada(self):
        for i, linha in enumerate(self.mapa):
            if 'E' in linha:
                return i, linha.index('E')

    def calcular_tamanho_horizontal(self):
        if self.mapa:
            return len(self.mapa[0])
        return 0

    def calcular_tamanho_vertical(self):
        return len(self.mapa)

    def mostrar_mapa(self):
        for linha in self.mapa:
            print("".join(linha))


class Robo:
    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.x, self.y = labirinto.posicao_do_robo  # Posição inicial (entrada do labirinto)
        self.direcao = self.direcao_labirinto(labirinto.posicao_do_robo)
        self.carga = "SEM CARGA"  # Robô começa sem o humano
        self.log = []  # Armazena o log das operações

    def direcao_labirinto(self, posicao_robo):
        linha, coluna = posicao_robo

        if linha == 0:
            return "S"
        elif linha == self.labirinto.tamanho_vertical - 1:
            return "N"
        elif coluna == 0:
            return "E"
        elif coluna == self.labirinto.tamanho_horizontal - 1:
            return "W"

    def regastar(self):
        pass



labirinto = Labirinto('labirinto_exemplo.txt')
labirinto.mostrar_mapa()
robo = Robo(labirinto)
print(robo.direcao)  # Verifica a direção inicial do robô

