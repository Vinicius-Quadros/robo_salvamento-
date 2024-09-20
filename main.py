import sys
from labirinto import Labirinto
from robo import Robo

def main():
    # Argumento para passar os mapas.
    if len(sys.argv) > 1:
        nome_arquivo_mapa = sys.argv[1]
    else:
        nome_arquivo_mapa = 'mapa.txt'

    labirinto = Labirinto(nome_arquivo_mapa)
    labirinto.exibir_mapa()

    robo = Robo(labirinto)
    print(f"Robô iniciado na posição {robo.posicao}, virado para {robo.direcao}.")

    robo.executar_missao()

    robo.gerar_log_csv(f'{nome_arquivo_mapa}_log.csv')
    print(f"Missão concluída. Logs salvos em {nome_arquivo_mapa}_log.csv.")

if __name__ == "__main__":
    main()
