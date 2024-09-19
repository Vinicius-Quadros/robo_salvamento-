# Robô de Salvamento em Labirinto

Este projeto implementa um robô de salvamento que navega em um labirinto em busca de um humano, utilizando o algoritmo de busca em largura (BFS). O objetivo é simular uma missão de resgate em um ambiente de labirinto, com o robô encontrando um humano e retornando à entrada do labirinto.

## Estrutura de Pastas

A estrutura de pastas do projeto é a seguinte:

```bash
projeto/
├── __init__.py        # Arquivo vazio, inicializa o diretório como um pacote Python
├── labirinto.py       # Implementa a classe Labirinto, que modela o ambiente do robô
├── robo.py            # Implementa a classe Robo, responsável por simular o comportamento do robô
├── main.py            # Script principal que inicializa e executa o robô e o labirinto
├── mapa.txt           # Arquivo de texto que define o layout do labirinto
├── tests/             # Diretório contendo os testes unitários
│   ├── __init__.py    # Arquivo vazio, inicializa o diretório como um pacote Python
│   ├── test_labirinto.py  # Testes unitários para a classe Labirinto
│   └── test_robo.py       # Testes unitários para a classe Robo
```

## Descrição dos Arquivos

### `labirinto.py`
Este arquivo contém a classe `Labirinto`, que modela o ambiente no qual o robô opera. O labirinto é representado por uma matriz de células, onde cada célula pode conter:

- `' '` (espaço vazio): O robô pode se mover livremente.
- `'*'` (parede): Impede o movimento do robô.
- `'H'` (humano): O objetivo final do robô, que deve ser resgatado.

**Principais métodos:**
- `is_valida()`: Verifica se uma posição no labirinto é válida.
- `carregar_mapa()`: Carrega o mapa a partir de um arquivo de texto.
- `exibir_mapa()`: Exibe o labirinto no console.

### `robo.py`
Este arquivo implementa a classe `Robo`, que simula o comportamento do robô durante sua missão de resgate. O robô utiliza três sensores (dois laterais e um frontal) e só pode girar 90° no sentido horário, sendo os comandos possiveis:

- `'A'` Avançar para frente UMA POSIÇÃO
- `'G'` Girar o robô 90 graus à direita (sentido horário)
- `'P'` Pegar o humano imediatamente à frente do robô (só tem carga na bateria para UMA tentativa)
- `'E'` Ejetar humano para fora do labirinto (só tem carga na bateria para UMA tentativa)


**Principais métodos:**
- `avancar()`: Faz o robô se mover para a próxima célula à sua frente.
- `girar()`: Gira o robô 90° no sentido horário.
- `registrar_log()`: Registra logs das ações do robô, incluindo alarmes de colisão, beco sem saída, e ejeção.
- `verificar_coleta()`: Verifica se o robô está pronto para coletar o humano.

### `main.py`
O script principal que inicializa o labirinto e o robô e executa a simulação. Ele carrega o mapa do labirinto a partir do arquivo `mapa.txt`, posiciona o robô na entrada e começa a execução do algoritmo de busca.

Ao final será criado um arquivo csv, aonde poderá ser visualizado os passos que o robo deu no labirinto,  como no exemplo abaixo:
```
Comando,Sensor Esquerdo,Sensor Direito,Sensor Frente,Carga
LIGAR,PAREDE,PAREDE,VAZIO,SEM CARGA
Caminho encontrado
Iniciando missao de resgate
A,VAZIO,VAZIO,PAREDE,SEM CARGA
G,PAREDE,VAZIO,VAZIO,SEM CARGA
A,PAREDE,PAREDE,VAZIO,SEM CARGA
A,VAZIO,PAREDE,PAREDE,SEM CARGA
G,PAREDE,VAZIO,PAREDE,SEM CARGA
G,PAREDE,VAZIO,VAZIO,SEM CARGA
G,VAZIO,PAREDE,VAZIO,SEM CARGA
A,PAREDE,PAREDE,VAZIO,SEM CARGA
A,VAZIO,PAREDE,PAREDE,SEM CARGA
G,PAREDE,VAZIO,PAREDE,SEM CARGA
G,PAREDE,VAZIO,VAZIO,SEM CARGA
G,VAZIO,PAREDE,VAZIO,SEM CARGA
A,PAREDE,PAREDE,VAZIO,SEM CARGA
A,PAREDE,PAREDE,VAZIO,SEM CARGA
A,PAREDE,PAREDE,VAZIO,SEM CARGA
A,PAREDE,VAZIO,PAREDE,SEM CARGA
G,PAREDE,VAZIO,VAZIO,SEM CARGA
A,PAREDE,PAREDE,VAZIO,SEM CARGA
A,PAREDE,VAZIO,VAZIO,SEM CARGA
A,PAREDE,PAREDE,HUMANO,SEM CARGA
P,PAREDE,PAREDE,VAZIO,COM HUMANO
iniciando retorno
G,VAZIO,VAZIO,PAREDE,COM HUMANO
G,PAREDE,PAREDE,VAZIO,COM HUMANO
A,VAZIO,PAREDE,VAZIO,COM HUMANO
A,PAREDE,PAREDE,VAZIO,COM HUMANO
A,VAZIO,PAREDE,PAREDE,COM HUMANO
G,PAREDE,VAZIO,PAREDE,COM HUMANO
G,PAREDE,VAZIO,VAZIO,COM HUMANO
G,VAZIO,PAREDE,VAZIO,COM HUMANO
A,PAREDE,PAREDE,VAZIO,COM HUMANO
A,PAREDE,PAREDE,VAZIO,COM HUMANO
A,PAREDE,PAREDE,VAZIO,COM HUMANO
A,PAREDE,VAZIO,PAREDE,COM HUMANO
G,PAREDE,VAZIO,VAZIO,COM HUMANO
A,PAREDE,PAREDE,VAZIO,COM HUMANO
A,PAREDE,VAZIO,PAREDE,COM HUMANO
G,PAREDE,VAZIO,VAZIO,COM HUMANO
A,PAREDE,PAREDE,VAZIO,COM HUMANO
A,VAZIO,PAREDE,VAZIO,COM HUMANO
G,VAZIO,VAZIO,PAREDE,COM HUMANO
G,PAREDE,VAZIO,VAZIO,COM HUMANO
G,VAZIO,VAZIO,VAZIO,COM HUMANO
A,PAREDE,PAREDE,VAZIO,COM HUMANO
E,PAREDE,PAREDE,VAZIO,SEM CARGA
Missao concluida
``` 

### `mapa.txt`
Contém a definição do layout do labirinto. Cada célula no mapa é representada por um caractere, como descrito anteriormente. O arquivo é lido pelo programa para configurar o ambiente.

Exemplo de mapa:
```
***E***
*     *
* *****
*     *
***** *
*     *
* *** *
* *  H*
*******
```

### `tests/`
Este diretório contém testes unitários para as classes `Labirinto` e `Robo`. Os testes são implementados usando o módulo `unittest`.

- `test_labirinto.py`: Testa as funcionalidades do labirinto, como carregar o mapa, verificar a validade de posições, e manipular a posição do humano.
- `test_robo.py`: Testa as funcionalidades do robô, incluindo movimentação, coleta de humanos, e detecção de colisões.

## Execução

-  Execute o script principal `main.py`:

```bash
python main.py
```

## Testes
Para rodar os testes unitários, utilize o seguinte comando:
```bash
python -m coverage run -m unittest discover
```

## Requisitos
- Python 3.8 ou superior
- Bibliotecas padrão do Python (sem dependências externas)
