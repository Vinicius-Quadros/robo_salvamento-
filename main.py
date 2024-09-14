# main.py
from labirinto import Labirinto
from robo import Robo

def main():
    # Carregar o labirinto a partir de um arquivo .txt
    nome_arquivo_mapa = 'mapa.txt'
    labirinto = Labirinto(nome_arquivo_mapa)
    labirinto.exibir_mapa()

    # Inicializar o robô
    robo = Robo(labirinto)
    print(f"Robô iniciado na posição {robo.posicao}, virado para {robo.direcao}.")

    # Executar a missão de resgate
    robo.executar_missao()

    # Gerar o log em CSV
    robo.gerar_log_csv(f'{nome_arquivo_mapa}_log.csv')
    print(f"Missão concluída. Logs salvos em {nome_arquivo_mapa}_log.csv'.")

if __name__ == "__main__":
    main()
