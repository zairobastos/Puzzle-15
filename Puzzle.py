import sys
import argparse
from Class import Tabuleiro
from buscas import bfs, dfs, astar, guloso, hamming, manhattan


def main():
    # Argumentos da entrada do script
    parser = argparse.ArgumentParser(description='Programa que resolve o jogo do 15.')
    parser.add_argument('--dfs', type=int,
                        help='Para executar a busca por profundidade')
    parser.add_argument('--bfs', action='store_true',
                        help='Para executar a busca em largura')
    parser.add_argument('--astar', '--a', type=int, choices=[1, 2],
                        help='Executa a busca A* (1 -hamming; 2 -manhattan)')
    parser.add_argument('--gulosa', '--gulosa', type=int, choices=[1, 2],
                        help='Executa a busca gulosa (1 -hamming; 2 -manhattan)')

    parser.add_argument('--input', '-i', help='Especifica um arquivo de entradas para testes')
    args = parser.parse_args()

    # Ler tabuleiro de entrada como argumento ou a digitação do estado
    if args.input is None:
        # terminal
        inicialState = input("Valores de inicialização do tabuleiro:\n").split()
        goalState = input("Tabuleiro objetivo:\n").split()
    else:
        # file
        try:
            numbers = []
            with open(args.input, "r") as f:
                lines = f.readlines()
                for line in lines:
                    numbers = numbers + line.split()
            inicialState = numbers[:16]
            numbers = numbers[16:]
            goalState = numbers[:16]
        except FileNotFoundError:
            sys.stderr.write("Caminho de arquivo inválido")
            sys.exit(1)

    # iniciar tabuleiros manualmente
    inicialState = Tabuleiro(inicialState)
    goalState = Tabuleiro(goalState)
    print(inicialState)
    print(goalState)

    if inicialState == goalState:
        print("Ambos iguais, portanto já está resolvido!")
        sys.exit(0)

    if inicialState.solucao() ^ goalState.solucao():
        print('Tabuleiro inválido.')
        sys.exit(1)

    # Testes dos argumentos para verificação dos
    if args.astar is None and not args.bfs and args.dfs is None and args.gulosa is None:
        sys.stderr.write("Forneça uma entrada válida.")
        sys.stderr.write("Escolha pelo menos um algoritmo para resolver.")
        sys.exit(1)

    if inicialState == goalState:
        print("Ambos iguais. Já resolvido!")
        sys.exit(0)

    if args.dfs is not None:
        if args.dfs < 0:
            parser.print_help(sys.stderr)
            sys.exit(1)
        print("Pesquisa em profundidade:")
        moves, nodes= dfs(inicialState, goalState, args.dfs)
        print("Total: ",nodes, "nós utilizados.")
        if moves:
            print("Caminho para o objetivo:")
            print(" ==> ".join(moves))
        else:
            print("Nenhuma solução encontrada.")

    if args.bfs:
        print("Pesquisa em largura:")
        moves, nodes = bfs(inicialState, goalState)
        print("Total: ",nodes, "nós utilizados.")
        if moves:
            print("Caminho para o objetivo:")
            print(" ==> ".join(moves))
        else:
            print("Nenhuma solução encontrada.")

    if args.astar:
        print("Buca A*:")
        comp = manhattan
        if args.astar == 1:
            comp = hamming
        moves, nodes = astar(inicialState, goalState, comp)
        print("Total: ",nodes, "nós usados com o algoritmo.", comp)
        if moves:
            print("Caminho para o objetivo:")
            print(" ==> ".join(moves))
        else:
            print("Nenhuma solução encontrada.")

    if args.gulosa:
        print("Busca Gulosa:")
        comp = manhattan
        if args.astar == 1:
            comp = hamming
        moves, nodes = guloso(inicialState, goalState, comp)
        print("Total: ",nodes, "nós usados com o algoritmo.", comp)
        if moves:
            print("Caminho para o objetivo:")
            print(" ==> ".join(moves))
        else:
            print("Nenhuma solução encontrada.")


if __name__ == '__main__':
    main()
