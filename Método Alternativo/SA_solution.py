import numpy as np
import random
import math

def custo(solucao: list[int], conflitos: list[tuple[int,int,int]], custos: list[list[int]]) -> int:
    """
    Função que calcula o custo total para a implementação de uma solução
    
    Args:
        solucao:
            Solução encontrada;
        
        conflitos:
            Lista de conflitos, no formato: (horario da prova i, horario da prova j, número de conflitos)
        
        custos:
            Matriz de custos no formato custos[i][j] => Custo de fazer uma prova no horario i e outra no horario j

    Returns:
        int:
            Custo total da solução

    """

    total = 0   # Variável para armazenar o valor do custo total

    # Percorre toda a lista de conflitos, recuperando 
    for i, j, conflito in conflitos:
        horario_i = solucao[i]  # Recupera o horário em que a prova i ocorre
        horario_j = solucao[j]  # Recupera o horário em que a prova j ocorre

        total += (conflito * custos[horario_i][horario_j])   # Calcula o custo de relizar essas provas nestes horários
    return total


def gerar_vizinho(solucao_atual: list[int], len_Provas: int, len_Horarios: int) -> list[int]:
    """
    Gera uma solução vizinha à atual.

    Args:
        solucao_atual:
            Solução atual, a qual se deseja criar uma vizinha
        
        len_Provas:
            Tamanho do conjunto de provas, no formato Provas[i] = i

        len_Horarios:
            Tamanho do conjunto de horarios, no formato horarios[i] = i
    
    Returns:
        list[int]:
            Retorna  uma solução vizinha.
    """

    # Copia a solução atual
    nova_sol = solucao_atual.copy()

    # Escolhe uma prova do conjunto de provas
    prova = random.randint(0, len_Provas - 1)

    # Escolhe um horário do conjunto de horários
    novo_hr = random.randint(0, len_Horarios - 1)

    # Faz a reatribuição da prova para o horário escolhidos
    nova_sol[prova] = novo_hr

    return nova_sol

def simulated_annealing(initial_sol: list[int],
                        conflitos: list[tuple[int,int,int]],
                        Provas_len: int,
                        Horarios_len: int,
                        custos: list[list[int]],
                        T_start: float = 1000, 
                        T_end: float = 0.1, 
                        alpha: float = 0.95) -> tuple[list[int], int]:
    """
    Aplica a meta-heurística do Simulated Annealing

    Args:
        initial_sol:
            Solução inicial do problema
        
        conflitos:
            Lista de conflitos no formato conflito[x] = (horario i, horario j, custo de fazer prova em i e outra em j)
        
        Provas_len:
            Tamanho do conjunto de provas

        Horarios_len:
            Tamanhodo conjunto de horarios
        
        custos:
            Matriz de custos no formato matriz[i][j] = custo de fazer uma prova no horario i e outra em j
        
        T_start:
            Temperatura inicial
        
        T_end:
            Temperatura final
        
        alpha:
            Fator de redução da temperatura
        
    Returns:
        tuple[list[int],int]:
            Retorna uma tupla no formato => nova solução, custo da nova solução.
    """
    # Copia a solução inicial e seu custo, formando o ponto de partida
    atual = initial_sol.copy()
    custo_atual = custo(atual,conflitos,custos)

    # Valor iniciais da melhor solução e melhor custos são iguais ao da solução inicial
    melhor = atual.copy()
    melhor_custo = custo_atual

    # Temperatura atual == Temperatura de inicio
    T_cur = T_start

    # Atua enquanto a temperatura atual for maior que o limite estabelecido
    while T_cur > T_end:

        # Gera uma solução vizinha e encontra seu custo
        neighbor = gerar_vizinho(atual,Provas_len,Horarios_len)
        neighbor_cost = custo(neighbor,conflitos,custos)

        # Verifica a variação do custo
        delta = neighbor_cost - custo_atual

        # Probabilidade de aceitar a nova solução
        prob = math.exp(-delta/T_cur)

        # Aceita a solução, se esta for melhor que a atual ou se o número gerado for menor do que a probabilidade de ser aceita
        if delta < 0 or random.random() < prob:
            atual = neighbor.copy()
            custo_atual = neighbor_cost

        # Caso a solução atual seja melhor que a última melhor encontrada, atualiza os dados
        if custo_atual < melhor_custo:
            melhor = atual.copy()
            melhor_custo = custo_atual
        
        # Decrementa a temperatura por um fator alpha
        T_cur *= alpha

    return melhor, melhor_custo


