class Labirinto:
    def __init__(self, arquivo_mapa):
        self.mapa = self.carregar_mapa(arquivo_mapa)
        self.altura = len(self.mapa)
        self.largura = len(self.mapa[0])
        self.posicao_humano = self.encontrar_humano()
        self.posicao_entrada = self.encontrar_entrada()

    @staticmethod
    def carregar_mapa(arquivo_mapa):
        with open(arquivo_mapa, 'r') as file:
            mapa = [list(linha.rstrip('\n')) for linha in file.readlines()]
        return mapa

    def encontrar_humano(self):
        for i in range(self.altura):
            for j in range(self.largura):
                if self.mapa[i][j] == 'H':
                    return i, j
        return None

    def encontrar_entrada(self):
        for i in range(self.altura):
            for j in range(self.largura):
                if self.mapa[i][j] == 'E':
                    return i, j
        return None

    def exibir_mapa(self):
        for linha in self.mapa:
            print("".join(linha))

    def is_valida(self, pos):
        linha, coluna = pos
        return 0 <= linha < self.altura and 0 <= coluna < self.largura and self.mapa[linha][coluna] != '*'
