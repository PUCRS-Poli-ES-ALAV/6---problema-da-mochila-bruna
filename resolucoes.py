import sys
from itertools import combinations

fibo_rec_calls = 0
memo_fibo_calls = 0
fibo_iter_ops = 0
memo_iter_ops = 0

#============================================================
def fibo_rec(n):
    global fibo_rec_calls
    fibo_rec_calls += 1
    if n <= 1:
        return n
    return fibo_rec(n - 1) + fibo_rec(n - 2)

def fibo_iter(n):
    global fibo_iter_ops
    f = [0] * (n + 1)
    f[0], f[1] = 0, 1
    fibo_iter_ops += 2
    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]
        fibo_iter_ops += 1
    return f[n]

def memoized_fibo(n):
    global memo_iter_ops
    f = [-1] * (n + 1)
    memo_iter_ops += n + 1
    return lookup_fibo(f, n)

def lookup_fibo(f, n):
    global memo_fibo_calls
    memo_fibo_calls += 1
    if f[n] >= 0:
        return f[n]
    if n <= 1:
        f[n] = n
    else:
        f[n] = lookup_fibo(f, n - 1) + lookup_fibo(f, n - 2)
    return f[n]

#============================================================
def knapsack_brute_force(items, C):
    best_value = 0
    count = 0
    for r in range(1, len(items) + 1):
        for combo in combinations(items, r):
            count += 1
            weight = sum(i[0] for i in combo)
            value = sum(i[1] for i in combo)
            if weight <= C:
                best_value = max(best_value, value)
    return best_value, count

def backPackPD(N, C, itens):
    maxTab = [[0] * (C + 1) for _ in range(N + 1)]
    count = 0
    for i in range(1, N + 1):
        peso, valor = itens[i - 1]
        for j in range(1, C + 1):
            count += 1
            if peso <= j:
                maxTab[i][j] = max(maxTab[i-1][j], valor + maxTab[i-1][j - peso])
            else:
                maxTab[i][j] = maxTab[i-1][j]
    return maxTab[N][C], count

#============================================================
def testar_fibonacci():
    valores = [4, 8, 16, 32, 128, 1000, 10000]
    print("\n=== Fibonacci ===")
    print(f"{'Algoritmo':<15} {'n':<8} {'Resultado':<12} {'Instruções'}")

    for n in valores:
        if n <= 32:
            global fibo_rec_calls
            fibo_rec_calls = 0
            res = fibo_rec(n)
            print(f"{'FIBO-REC':<15} {n:<8} {res:<12} {fibo_rec_calls}")

        global fibo_iter_ops
        fibo_iter_ops = 0
        res = fibo_iter(n)
        print(f"{'FIBO (iter)':<15} {n:<8} {res:<12} {fibo_iter_ops}")

        if n <= 1000:
            global memo_fibo_calls, memo_iter_ops
            memo_fibo_calls = 0
            memo_iter_ops = 0
            try:
                res = memoized_fibo(n)
                total_ops = memo_iter_ops + memo_fibo_calls
                print(f"{'MEMOIZED-FIBO':<15} {n:<8} {res:<12} {total_ops}")
            except RecursionError:
                print(f"{'MEMOIZED-FIBO':<15} {n:<8} {'-':<12} [recursion limit]")
        else:
            print(f"{'MEMOIZED-FIBO':<15} {n:<8} {'-':<12} [recursion limit]")

def testar_mochila():
    print("\n=== Mochila ===")

    # Caso 1
    capacidade1 = 165
    pesos1 = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
    valores1 = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
    itens1 = list(zip(pesos1, valores1))

    res_pd_1, count_pd_1 = backPackPD(len(itens1), capacidade1, itens1)
    res_bf_1, count_bf_1 = knapsack_brute_force(itens1, capacidade1)

    print(f"[CASO 1] Capacidade: {capacidade1}")
    print(f"PD         → Valor ótimo: {res_pd_1} | Iterações: {count_pd_1}")
    print(f"Força Bruta→ Valor ótimo: {res_bf_1} | Iterações: {count_bf_1} (Valor esperado: 309)")
    print("")

    # Caso 2
    capacidade2 = 190
    pesos2 = [56, 59, 80, 64, 75, 17]
    valores2 = [50, 50, 64, 46, 50, 5]
    itens2 = list(zip(pesos2, valores2))

    res_pd_2, count_pd_2 = backPackPD(len(itens2), capacidade2, itens2)
    res_bf_2, count_bf_2 = knapsack_brute_force(itens2, capacidade2)

    print(f"[CASO 2] Capacidade: {capacidade2}")
    print(f"PD         → Valor ótimo: {res_pd_2} | Iterações: {count_pd_2}")
    print(f"Força Bruta→ Valor ótimo: {res_bf_2} | Iterações: {count_bf_2} (Valor esperado: 150)")

testar_fibonacci()
testar_mochila()
