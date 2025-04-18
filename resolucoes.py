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
def edit_distance_recursive(a, b):
    count = [0]

    def dist(i, j):
        count[0] += 1
        if i == 0: return j
        if j == 0: return i
        if a[i - 1] == b[j - 1]:
            return dist(i - 1, j - 1)
        return 1 + min(
            dist(i - 1, j),
            dist(i, j - 1), 
            dist(i - 1, j - 1) 
        )

    result = dist(len(a), len(b))
    return result, count[0]

def edit_distance_dp(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    iter_count = 0

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            iter_count += 1
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n], iter_count

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

    capacidade2 = 190
    pesos2 = [56, 59, 80, 64, 75, 17]
    valores2 = [50, 50, 64, 46, 50, 5]
    itens2 = list(zip(pesos2, valores2))

    res_pd_2, count_pd_2 = backPackPD(len(itens2), capacidade2, itens2)
    res_bf_2, count_bf_2 = knapsack_brute_force(itens2, capacidade2)

    print(f"[CASO 2] Capacidade: {capacidade2}")
    print(f"PD         → Valor ótimo: {res_pd_2} | Iterações: {count_pd_2}")
    print(f"Força Bruta→ Valor ótimo: {res_bf_2} | Iterações: {count_bf_2} (Valor esperado: 150)")

def testar_edicao():
    print("\n=== Distância de Edição ===")
    casos = [
        ("Casablanca", "Portentoso"),
        ("Maven, a Yiddish word meaning accumulator of knowledge, began as an attempt to " +
   			"simplify the build processes in the Jakarta Turbine project. There were several" + 
   			" projects, each with their own Ant build files, that were all slightly different." +
   			"JARs were checked into CVS. We wanted a standard way to build the projects, a clear "+ 
   			"definition of what the project consisted of, an easy way to publish project information" +
   			"and a way to share JARs across several projects. The result is a tool that can now be" +
   			"used for building and managing any Java-based project. We hope that we have created " +
   			"something that will make the day-to-day work of Java developers easier and generally help " +
   			"with the comprehension of any Java-based project.",
         "This post is not about deep learning. But it could be might as well. This is the power of " +
   			"kernels. They are universally applicable in any machine learning algorithm. Why you might" +
   			"ask? I am going to try to answer this question in this article." + 
   		        "Go to the profile of Marin Vlastelica Pogančić" + 
   		        "Marin Vlastelica Pogančić Jun")
    ]

    for idx, (s1, s2) in enumerate(casos, 1):
        print(f"\n--- Caso {idx} ---")
        print(f"Strings: {s1[:30]}... x {s2[:30]}...")

        dist_rec, iter_rec = edit_distance_recursive(s1, s2) if len(s1) < 20 and len(s2) < 20 else ("(Muito lento)", "(Muito alto)")
        dist_dp, iter_dp = edit_distance_dp(s1, s2)

        print(f"[Recursivo]     Distância: {dist_rec} | Iterações: {iter_rec}")
        print(f"[Prog. Dinâm.] Distância: {dist_dp} | Iterações: {iter_dp}")

if __name__ == "__main__":
    testar_fibonacci()
    testar_mochila()
    testar_edicao()
