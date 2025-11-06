from exporter import chemins, tracer, reduire
from horizon  import decouper, hauteur, gauche, droite
from math     import sqrt
from random   import randint, expovariate, uniform

def figure(code, texte):
    return "\n".join(["  \\begin{frame}",
                      "    \\vspace*{-3cm}",
                      "    \\begin{overlayarea}{\\textwidth}{2cm}",
                      texte,
                      "    \\end{overlayarea}",
                      "    \\vspace*{10pt}",
                      "    \\begin{overlayarea}{\\textwidth}{3cm}",
                      "      \\begin{minipage}[t][7cm][b]{\\linewidth}",
                      "        \\centering",
                      "        \\begin{adjustbox}{width=\\textwidth}",
                      "          \\begin{tikzpicture}[line width=5pt]",
                      "            ", code,
                      "          \\end{tikzpicture}",
                      "        \\end{adjustbox}",
                      "      \\end{minipage}",
                      "    \\end{overlayarea}",
                      "  \\end{frame}"])

def diapo(paysages, opacite, texte):
    code = []
    
    for paysage in paysages:
        decoupage = decouper(paysage)
        reduction = reduire(decoupage)
        chem      = chemins(reduction)
        
        code.append(tracer(chem, False, opacite, "none", "blue"))

    return figure("\n".join(code), texte)

def exporter(contenu):   
    return "\n".join(["\\documentclass{beamer}",
                      "\definecolor{arriere}{RGB}{242, 241, 240}",
                      "\\setbeamercolor{background canvas}{bg=arriere}",
                      "\\usepackage{adjustbox}",
                      "\\usepackage{tikz}",
                      "\\newcommand{\\N}{\\mathbb{N}}",
                      "\\setbeamertemplate{navigation symbols}{}",
                      "",
                      "\\begin{document}",
                      "\n".join(contenu),
                      "\\end{document}"])

# Exemple
if __name__ == "__main__":
    # Distributions des positions et hauteurs
    CONST = 50

    ## Distrib. exponentielle
    nom_distrib = lambda p: "\\mathrm{{Exp}}({:05.2f})\\cdot{}".format(p, CONST)
    distrib     = lambda p: max(1, int(expovariate(param) * CONST))
    esperance   = lambda p: (1.0 / param) * CONST
    variance    = lambda p: (1.0 / param**2) * CONST**2    

    ## Distrib. uniforme
    # nom_distrib = lambda p: "\\mathrm{{Unif}}({:.2f})\\cdot{}".format(2.0 / p,
    #                                                                   CONST)
    # distrib     = lambda p: int(uniform(0, 2.0 / p) * CONST)
    # esperance   = lambda p: (1.0 / param) * CONST
    # variance    = lambda p: (1.0/12)*(2.0 / p)**2 * CONST**2

    # Génération des paysages "moyens" selon la distribution
    param_max = 50
    num_rep   = 100
    num_blocs = 100

    contenu = []
    
    for param in range(1, param_max + 1):
        paysages = []
        
        for _ in range(num_rep):
            blocs = []

            for _ in range(num_blocs):
                position = randint(0, 100)
                vertical = distrib(param)
                largeur  = distrib(param)

                bloc = (position, vertical, position + largeur)
            
                blocs.append(bloc)

            paysages.append(blocs)

        etiquette = "\\resizebox{{\\textwidth}}{{!}}{{"\
                    "\\begin{{minipage}}{{\\textwidth}}"\
                    "  \\begin{{alignat*}}{{4}}"\
                    "    \\text{{Blocs par paysage}}  &= {0} &\\quad"\
                    "    \\text{{Nombre de paysages}} &= {1} \\\\"\
                    ""\
                    "    Gauche  &\\sim \\mathrm{{Unif}}_{{\\N}}(100) &\\quad"\
                    "    Hauteur &\\sim {2}                    &\\quad"\
                    "    Largeur &\\sim {2}                    \\\\"\
                    ""\
                    "    \\mathbb{{E}}[Gauche]  &= 50      &\\quad"\
                    "    \\mathbb{{E}}[Hauteur] &= {3:.2f} &\\quad"\
                    "    \\mathbb{{E}}[Largeur] &= {3:.2f} \\\\"\
                    ""\
                    "    \\sqrt{{\\mathbb{{V}}[Gauche]}}  &= 29.15   &\\quad"\
                    "    \\sqrt{{\\mathbb{{V}}[Hauteur]}} &= {4:.2f} &\\quad"\
                    "    \\sqrt{{\\mathbb{{V}}[Largeur]}} &= {4:.2f}"\
                    "  \\end{{alignat*}}"\
                    "\\end{{minipage}}}}".format(num_blocs,
                                                 num_rep,
                                                 nom_distrib(param),
                                                 esperance(param),
                                                 sqrt(variance(param)))

        contenu.append(diapo(paysages, (0.05 + 0.95 / num_rep), etiquette))

    print(exporter(contenu))
