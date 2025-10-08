from collections import deque

def tri_topologique(G):
    V, E = G

    # Calcul des degrés entrants
    deg = {v: 0 for v in V}

    for u in V:
        for v in E[u]:
            deg[v] += 1

    # Trier V topologiquement
    zeros = deque(v for v in V if deg[v] == 0) # File des sommets de deg. 0
    ordre = []                                 # Ordre topo. à construire
    
    while len(zeros) > 0:
        u = zeros.popleft()
        ordre.append(u)

        for v in E[u]:
            deg[v] -= 1

            if deg[v] == 0:
                zeros.append(v)

    return ordre if len(ordre) == len(V) else None

# Exemple
if __name__ == "__main__":
    # Cours obligatoires
    cours = {"IFT159", "IFT187", "IFT203", "IFT209", "IFT215", "IFT232",
             "IFT287", "IFT313", "IFT320", "IFT339", "IFT359", "IFT436",
             "IFT606", "IFT615", "IFT601", "IMN401", "MAT115", "MAT193",
             "STT418"}

    # Préalables: (u, v) indique que le cours u est préalable au cours v
    dependances = {("IFT159", "IFT209"),
                   ("IFT159", "IFT215"),
                   ("IFT159", "IFT232"),
                   ("IFT187", "IFT287"),
                   ("MAT115", "IFT313"),
                   ("IFT159", "IFT320"),
                   ("IFT209", "IFT320"),
                   ("IFT159", "IFT339"),
                   ("IFT159", "IFT359"),
                   ("IFT339", "IFT436"),
                   ("MAT115", "IFT606"),
                   ("IFT436", "IFT615"),
                   ("STT418", "IFT615"),
                   ("IFT232", "IFT601"),
                   ("IFT159", "IMN401"),
                   ("MAT193", "IMN401")}

    # Construire le graphe des dépendances
    V = cours
    E = {v: [] for v in cours}

    for (u, v) in dependances:
        E[u].append(v)

    G = (V, E)

    # Trier les cours topologiquement
    s = tri_topologique(G)

    print("Ordre topologique des cours:")
    print(s)
