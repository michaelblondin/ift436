from horizon import decouper, hauteur, gauche, droite
from random  import randint, expovariate

def reduire(blocs):
    n = len(blocs)
    
    if n <= 1:
        return blocs
    else:
        r = [blocs[0]]
        
        for a in blocs:
            b = r[-1]

            if hauteur(a) == hauteur(b) and gauche(a) <= droite(b):
                r[-1] = (gauche(b), hauteur(b), droite(a))
            else:
                r.append(a)

        return r

def chemins(blocs):
    if len(blocs) == 0:
        return blocs
    else:
        blocs = reduire(blocs)
        chem  = []

        b   = blocs[0]
        acc = [(gauche(b), 0),
               (gauche(b), hauteur(b)),
               (droite(b), hauteur(b))]

        for i in range(1, len(blocs)):
            a = blocs[i - 1]
            b = blocs[i]

            if gauche(b) != droite(a):
                acc.append((droite(a), 0))
                chem.append(acc)

                acc = [(gauche(b), 0)]
                
            acc.append((gauche(b), hauteur(b)))
            acc.append((droite(b), hauteur(b)))

        acc.append((droite(b), 0))
        chem.append(acc)

        return chem

def rectangle(bloc, col):
    off     = 0.09
    g, h, d = bloc

    return (f"\\draw[{col}, fill={col}, fill opacity=0.3]"
            f"({g} + {off}, 0)           -- ({g} + {off}, {h} - {off}) -- "
            f"({d} - {off}, {h} - {off}) -- ({d} - {off}, 0) -- cycle;")

def point(pt):
    diam = 7
    i, j = pt

    return f"\\filldraw ({i}, {j}) circle ({diam}pt) node[] {{}};"

def points(bloc):
    g, h, d = bloc

    return "\n".join(point(pt) for pt in [(g, 0), (g, h), (d, h), (d, 0)])

def rectangles(blocs, coins=False):
    col  = ["cyan", "magenta", "orange", "purple", "green",
            "red", "blue", "olive"]
    rect = [rectangle(b, c) for (b, c) in zip(blocs, col * len(blocs))]
    pts  = [points(b) for b in blocs] if coins else []

    return "\n".join(rect + pts)

def tracer_chemin(c, coins, opacite, contour, couleur):
    pts = ["({}, {})".format(i, j) for (i, j) in c]
    tr  = "\\draw[draw={}, fill={}, fill opacity={}]"\
          " {} -- cycle;".format(contour, couleur, opacite, " -- ".join(pts))

    if coins: tr += "\n".join(point(p) for p in c)

    return tr

def tracer(chem, coins=False, opacite=1.0, contour="black", couleur="gray!50"):
    return "\n".join(tracer_chemin(c, coins, opacite,
                                   contour, couleur) for c in chem)

def figure(code):
    return "\n".join(["  \\begin{frame}",
                      "    \centering",
                      "    \\begin{adjustbox}{width=\\textwidth}",
                      "      \\begin{tikzpicture}[line width=5pt]",
                      "        ", code,
                      "      \\end{tikzpicture}",
                      "    \\end{adjustbox}",
                      "  \\end{frame}"])

def exporter(blocs):
    decoupage = decouper(blocs)
    reduction = reduire(decoupage)
    chem      = chemins(reduction)
    
    return "\n".join([f"%% Blocs: {blocs}",
                      "\\documentclass{beamer}",
                      "\definecolor{arriere}{RGB}{242, 241, 240}",
                      "\\setbeamercolor{background canvas}{bg=arriere}",
                      "\\usepackage{adjustbox}",
                      "\\usepackage{tikz}",
                      "\\setbeamertemplate{navigation symbols}{}",
                      "",
                      "\\begin{document}",
                      "%% Paysage",  figure(rectangles(blocs)),
                      "%% Découpé",  figure(rectangles(decoupage)),
                      "%% Minimisé", figure(rectangles(reduction)),
                      "%% Minimisé", figure(rectangles(reduction, coins=True)),
                      "%% Tracé",    figure(tracer(chem, coins=True)),
                      "%% Tracé",    figure(tracer(chem)),
                      "",
                      "\\end{document}"])

# Exemple
if __name__ == "__main__":
    # Paysage aléatoire
    blocs = []

    for _ in range(10):
        horizontal = max(1, int(expovariate(5) * 50))
        vertical   = max(1, int(expovariate(5) * 40))
        position   = randint(0, 50)

        bloc = (position, vertical, position + horizontal)

        blocs.append(bloc)

    # # Paysage sous forme de montagne
    # n = 10
    # blocs = [(n - i, n - i, n + i + 1) for i in range(n)]

    print(exporter(blocs))
