import math
import random

# DEKLARASI GLOBAL
tabpop = {  # populasi random
    'kromosom': [],
    'fitness': []
}

newPop = {  # populasi hasil rekayasa
    'kromosom': [],
    'fitness': []
}

bestKrom = {
    'generasi': [],
    'kromosom': [],
    'fitness': []
}

# inisiasi batas interval x1 dan x2
interval_x1 = [-10, 10]
interval_x2 = [-10, 10]

# ukuran populasi
n_kromosom = 10
n_gen = 10
generasi = 10

# probabilitas operasi genetik (pc dan pm)
prob_crossover = 0.8
prob_mutasi = 0.01

# random kromosom
def randKrom(n_gen):
    tabkrom = []
    for i in range(n_gen):
        tabkrom.append(random.randint(0, 1))
    return tabkrom

# populasi untuk menampung kromosom
def buat_populasi(n_krom, n_gen, tabpop):
    for i in range(n_krom):
        tabpop['kromosom'].append(randKrom(n_gen))

# fungsi
def fungsi(x1, x2):
    h = - (math.sin(x1) * math.cos(x2) + (4/5) * math.exp(1 - math.sqrt(x1**2 + x2**2)))
    return h

# metode dekode kromosom
def decodeKrom(kromosom, interval):  # binary decoding
    jml_kali = 0
    jml_penyebut = 0
    for i in range(len(kromosom)):
        genotif = kromosom[i]
        jml_kali += (genotif * (2**-(i+1)))
        jml_penyebut += (2**-(i+1))

    return interval[0] + (((interval[1] - interval[0]) / jml_penyebut) * jml_kali)

