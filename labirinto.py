class Labirinto:
    def __init__(self, arquivo_mapa):
        self.mapa = self.carregar_mapa(arquivo_mapa)
        self.altura = len(self.mapa)
        self.largura = len(self.mapa[0])
        self.posicao_humano = self.encontrar_humano()
        self.posicao_entrada = self.encontrar_entrada()
        self.posicao_saida = self.posicao_entrada

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
        return self.is_dentro_dos_limites(pos) and self.mapa[pos[0]][pos[1]] != '*'

    def is_dentro_dos_limites(self, pos):
        linha, coluna = pos
        return 0 <= linha < self.altura and 0 <= coluna < self.largura

    def is_saida(self, pos, direcao):
        linha, coluna = pos
        linha_max = self.altura - 1
        coluna_max = self.largura - 1

        # Verifica se a posição atual é na borda e não é uma parede
        if self.mapa[linha][coluna] == '*':
            return False
        if direcao == 'N' and linha == 0:
            return True
        elif direcao == 'S' and linha == linha_max:
            return True
        elif direcao == 'W' and coluna == 0:
            return True
        elif direcao == 'E' and coluna == coluna_max:
            return True
        else:
            return False