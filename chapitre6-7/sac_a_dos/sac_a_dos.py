from fractions import Fraction

def sac_a_dos_glouton(v, p, c):
    ratio   = lambda i: Fraction(v[i], p[i])
    indices = sorted(range(len(v)), key=ratio, reverse=True)
    valeur  = 0
    poids   = 0

    x = [0 for _ in v]

    for i in indices:
        if poids + p[i] <= c:
            valeur += v[i]
            poids  += p[i]
        else:
            break

    return valeur

def sac_a_dos_naif(v, p, c):
    def remplir(i, valeur, poids):
        if i == len(v):
            return valeur if poids <= c else 0
        else:
            valeur_ = valeur + v[i]
            poids_  = poids  + p[i]

            return max(remplir(i + 1, valeur,  poids),  # sans objet i
                       remplir(i + 1, valeur_, poids_)) # avec objet i

    return remplir(0, 0, 0)

def sac_a_dos_elagage(v, p, c):
    def remplir(i, valeur, poids):
        
        if i == len(v):
            return valeur
        else:
            valeur_ = valeur + v[i]
            poids_  = poids  + p[i]

            sol = remplir(i + 1, valeur, poids) # sans objet i

            if poids_ <= c:                     # avec objet i
                sol = max(sol, remplir(i + 1, valeur_, poids_)) 

            return sol
            
    return remplir(0, 0, 0)

def sac_a_dos_turbo(v, p, c):
    num_appels   = 0
    num_completes = 0 
    meilleure = max(max(v), sac_a_dos_glouton(v, p, c))
    potentiel = [sum(v[i:]) for i in range(len(v))]

    def remplir(i, valeur, poids):
        nonlocal meilleure

        meilleure = max(meilleure, valeur)

        if (i < len(v)) and (valeur + potentiel[i] > meilleure):
            valeur_ = valeur + v[i]
            poids_  = poids  + p[i]
                
            remplir(i + 1, valeur, poids)

            if poids_ <= c:
                remplir(i + 1, valeur_, poids_)

    remplir(0, 0, 0)

    return meilleure

def sac_a_dos_dyn(v, p, c):
    n = len(v)
    T = [[0 for _ in range(c + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(c + 1):
            valeur = v[i - 1]
            poids  = p[i - 1]

            a = T[i - 1][j]
            b = T[i - 1][j - poids] + valeur if j >= poids else 0
   
            T[i][j] = max(a, b)

    return T[-1][-1]
    
# Exemple des notes de cours
if __name__ == "__main__":
    def instance(v, p, c):
        print("Instance:")
        print()
        print(f" valeurs  v = {v}")
        print(f" poids    p = {p}")
        print(f" capacité c = {c}")
        print()
        print("Valeur max. (force brute naïve):  ", sac_a_dos_naif(v, p, c))
        print("Valeur max. (force brute élagage):", sac_a_dos_elagage(v, p, c))
        print("Valeur max. (force brute turbo):  ", sac_a_dos_turbo(v, p, c))
        print("Valeur max. (prog. dynamique):    ", sac_a_dos_dyn(v, p, c))

    instance([5, 3, 4],
             [4, 2, 3], 8)
    print()
    instance([ 50,   5,  65, 10,  12,  20],
             [700, 320, 845, 70, 420, 180], 900)

