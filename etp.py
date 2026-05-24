from pyscipopt import Model, quicksum

# ==========================================================
# Geração de uma instância fixa para testes
# ==========================================================

num_provas = {

    0: "Circuitos Eletrônicos 1",
    1: "Fundamentos de Controle",
    2: "Ondas Eletromagnéticas",
    3: "Programação Matemática",
    4: "Estatística 1",
    5: "Processamento Digital de Sinais",
    6: "Sistemas Operacionais 1"
}

E = range(len(num_provas))

num_periodos = {
    0: "Segunda 08h",
    1: "Segunda 14h",
    2: "Terça 08h",
    3: "Terça 14h",
    4: "Quarta 08h",
    5: "Quarta 14h",
    6: "Quinta 08h",
    7: "Quinta 14h",
    8: "Sexta 08h",
    9: "Sexta 14h"
}

T = range(len(num_periodos))

# ==========================================================
# Alocação das matrículas de uma turma com 19 alunos 
# ==========================================================

# matricula[x] = vetor/lista de provas referntes ao aluno x

matricula = {
    
    0: [0, 1, 3],
    1: [0, 2, 4],
    2: [1, 3, 5],
    3: [0, 4, 6],
    4: [2, 3, 5],
    5: [1, 4, 6],
    6: [0, 2, 5],
    7: [1, 3, 6],
    8: [0, 4, 5],
    9: [2, 3, 6],
    10: [0, 1, 5],
    11: [2, 4, 6],
    12: [1, 3, 4],
    13: [0, 2, 6],
    14: [1, 5, 6],
    15: [0, 3, 4],
    16: [2, 4, 5],
    17: [1, 2, 3],
    18: [0, 5, 6],
    19: [3, 4, 6]
}

# ==========================================================
# Matriz de conflito: c_{ij}
# ==========================================================

c = {}

for i in E:
    for j in E:
        if i < j:
            alunos_comum = 0
            for aluno in matricula:
                if i in matricula[aluno] and j in matricula[aluno]:
                    alunos_comum += 1
            c[i, j] = alunos_comum

# ==================================================================
# Matriz das penalidades/punições baseada nas distância entre provas
# ==================================================================

# O cálculo das penalidades foi feito seguindo um padrão arbitrário descrescente (ou seja, quanto mais próximas, maior a punição)

w = {}

for t1 in T:
    for t2 in T:
        dist = abs(t1 - t2)

        if dist == 0:
            w[t1, t2] = 1000
        elif dist == 1:
            w[t1, t2] = 10
        elif dist == 2:
            w[t1, t2] = 5
        elif dist == 3:
            w[t1, t2] = 1
        else:
            w[t1, t2] = 0

# ==========================================================
# Modelo + variáveis x_{it} e y_{ijtt'}
# ==========================================================

model = Model("Exam_Timetabling")

x = {}

for i in E:
    for t in T:
        x[i, t] = model.addVar(vtype="B", name=f"x_{i}_{t}")

y = {}

for i in E:
    for j in E:
        if i < j:
            for t1 in T:
                for t2 in T:
                    y[i, j, t1, t2] = model.addVar(vtype="B", name=f"y_{i}_{j}_{t1}_{t2}")

# ==========================================================
# R1: cada prova deve ocorrer exatamente uma vez
# ==========================================================

for i in E:

    model.addCons(quicksum(x[i, t] for t in T) == 1, name=f"exam_once_{i}")

# ==========================================================
# R2: Sem conflitos simultâneos
# ==========================================================

for i in E:
    for j in E:
        if i < j and c[i, j] > 0:
            for t in T:
                model.addCons(x[i, t] + x[j, t] <= 1, name=f"conflict_{i}_{j}_{t}")

# ==========================================================
# Restrições de linearização
# ==========================================================

for i in E:
    for j in E:
        if i < j:
            for t1 in T:
                for t2 in T:

                    model.addCons(y[i, j, t1, t2] <= x[i, t1])
                    model.addCons(y[i, j, t1, t2] <= x[j, t2])
                    model.addCons(y[i, j, t1, t2] >= x[i, t1] + x[j, t2] - 1)

# ==========================================================
# Obtenção dos resultados
# ==========================================================

objective = quicksum(c[i, j] * w[t1, t2] * y[i, j, t1, t2] for i in E for j in E if i < j for t1 in T  for t2 in T)
model.setObjective(objective, "minimize")

model.setParam("limits/time", 300) # limite proposto de 300s para execução do modelo

model.optimize()

print("\n==============================")
print("STATUS:", model.getStatus())
print("==============================")

print("\nValor da função objetivo:")
print(model.getObjVal())

print("\n==============================")
print("CALENDÁRIO FINAL")
print("==============================")

for i in E:
    for t in T:
        if model.getVal(x[i, t]) > 0.5:
            print(f"Prova {i} -> Horário {t}")

print("\n==============================")
print("ESTATÍSTICAS")
print("==============================")

print("Número de variáveis:", model.getNVars())
print("Número de restrições:", model.getNConss())
