import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation


# Função para desenhar o labirinto
def desenhar_labirinto(ax, mapa):
    linhas = mapa.strip().split('\n')
    altura = len(linhas)
    largura = len(linhas[0])

    for y in range(altura):
        for x in range(largura):
            caractere = linhas[y][x]
            # Paredes
            if caractere == '*':
                ax.add_patch(plt.Rectangle((x, altura - y - 1), 1, 1, facecolor='black', edgecolor='black'))
            # Humano
            elif caractere == 'H':
                ax.add_patch(plt.Rectangle((x, altura - y - 1), 1, 1, facecolor='red', edgecolor='black'))
            # Caminhos livres
            elif caractere == ' ' or caractere == 'E':
                ax.add_patch(plt.Rectangle((x, altura - y - 1), 1, 1, facecolor='white', edgecolor='black'))


# Função de busca simples (DFS) para encontrar o caminho da entrada até o humano
def buscar_caminho(mapa):
    linhas = mapa.strip().split('\n')
    altura = len(linhas)
    largura = len(linhas[0])

    # Encontra a posição da entrada e do humano
    entrada = None
    humano = None
    for y in range(altura):
        for x in range(largura):
            if linhas[y][x] == 'E':
                entrada = (x, y)
            elif linhas[y][x] == 'H':
                humano = (x, y)

    # Função de DFS para encontrar o caminho
    caminho = []
    visitado = set()

    def dfs(pos):
        if pos == humano:
            caminho.append(pos)
            return True
        x, y = pos
        if pos in visitado or linhas[y][x] == '*':
            return False
        visitado.add(pos)
        caminho.append(pos)

        # Movimentos possíveis: direita, esquerda, baixo, cima
        movimentos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for mov in movimentos:
            novo_x, novo_y = x + mov[0], y + mov[1]
            if 0 <= novo_x < largura and 0 <= novo_y < altura:
                if dfs((novo_x, novo_y)):
                    return True

        caminho.pop()  # Remove se não for o caminho certo
        return False

    dfs(entrada)
    return caminho


# Função para criar a animação do robô
def animar_robo(mapa, caminho):
    linhas = mapa.strip().split('\n')
    altura = len(linhas)

    fig, ax = plt.subplots()
    desenhar_labirinto(ax, mapa)

    # Configura o aspecto para que as células sejam quadradas
    ax.set_aspect('equal')
    ax.set_xlim(0, len(linhas[0]))
    ax.set_ylim(0, altura)
    ax.axis('off')

    # Adiciona o robô (bloco azul) inicial na posição da entrada
    robo = patches.Rectangle((caminho[0][0], altura - caminho[0][1] - 1), 1, 1, facecolor='blue', edgecolor='black')
    ax.add_patch(robo)

    # Lista para guardar as marcas de onde o robô já passou (ida e volta)
    marcas = []

    # Função de atualização da animação
    def update(frame):
        total_frames = len(caminho) * 2  # Ida e volta
        halfway = len(caminho)

        if frame < halfway:  # Ida (cor azul)
            pos = caminho[frame]
            # Adiciona uma marca azul onde o robô passou
            marca = patches.Rectangle((pos[0], altura - pos[1] - 1), 1, 1, facecolor='blue', edgecolor='black')
            ax.add_patch(marca)
            marcas.append(marca)
            robo.set_xy((pos[0], altura - pos[1] - 1))
        else:  # Volta (cor roxa)
            pos = caminho[total_frames - frame - 1]
            # Adiciona uma marca roxa no caminho de volta
            marca = patches.Rectangle((pos[0], altura - pos[1] - 1), 1, 1, facecolor='purple', edgecolor='black')
            ax.add_patch(marca)
            marcas.append(marca)
            robo.set_xy((pos[0], altura - pos[1] - 1))

            # Verifica se o robô chegou de volta à entrada e para a animação
            if frame == total_frames - 1:  # Último quadro
                anim.event_source.stop()

        return [robo] + marcas

    # Cria a animação
    anim = FuncAnimation(fig, update, frames=len(caminho) * 2, interval=500, blit=True)

    # Exibe a animação
    plt.show()


# Função para carregar o mapa de um arquivo .txt
def carregar_mapa(arquivo):
    with open(arquivo, 'r') as f:
        return f.read()


# Caminho do arquivo .txt com o mapa do labirinto
arquivo_mapa = 'mapa.txt'

# Carrega o mapa a partir do arquivo
mapa_labirinto = carregar_mapa(arquivo_mapa)

# Busca o caminho da entrada até o humano
caminho = buscar_caminho(mapa_labirinto)

# Anima o robô seguindo o caminho (ida e volta)
animar_robo(mapa_labirinto, caminho)