# membagi array menjadi 2 gamet: x1 dan x2
def split(kromosom):
    return (kromosom[:len(kromosom)//2], kromosom[len(kromosom)//2:])

# nilai fitness
def fitness(h):
    a = 0.0000000001
    return 1 / (h + a)

# perhitungan fitness
def hitungFitness(tabpop):
    for i in range(len(tabpop['kromosom'])):
        x1, x2 = split(tabpop['kromosom'][i])
        gamet_x1 = decodeKrom(x1, interval_x1)
        gamet_x2 = decodeKrom(x2, interval_x2)
        f = fitness(fungsi(gamet_x1, gamet_x2))
        tabpop['fitness'].append(f)

# pemilihan orang tua menggunakan roulette wheel selection
def RouletteWheelSelection(tabpop):
    total = 0
    for indv in range(len(tabpop['kromosom'])):
        total += tabpop['fitness'][indv]

    r = random.random()
    indv = 0
    while r > 0 and indv < len(tabpop['kromosom']):
        r -= tabpop['fitness'][indv] / total
        indv += 1
    return tabpop['kromosom'][indv - 1]

# crossover single point
def crossover(parent1, parent2, prob):
    child1 = []
    child2 = []

    # mencari nilai random
    nilai = random.random()

    if nilai < prob:
        p = random.randint(1, len(parent1) - 1)  # mencari titik silang

        # offspring 1
        child1[:p] = parent1[:p]
        child1[p:] = parent2[p:]

        # offspring 2
        child2[:p] = parent2[:p]
        child2[p:] = parent1[p:]

    else:
        child1 = parent1
        child2 = parent2

    return (child1, child2)

# mutasi
def mutasi(krom, prob):

    for i in range(len(krom)):
        # mencari nilai random
        r = random.random()
        if r <= prob:
            if krom[i] == 0:
                krom[i] = 1
            else:
                krom[i] = 0
    return krom

# seleksi survivor
def elitism(tabpop, newpop):

    # mencari bibit unggul ke 1
    best1 = max(tabpop['fitness'])
    idx_best1 = tabpop['fitness'].index(best1)

    newpop['kromosom'].append(tabpop['kromosom'][idx_best1])
    newpop['fitness'].append(tabpop['fitness'][idx_best1])

    # mencari bibit unggul ke 2
    i = 0
    best2 = 0
    while i < len(tabpop['kromosom']):
        if tabpop['fitness'][i] > best2 and tabpop['fitness'][i] < best1:
            best2 = tabpop['fitness'][i]
        i += 1

    idx_best2 = tabpop['fitness'].index(best2)
    newpop['kromosom'].append(tabpop['kromosom'][idx_best2])
    newpop['fitness'].append(tabpop['fitness'][idx_best2])

    return newpop

# PROGRAM UTAMA
# Pergantian Generasi dengan Generational Model
buat_populasi(n_kromosom, n_gen, tabpop)  # membuat populasi random
hitungFitness(tabpop)  # menghitung fitness setiap kromosom pada populasi

g = 1
while (g <= generasi):  # kondisi penghentian

    newPop = {  # populasi hasil rekayasa
        'kromosom': [],
        'fitness': []
    }

    # menampilkan tabel populasi
    print(">>>> POPULASI GENERASI KE", g, "<<<<")
    print()
    print('-' * 120)
    print('No.', '\t|', '{:<33}{:<3}{:<22}{:<3}{:<22}{:<3}{:<22}'.format('Kromosom', '|', 'Fenotif x1', '|',
                                                                        'Fenotif x2', '|', 'Nilai Fitness'))
    print('-' * 120)

    TK = dict(tabpop)
    for j in range(len(TK['kromosom'])):
        x1, x2 = split(TK['kromosom'][j])

        print(j + 1, '\t| ', TK['kromosom'][j], '| ', '{:<22}{:<3}{:<22}{:<3}{:<22}'.format(
            decodeKrom(x1, interval_x1), '| ', decodeKrom(x2, interval_x2), '| ', TK['fitness'][j]))

    print('-' * 120)
    print()

    # menyeleksi 2 bibit dengan fitness tertinggi
    newPop = elitism(tabpop, newPop)

    # menyimpan data bibit terunggul
    bestKrom['generasi'].append(g)
    bestKrom['kromosom'].append(newPop['kromosom'][0])
    bestKrom['fitness'].append(newPop['fitness'][0])

    while len(newPop['kromosom']) < n_kromosom:
        # menyeleksi parent
        parent1 = RouletteWheelSelection(tabpop)
        parent2 = RouletteWheelSelection(tabpop)

        # crossover
        ofs1, ofs2 = crossover(parent1, parent2, prob_crossover)

        # mutasi
        ofs1 = mutasi(ofs1, prob_mutasi)
        ofs2 = mutasi(ofs2, prob_mutasi)

        newPop['kromosom'].append(ofs1)
        newPop['kromosom'].append(ofs2)

    hitungFitness(newPop)
    tabpop = newPop
    g += 1

# Tampilan piranti
print("KROMOSOM TERBAIK DENGAN NILAI FUNGSI MINIMUM PADA TIAP GENERASI")
print("")
print('-' * 122)
print('{:<16}{:<3}{:<31}{:<3}{:<22}{:<3}{:<22}{:<3}{:<22}'.format('Generasi ke-', '|', 'Kromosom', '|',
                                                                    'Fenotif x1', '|', 'Fenotif x2', '|', 'Nilai Fitness'))
print('-' * 122)
DPX = dict(bestKrom)
for i in range(len(DPX['generasi'])):
    x1, x2 = split(DPX['kromosom'][i])

    print(DPX['generasi'][i], '\t\t| ', DPX['kromosom'][i], '| ', '{:<22}{:<3}{:<22}{:<3}{:<22}'.format(
        decodeKrom(x1, interval_x1), '| ', decodeKrom(x2, interval_x2), '| ', DPX['fitness'][i]))

print('-' * 122)

# Mencari letak generasi solusi
k = 0
max_fit = 0.0
idx_max = 0
while(k < len(bestKrom['generasi'])):
    if (bestKrom['fitness'][k] > max_fit):
        max_fit = bestKrom['fitness'][k]
        idx_max = k
    k += 1

# Menampilkan solusi terbaik
print()
print("Solusi kromosom terbaik pada populasi adalah", bestKrom['kromosom'][idx_max])
print("dengan nilai fitness =", max_fit, "terdapat pada generasi ke-", bestKrom['generasi'][idx_max])

gamet_x1, gamet_x2 = split(bestKrom['kromosom'][idx_max])
x1 = decodeKrom(x1, interval_x1)
x2 = decodeKrom(x2, interval_x2)
print("Nilai x1 :", x1)
print("Nilai x2 :", x2)
print("Hasil fungsi :", fungsi(x1, x2))
