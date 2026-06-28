from pyscipopt import Model, quicksum
import random
import time

random.seed(42)

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
    4: "Quarta 08h"

}

T = range(len(num_periodos))

num_alunos = 20

matricula = {}

for aluno in range(num_alunos):

    qtd_disciplinas = random.randint(2,3)

    matricula[aluno] = random.sample(list(E), qtd_disciplinas)

print("\n==============================")
print("MATRÍCULAS GERADAS")
print("==============================")

for aluno in matricula:

    nomes = [num_provas[p] for p in matricula[aluno]]

    print(f"Aluno {aluno}: {nomes}")


# matriz de conflito c_ij


c = {}

for i in E:
    for j in E:

        if i < j:

            alunos_comum = 0

            for aluno in matricula:
                if i in matricula[aluno] and j in matricula[aluno]:
                    alunos_comum += 1
            c[i,j] = alunos_comum

print("\n==============================")
print("MATRIZ DE CONFLITOS")
print("==============================")

for (i,j), valor in c.items():

    if valor > 0:

        print(f"{num_provas[i]} x " f"{num_provas[j]}" f" -> {valor}")


# penalidades

w = {}

for t1 in T:
    for t2 in T:

        dist = abs(t1-t2)

        if dist == 0:
            w[t1,t2] = 0

        elif dist == 1:
            w[t1,t2] = 10

        elif dist == 2:
            w[t1,t2] = 5

        elif dist == 3:
            w[t1,t2] = 1

        else:
            w[t1,t2] = 0


# modelo


model = Model("Exam_Timetabling")

x = {}

for i in E:
    for t in T:

        x[i,t] = model.addVar(vtype="B", name=f"x_{i}_{t}")

y = {}

for i in E:
    for j in E:
        if i<j:
            for t1 in T:
                for t2 in T:
                    if t1!=t2:
                        y[i,j,t1,t2] = model.addVar(vtype="B", name=f"y_{i}_{j}_{t1}_{t2}")


# restrições

for i in E:
    model.addCons(quicksum(x[i,t] for t in T) == 1)

for i in E:
    for j in E:
        if i<j and c[i,j]>0:
            for t in T:
                model.addCons(x[i,t] + x[j,t] <=1)


# linearização das variáveis binárias


for i in E:
    for j in E:
        if i<j:
            for t1 in T:
                for t2 in T:
                    if t1!=t2:
                        model.addCons(y[i,j,t1,t2] <= x[i,t1])
                        model.addCons(y[i,j,t1,t2] <= x[j,t2])
                        model.addCons(y[i,j,t1,t2] >= x[i,t1] + x[j,t2] -1)


# função objetivo

objective = quicksum(c[i,j] * w[t1,t2] * y[i,j,t1,t2] for i in E for j in E if i<j for t1 in T for t2 in T if t1!=t2)

model.setObjective(objective, "minimize")
model.setParam("limits/time", 300)

inicio=time.time()
model.optimize()
tempo=time.time()-inicio

status=model.getStatus()

print("\n==============================")
print("STATUS:",status)
print("==============================")

if status == "optimal" or status == "feasible":

    print("\nValor da função objetivo:")
    print(model.getObjVal())

    print(f"\nTempo: {tempo:.4f} s")

    print(f"GAP: {model.getGap()*100:.4f}%")

    print("\n==============================")
    print("CALENDÁRIO FINAL")
    print("==============================")

    for i in E:
        for t in T:
            if model.getVal(x[i,t]) > 0.5:
                print(f"{num_provas[i]}" f" -> " f"{num_periodos[t]}")

else:

    print("\nNão foi encontrada solução viável.")
    print(f"\nTempo: {tempo:.4f} s")


# estatísticas finais

print("\n==============================")
print("ESTATÍSTICAS")
print("==============================")

print("Número de variáveis:", model.getNVars())
print("Número de restrições:", model.getNConss())
