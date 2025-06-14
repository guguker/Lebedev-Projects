def count_ways(n, k):
    MODUL = 10**9 + 7
    
    ararray = [0] * (n + 1)

    ararray[1] = 1 # c 1 cтупеньки только 1 способ
    
    for i in range(2, n + 1):
        # jump mario!!!
        for j in range(1, min(i, k + 1)):
            ararray[i] = (ararray[i] + ararray[i - j]) % MODUL
            
    return ararray[n]

n, k = map(int, input().split())

print(count_ways(n, k))



