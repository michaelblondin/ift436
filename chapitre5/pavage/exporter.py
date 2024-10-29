from pavage import pavages, Tuile

def macros():
    return "\n".join(["\\definecolor{colA}{HTML}{648FFF}",
                      "\\definecolor{colB}{HTML}{DC267F}",
                      "\\definecolor{colC}{HTML}{FE6100}",
                      "\\definecolor{colD}{HTML}{785EF0}",
                      "\\definecolor{colE}{HTML}{FFB000}",
                      "\\newcommand{\\tuileA}[2]{%",
                      "  \\begin{tikzpicture}%",
                      "    \\fill[#1] (0, 0) -- (0, 3) -- (1, 3) -- (1, 0) -- cycle;%",
                      "    \\draw[white] (0, 1) -- (1, 1);%",
                      "    \\draw[white] (0, 2) -- (1, 2);%",
                      "  \\end{tikzpicture}\\hspace{-3.5pt}%",
                      "}",
                      "\\newcommand{\\tuileB}[2]{%",
                      "  \\begin{tikzpicture}%",
                      "    \\fill[#1] (0, 0) -- (0, 3) -- (2, 3) -- (2, 0) -- cycle;%",
                      "    \\draw[white] (0, 1) -- (2, 1);%",
                      "    \\draw[white] (0, 2) -- (2, 2);%",
                      "    \\draw[white] (1, 0) -- (1, 3);%",
                      "  \\end{tikzpicture}\\hspace{-3.5pt}%",
                      "}",
                      "\\newcommand{\\tuileC}[2]{%",
                      "  \\begin{tikzpicture}%",
                      "    \\fill[#1] (0, 0) -- (0, 2) -- (1, 2) -- (1, 1) -- (2, 1) -- (2, 0) -- cycle;%",
                      "    \\fill[#2] (0, 2) -- (0, 3) -- (2, 3) -- (2, 1) -- (1, 1) -- (1, 1) -- (1, 2) -- cycle;%",
                      "    \\draw[white] (0, 1) -- (2, 1);%",
                      "    \\draw[white] (0, 2) -- (2, 2);%",
                      "    \\draw[white] (1, 0) -- (1, 3);%",
                      "  \\end{tikzpicture}%",
                      "}",
                      "\\newcommand{\\tuileD}[2]{\\hspace{-7pt}}"])

def latex(p):
    TUILE = {Tuile.A: "\\tuileA",
             Tuile.B: "\\tuileB",
             Tuile.C: "\\tuileC",
             Tuile.D: "\\tuileD"}

    MOTIFS = ["{preaction={fill=colA}, pattern=north west lines, pattern color=white}",
              "{preaction={fill=colB}, pattern=north east lines, pattern color=white}",
              "{preaction={fill=colC}, pattern=crosshatch, pattern color=white}",
              "{preaction={fill=colD}, pattern=north west lines, pattern color=white}",
              "{preaction={fill=colE}, pattern=north east lines, pattern color=white}",
              "{preaction={fill=black}, pattern=crosshatch dots, pattern color=white}"]
        
    # Générer pavage
    tuiles = []

    for (i, t) in enumerate(p):
        tuiles.append(TUILE[t] + MOTIFS[(2*i) % len(MOTIFS)] + MOTIFS[(2*i + 1) % len(MOTIFS)])
    
    return "\n".join(["\\begin{frame}",
                      "  \\hfill",
                      "      \n".join(tuiles),
                      "  \\hfill\\hfill",
                      "\\end{frame}"])

def exporter(n):
    # Générer diapos
    s      = pavages(n)
    diapos = [latex(p) for p in s]
    
    return "\n".join(["\\documentclass{beamer}",
                      "\\setbeamertemplate{navigation symbols}{}",
                      "\\usepackage{tikz}",
                      "\\usetikzlibrary{patterns}",
                      macros(),
                      "\\begin{document}",
                      "  \n".join(diapos),
                      "\\end{document}"])

if __name__ == "__main__":
    n = 3
    
    print(exporter(n))
