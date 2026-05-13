import numpy as np

DEFAULT_VALS = True

# Modelando o problema -----------------------------------------------------------------------------------------

# Parâmetros globais

p = 30  # Número total de alunos
n = 3   # Número de provas a serem realizadas
m = 4   # Número de horários disponíveis

# Utiliza valores padrão para comparação das respostas
if(DEFAULT_VALS):

    # Conjuntos iniciais:

    A = np.arange(30)   # Conjunto de alunos, de tamanho 30 (indíce 0 à 29, com A[0] = 0, E[1] = 1, etc.)

    E = np.arange(3)    # Conjunto de provas, de tamanho 3 (indíce 0 à 2, com E[0] = 0, E[1] = 1, etc.)

    T = np.arange(4)    # Conjunto de horários, de tamanho 4 (indíce 0 à 3, com E[0] = 0, E[1] = 1, etc.)

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
        [100, 10, 5 , 1],
        [10, 100, 10 , 5],
        [5, 10, 100 , 10],
        [1, 5, 10 , 100]
    )

# Gera valores diferentes 
else:
    
    A = np.arange(p)    # Conjunto de alunos, de tamanho p (indíce 0 à p-1, com A[0] = 0, E[1] = 1, etc.)

    E = np.arange(n)    # Conjunto de provas, de tamanho n (indíce 0 à n-1, com E[0] = 0, E[1] = 1, etc.)

    T = np.arange(m)    # Conjunto de horários, de tamanho m (indíce 0 à m-1, com E[0] = 0, E[1] = 1, etc.)

    c = np.zeros((n,n)) # Criação de matriz auxiliar - elemento ij representa quantos alunos farão a prova i e j

    # Gera conflitos aleatórios
    for i in range(0,n):

        # Utiliza da simetria da matriz para reduzir o custo computacional
        for j in range(i, n):
            c[i][j] = c[j][i] = np.random.randint(0,p)
            
    # Matriz de custos
    w = np.zeros(m,m)   # De tamanho mXm pois é o custo pra fazer um aprova no horário i e outra no j. Ou seja, se i == j há conflito e o custo é máximo

    max_cost = 50 * (m) # Custo máximo, onde i == j. Trabalhamos com múltiplos de 50, logo o máx é 50 * n° de horários
    aux = 0             # Variável auxiliar
    for i in range(0,m):
        aux = max_cost

        # Utiliza da simetria da matriz para reduzir o custo computacional
        for j in range(i,m):
            w[i][j] = w[j][i] = aux
            aux -= 50   # Decrementa o custo


