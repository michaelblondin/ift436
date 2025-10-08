from topologique import tri_topologique

# Identifie le premier et dernier niveau d'un jeu bien conçu
#  (on suppose qu'on a déjà vérifié qu'il est bien conçu)
def niveaux(G):
    sommets, adj = G

    deg_entrant = {v: 0 for v in sommets}
    deg_sortant = {v: 0 for v in sommets}

    for u in sommets:
        for v in adj[u]:
            deg_entrant[v] += 1
            deg_sortant[u] += 1

    for v in sommets:
        if deg_entrant[v] == 0:
            premier = v
        elif deg_sortant[v] == 0:
            dernier = v

    return (premier, dernier)

# Propagation vers l'avant avec tri toplogique
def solution1(G):
    sommets, adj = G

    # Ordonner les sommets topologiquement
    ordre   = tri_topologique(G)
    premier = ordre[0]
    dernier = ordre[-1]

    # Calculer scores optimaux vers l'avant
    score = {v: 0 for v in sommets}
    score[premier] = 1

    for u in ordre:
        for v in adj[u]:
            score[v] = max(score[v], score[u] + 1)

    return score[dernier]

# Propagation vers l'arrière avec tri toplogique
def solution2(G):
    sommets, adj = G

    # Ordonner les sommets en ordre topologique inverse
    ordre   = tri_topologique(G)
    premier = ordre[0]
    dernier = ordre[-1]

    ordre.reverse()

    # Calculer scores optimaux vers l'arrière
    score = {v: 0 for v in sommets}
    score[dernier] = 1

    for u in ordre:
        for v in adj[u]:
            score[u] = max(score[u], score[v] + 1)

    return score[premier]

# Propagation vers l'avant récursive
#  (Attention: ne fonctionne pas si on marque les sommets,
#              et fonctionne en temps exponentiel sans marquage)
def solution3(G):
    sommets, adj = G
    premier, dernier = niveaux(G)

    marque = {v: False for v in sommets}
    score  = {v: 0     for v in sommets}
    
    score[premier] = 1

    def calculer_score(u):
        if not marque[u]: # Si déjà traité, ne pas retraiter
            # marque[u] = True # Brise l'algorithme si on marque les sommets

            for v in adj[u]:
                score[v] = max(score[v], score[u] + 1)
                
                calculer_score(v)            

    calculer_score(premier)

    return score[dernier]

# Propagation vers l'arrière récursive (avec renversement des arêtes)
#  (Attention: ne fonctionne pas si on marque les sommets,
#              et fonctionne en temps exponentiel sans marquage)
def solution4(G):
    sommets, adj = G
    premier, dernier = niveaux(G)

    # Obtenir liste d'adjacence inversée
    adj_ = {v: [] for v in sommets}

    for u in sommets:
        for v in adj[u]:
            adj_[v].append(u)

    # Propager le score optimal
    marque = {v: False for v in sommets}
    score  = {v: 0     for v in sommets}
    
    score[dernier] = 1

    def calculer_score(u):
        if not marque[u]: # Si déjà traité, ne pas retraiter
            # marque[u] = True # Brise l'algorithme si on marque les sommets

            for v in adj_[u]:
                score[v] = max(score[v], score[u] + 1)
                
                calculer_score(v)

    calculer_score(dernier)

    return score[premier]

# Calcul récursif vers l'arrière
def solution5(G):
    sommets, adj = G
    premier, dernier = niveaux(G)

    score = {v: 0 for v in sommets}
    score[dernier] = 1

    def calculer_score(u):
        if score[u] != 0:   # Si meilleur score déjà connu, ne pas recalculer
            return score[u] #             pour éviter complexité exponentielle
        else:               # Sinon, trouver le meilleur score récursivement
            meilleur = 0

            for v in adj[u]:
                meilleur = max(meilleur, calculer_score(v) + 1)

            score[u] = meilleur

            return meilleur

    return calculer_score(premier)

# Calcul récursif vers l'avant (en renversant les arêtes)
def solution6(G):
    sommets, adj = G
    premier, dernier = niveaux(G)

    # Obtenir liste d'adjacence inversée
    adj_ = {v: [] for v in sommets}

    for u in sommets:
        for v in adj[u]:
            adj_[v].append(u)

    # Calculer score optimal
    score = {v: 0 for v in sommets}
    score[premier] = 1

    def calculer_score(u):
        if score[u] != 0:   # Si meilleur score déjà connu, ne pas recalculer
            return score[u] #             pour éviter complexité exponentielle
        else:               # Sinon, trouver le meilleur score récursivement
            meilleur = 0

            for v in adj_[u]:
                meilleur = max(meilleur, calculer_score(v) + 1)

            score[u] = meilleur

            return meilleur

    return calculer_score(dernier)

# Exemple
if __name__ == "__main__":
    # Graphe du devoir 2, mais en imaginant un monde comme un seul niveau
    sommets = ["ciel", "cité", "début", "fin", "forêt"]
    adj = {"début": ["ciel", "cité"],
           "ciel":  ["fin"],
           "cité":  ["ciel", "forêt"],
           "forêt": ["fin"],
           "fin":   []}
    G = (sommets, adj)

    # adj["ciel"].append("forêt") # La solution augmente à 5 avec cette arête

    print("Score maximal:")
    print(" Solution 1:", solution1(G))
    print(" Solution 2:", solution2(G))
    print(" Solution 3:", solution3(G))
    print(" Solution 4:", solution4(G))
    print(" Solution 5:", solution5(G))
    print(" Solution 6:", solution6(G))
    print()
