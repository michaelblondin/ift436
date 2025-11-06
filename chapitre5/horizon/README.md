# Problème de la ligne d'horizon

Afin de convertir en PDF:

1. Convertir le paysage en LaTeX: `python3 exporter.py > paysage.tex`
2. Compiler: par ex.              `pdflatex paysage.tex`
3. Ouvrir `paysage.pdf`

_La compilation requiert le package TikZ pour LaTeX._

<img src="img/animation.gif" width="500" alt="Animation">

## Distribution des paysages

Le script `distribution.py` génère les animations ci-dessous. Cela répond partiellement
à une question posée en classe (A25) à propos de la distribution des paysages
aléatoires obtenus par une loi exponentielle ou uniforme:

<img src="img/animation_exp.gif" width="500" alt="Animation"><img src="img/animation_unif.gif" width="500" alt="Animation">