def main():

    # Modelando o problema ------------------------------------------------------------------------

    # Parâmetros para geração dinâmica
    p = 30  # Número total de alunos
    n = 3   # Número de provas a serem realizadas
    m = 4   # Número de horários disponíveis

    # Utiliza valores padrão para comparação das respostas
    if(DEFAULT_VALS):

        # Conjuntos iniciais:

        Alunos = np.arange(30)   # Conjunto de alunos, de tamanho 30 (indíce 0 à 29, com A[0] = 0, E[1] = 1, etc.)

        Provas = np.arange(3)    # Conjunto de provas, de tamanho 3 (indíce 0 à 2, com E[0] = 0, E[1] = 1, etc.)

        Horarios = np.arange(4)  # Conjunto de horários, de tamanho 4 (indíce 0 à 3, com E[0] = 0, E[1] = 1, etc.)

        c = np.zeros((3,3)) # Criação de matriz auxiliar - elemento ij representa quantos alunos farão a prova i e j

        # Quantidade de alunos por prova
        c[0][0] = 18
        c[1][1] = 20
        c[2][2] = 16

        # Conflitos entre provas - matriz deve ser simétrica c[i][j] == c[j][i]
        c[0][1] = 7
        c[1][0] = 7

        c[0][2] = 5
        c[2][0] = 5

        c[1][2] = 9
        c[2][1] = 9

        # Matriz de custos
        w = np.array(
            [
                [100, 10, 5 , 1],
                [10, 100, 10 , 5],
                [5, 10, 100 , 10],
                [1, 5, 10 , 100]
            ]
        )

        # Solução inicial (ponto de ínicio do Simulated Annealing)
        solucao = [1,2,0]   # Formato: solucao[i] == horário em que a prova i será realizada

    # Gera valores dinâmicos
    else:

        Alunos = np.arange(p)    # Conjunto de alunos, de tamanho p (indíce 0 à p-1, com A[0] = 0, E[1] = 1, etc.)

        Provas = np.arange(n)    # Conjunto de provas, de tamanho n (indíce 0 à n-1, com E[0] = 0, E[1] = 1, etc.)

        Horarios = np.arange(m)    # Conjunto de horários, de tamanho m (indíce 0 à m-1, com E[0] = 0, E[1] = 1, etc.)

        c = np.zeros((n,n)) # Criação de matriz auxiliar - elemento ij representa quantos alunos farão a prova i e j

        # Gera conflitos aleatórios
        for i in range(0,n):

            # Utiliza da simetria da matriz para reduzir o custo computacional
            for j in range(i + 1, n):
                c[i][j] = c[j][i] = np.random.randint(0,p)

        # Matriz de custos
        w = np.zeros((m,m)) # De tamanho mXm pois é o custo pra fazer um aprova no horário i e outra no j. Ou seja, se i == j há conflito e o custo é máximo

        max_cost = 50 * (m) # Custo máximo, onde i == j. Trabalhamos com múltiplos de 50, logo o máx é 50 * n° de horários
        aux = 0             # Variável auxiliar

        for i in range(0,m):
            aux = max_cost

            # Utiliza da simetria da matriz para reduzir o custo computacional
            for j in range(i,m):
                w[i][j] = w[j][i] = aux
                aux -= 50   # Decrementa o custo


        # Gera uma solução inicial aleatória
        solucao = np.arange(n)  # Formato: solucao[i] == horário em que a prova i será realizada
        for i in range(n):
            solucao[i] = np.random.randint(0,m) # Valor máximo == prova m-1


    # Cria lista de conflitos no formato (prova_i, prova_j, n° de alunos que farão i e j)
    conflitos = []
    for i in range(0,len(Provas)):
        
        # Pula as diagonais pois nos interessamos apenas em provas distintas (i!=j) e usa da simetria da matriz pra aumentar a eficácia
        for j in range(i + 1,len(Provas)):
            if c[i][j] > 0:
                conflitos.append((i,j,c[i][j]))

    # Função que calcula o custo de relizar as provas nos horários especificados


    # ---------------------------------------------------------------------------------------------

    # Otimizando o resultado através de Simulated Annealing ---------------------------------------

    # Gera a nova solução
    new_sol, new_cost = simulated_annealing(solucao, conflitos,len(Provas), len(Horarios), w, alpha=0.99)

    # Exibe a solução e o custo final
    print(f"Solução final encontrada => {new_sol}")
    print(f"Custo da solução: {new_cost}")


# Main --------------
DEFAULT_VALS = True

main()
# -------------------