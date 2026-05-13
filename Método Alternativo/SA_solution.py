import numpy as np

# Modelando o problema -----------------------------------------------------------------------------------------

# Parâmetros globais

p = 30  # Número total de alunos
n = 3  # Número de provas a serem realizadas
m = 4   # Número de horários disponíveis

# Conjuntos iniciais:

A = np.arange(p)    # Conjunto de alunos, de tamanho p (indíce 0 à p-1, com A[0] = 0, E[1] = 1, etc.)

E = np.arange(n)    # Conjunto de provas, de tamanho n (indíce 0 à n-1, com E[0] = 0, E[1] = 1, etc.)

T = np.arange(m)    # Conjunto de horários, de tamanho m (indíce 0 à m-1, com E[0] = 0, E[1] = 1, etc.)

c = np.zeros((n,n)) # Criação de matriz auxiliar - elemento ij representa quantos alunos farão a prova i e j

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



