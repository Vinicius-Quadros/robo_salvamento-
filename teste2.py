class Labirinto:
    def __init__(self, arquivo_de_entrada):
        self.mapa = self.carregar_mapa(arquivo_de_entrada)
        self.posicao_do_humano = self.encontrar_humano()
        self.posicao_do_robo = self.encontrar_entrada()

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

    def mostrar_mapa(self):
        for linha in self.mapa:
            print("".join(linha))


class Robo:
    def __init__(self):
        pass



labirinto = Labirinto('labirinto_exemplo.txt')
labirinto.mostrar_mapa()
print(labirinto.posicao_do_robo)
print(labirinto.posicao_do_humano)

