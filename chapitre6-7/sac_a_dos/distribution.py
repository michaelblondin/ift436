from sac_a_dos import sac_a_dos_glouton
from random    import randint

# Classe représentant un arbre (avec exportation vers code LaTeX)
class Arbre:
    def __init__(self, val, gauche=None, droite=None):
        self.val    = val
        self.gauche = gauche
        self.droite = droite

    @staticmethod
    def code_enfant(x, opacite=1.0):
        if x is not None:
            return ("  child[blue, opacity={}]".format(opacite) + \
                    " {" + Arbre.code(x, False, opacite) + "}")
        else:
            return ""
        
    @staticmethod
    def code(x, init=False, opacite=1.0):
        fst = "\\" if init else ""
        lst = ";"  if init else ""

        return (fst +\
                f"node[blue, fill=blue, "\
                f"opacity={opacite}, fill opacity={opacite}] " +\
                "{}" +
                Arbre.code_enfant(x.gauche, opacite) + " " +\
                Arbre.code_enfant(x.droite, opacite) + lst)

    def __str__(self):
        return Arbre.code(self, init=True, opacite=1.0)

# Algorithmes modifiés pour retourner leur arbre de récursion
def sac_a_dos_naif(v, p, c):
    def remplir(i, valeur, poids):
        if i == len(v):
            return Arbre(valeur if poids <= c else 0)
        else:
            valeur_ = valeur + v[i]
            poids_  = poids  + p[i]

            gauche  = remplir(i + 1, valeur,  poids)  # sans objet i
            droite  = remplir(i + 1, valeur_, poids_) # avec objet i

            return Arbre(max(gauche.val, droite.val), gauche, droite)

    return remplir(0, 0, 0)


def sac_a_dos_elagage(v, p, c):
    def remplir(i, valeur, poids):        
        if i == len(v):
            return Arbre(valeur)
        else:
            valeur_ = valeur + v[i]
            poids_  = poids  + p[i]

            gauche = remplir(i + 1, valeur, poids) # sans objet i
            droite = Arbre(0)
            sol    = gauche.val

            if poids_ <= c:                        # avec objet i
                droite = remplir(i + 1, valeur_, poids_)
                sol    = max(sol, droite.val)

            return Arbre(sol, gauche, droite)
            
    return remplir(0, 0, 0)

def sac_a_dos_turbo(v, p, c):
    num_appels   = 0
    num_completes = 0 
    meilleure = max(max(v), sac_a_dos_glouton(v, p, c))
    potentiel = [sum(v[i:]) for i in range(len(v))]

    def remplir(i, valeur, poids):
        nonlocal meilleure

        meilleure = max(meilleure, valeur)

        if i == len(v):
            return Arbre(valeur)
        elif valeur + potentiel[i] <= meilleure:
            return Arbre(0)
        else:
            valeur_ = valeur + v[i]
            poids_  = poids  + p[i]

            gauche = remplir(i + 1, valeur, poids)
            droite = Arbre(0)
            sol    = gauche.val

            if poids_ <= c:
                droite = remplir(i + 1, valeur_, poids_)
                sol    = max(sol, droite.val)

            return Arbre(sol, gauche, droite)

    return remplir(0, 0, 0)

# Code de génération de diaporama
def figure(arbres, n):
    # Distance des étages
    distances = []
    d = 2**(n-1)

    for i in range(1, n+1):
        distances.append("level " + str(i) +
                         "/.style={sibling distance=" + str(d) + "cm}")
        d //= 2

    # Dessiner arbres
    dessins = [Arbre.code(arbre, init=True, opacite=1.0 / len(arbres))
               for arbre in arbres]
    
    return "\n".join(["\\begin{adjustbox}{width=\\textwidth}",
                      "  \\begin{tikzpicture}[thick," +\
                      ",".join(distances) + "]",
                      *dessins,
                      "  \\end{tikzpicture}"
                      "\\end{adjustbox}"])

def page(arbres, n, algo):
    return ("\\begin{{frame}}"\
            "  \\begin{{overlayarea}}{{\\textwidth}}{{1cm}}"\
            "  \\begin{{minipage}}{{\\textwidth}}"\
            "    Algorithme \\text{{{}}} où $n$ = {}"
            "    \\begin{{alignat*}}{{3}}"\
            "     \\mathrm{{Poids}}  &\\sim \\mathrm{{Unif}}(1, 25) &\\quad"\
            "     \\mathrm{{Valeur}} &\\sim \\mathrm{{Unif}}(1, 25) &\\quad"\
            "     \\mathrm{{Capacité}} &= 25"\
            "    \\end{{alignat*}}"\
            "  \\end{{minipage}}"\
            "  \\end{{overlayarea}}".format(algo, n) +\
            "  \\vspace{1cm}" +\
            "  \\begin{overlayarea}{\\textwidth}{6cm}" +\
                 figure(arbres, n) +\
            "  \\end{overlayarea}" +\
            "\\end{frame}")

def diapo(seq_arbres, seq_taille, algo):
    return "\n".join(["\\documentclass{beamer}",
                      "\definecolor{arriere}{RGB}{242, 241, 240}",
                      "\\setbeamercolor{background canvas}{bg=arriere}",
                      "\\usepackage{adjustbox}",
                      "\\usepackage{tikz}",
                      "\\setbeamertemplate{navigation symbols}{}",
                      "",
                      "\\begin{document}",
                      "\n".join([page(a, n, algo) for (a, n) in
                                 zip(seq_arbres, seq_taille)]),
                      "\\end{document}"])
    
if __name__ == "__main__":
    num_rep = 100

    # Générer arbres
    seq_arbres = []
    seq_taille = []
    
    for n in range(4, 8+1):
        arbres = []

        for _ in range(num_rep):
            v = [randint(1, 25) for _ in range(n)]
            p = [randint(1, 25) for _ in range(n)]
            c = 25

            arbres.append(sac_a_dos_turbo(v, p, c))

        seq_arbres.append(arbres)
        seq_taille.append(n)

    print(diapo(seq_arbres, seq_taille, "avec élagage++"))
