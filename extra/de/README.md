# Dé à six faces: analyse de l'algorithme

Rappelons qu'en classe, nous avons implémenté algorithmiquement 
un dé à six faces à l'aide d'une pièce (non biaisée):

```
val(b₂, b₁, b₀):
  retourner 2²·b₂ + 2¹·b₁ + 2⁰·b₀

faire:
  choisir un bit y₀ avec la pièce
  choisir un bit y₁ avec la pièce
  choisir un bit y₂ avec la pièce
tant que y₀ = y₁ = y₂

retourner val(y₂, y₁, y₀)
```

## Combien de pièces pour émuler le dé?

Soit $X$ la variable aléatoire qui compte le nombre d'itérations de la boucle.
Puisque chaque itération de l'algorithme est indépendante des précédentes, _X_
suit une loi géométrique. Ainsi, $\mathbb{E}[X] = 1 / p$, où $p$ est la probabilité de
succès, c.-à-d. de quitter la boucle. Par conséquent, $\mathbb{E}[X] = 1 / (6 / 8) = 4/3$.

## Émule-t-on véritablement une pièce de monnaie?

Calculons la probabilité que l'algorithme retourne un certain nombre $m \in [1..6]$.

### Aproche 1: probabilité conditionnelle

$$
\begin{alignat}{3}
  & && \mathbb{P}(\text{retourner } m) \\\\[5pt]
  & && \mathbb{P}(\mathrm{val}(y_2, y_1, y_0) = m | \neg(y_0 = y_1 = y_2)) \\\\[5pt]
  &=\ && \mathbb{P}(\mathrm{val}(y_2, y_1, y_0) = m \land \neg(y_0 = y_1 = y_2)) / \mathbb{P}(\neg(y_0 = y_1 = y_2))
  && \text{(car $\mathbb{P}(A \mid B) = \mathbb{P}(A \cap B) / \mathbb{P}(B)$)} \\\\[5pt]
  &=\ && \mathbb{P}(\mathrm{val}(y_2, y_1, y_0) = m) / \mathbb{P}(\neg(y_0 = y_1 = y_2))
  && \text{(car $m \in [1..6]$)} \\\\[5pt]
  &=\ && (1/8) / (6/8) \\\\[5pt]
  &=\ && 1/6.
\end{alignat}
$$

### Approche 2: série géométrique

$$
\begin{alignat}{3}
  & && \mathbb{P}(\text{retourner } m) \\\\[5pt]
  &=\ && \sum_{i=0}^\infty \mathbb{P}(y_0 = y_1 = y_2)^i \cdot \mathbb{P}(\mathrm{val}(y_2, y_1, y_0) = m)
  && \text{(car il y a un certain nombre $i$ d'itérations)} \\\\[5pt]
  &=\ && \sum_{i=0}^\infty (2 / 8)^i \cdot (1 / 8) \\\\[5pt]
  &=\ && (1 / 8) \cdot \sum_{i=0}^\infty (1 / 4)^i \\\\[5pt]
  &=\ && (1 / 8) \cdot (1 / (1 - 1/4))
  && \text{(car $r^0 + r^1 + r^2 + \ldots = 1 / (1 - r)$ lorsque $0 < r < 1$)} \\\\[5pt]
  &=\ && (1 / 8) \cdot (4 / 3) \\\\[5pt]
  &=\ && 1 / 6.
\end{alignat}
$$

### ★ Approche 3: analyse à l'aide d'un graphe de probabilités

En classe (A23), j'ai tenté en vain d'analyser la probabilité que
l'algorithme génère un nombre en particulier, à l'aide de ce graphe
de probabilités (mieux connu sous le nom savant de _[chaîne de Markov à temps
discret](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_Markov)_):

```                                  
  ┌─────────────────▸ (???) ◂─────────────────┐
  │             ½ ↙           ↘ ½             │
 ½│        (??0)                 (??1)        │½
  │     ½ ↙     ↘ ½           ½ ↙     ↘ ½     │
  └───(?00)     (?10)       (?01)     (?11)───┘
       ½↓      ½ ↙ ↘ ½     ½ ↙ ↘ ½      ↓½
      (100)  (010) (110) (001) (101)  (011)
```

Ici, chaque sommet de la forme ```(abc)``` indique que le bit _a_ a été
assigné à la variable _y₂_, que le bit _b_ a été assigné à la
variable _y₁_, et , que le bit _c_ a été assigné à la variable _y₀_,
où ```?``` signifie que rien n'a été assigné.

#### Cycles

Voici une analyse qui fonctionne. Cherchons à identifier la
probabilité de débuter dans le sommet ```???``` et d'atteindre le
sommet ```100``` qui correspond au verdict ```4```. Il est possible
d'utiliser les cycles simples ```??? → ??0 → ?00 → ???``` et
```??? → ??1 → ?11 → ???``` un certain nombre de fois. Appelons ces deux
cycles ```g``` et ```d```. Il y a plusieurs façons de combiner ces cycles, par
ex. ```gddg``` indique qu'on tourne d'abord à gauche, puis deux fois à
droite, puis une dernière fois à gauche. Le nombre de façons de concaténer
_n_ cycles avec exactement _k_ occurrences de ```g``` correspond à [_k
parmi n_](https://fr.wikipedia.org/wiki/Coefficient_binomial). Par
exemple, pour _n = 4_ et _k = 2_, six choix s'offrent à nous:

```
ggdd
ddgg
gdgd
dgdg
gddg
dggd
```

De plus, la probabilité de produire un ```g```, c.-à-d. de choisir le
cycle de gauche, est de _1/2 · 1/2 · 1/2 = 1/8_. Similairement, la
probabilité de produire un ```d```, c.-à-d. de choisir le cycle de
droite, est de _1/8_.

#### Probabilité d'obtenir ```4```

Pour atteindre le sommet ```100``` à partir du sommet ```???```, on doit:

* débuter en ```???``` et y revenir en combinant les deux cycles _n_
  fois en utilisant _k_ fois le cycle de gauche (pour certains _n_,
  _k_);
* suivre les trois arêtes vers le bas et la gauche: ```??? → ??0 → ?00 → 100```.

La probabilité d'obtenir ```4``` est donc de:

$$
\begin{alignat}{3}
  & && \mathbb{P}(\text{retourner } 4) \\\\[5pt]
  &=\ && \sum_{n=0}^\infty \sum_{k=0}^n {n \choose k} \cdot (1/8)^k \cdot (1/8)^{n-k} \cdot (1/2) \cdot (1/2) \cdot (1/2) \\\\[5pt]
  &=\ && (1/8) \cdot \sum_{n=0}^\infty \sum_{k=0}^n {n \choose k} \cdot (1/8)^k \cdot (1/8)^{n-k} \\\\[5pt]
  &=\ && (1/8) \cdot \sum_{n=0}^\infty (1/8 + 1/8)^n
  && \text{(par la formule du binôme de Newton avec $x = 1/8$ et $y = 1/8$)} \\\\[5pt]
  &=\ && (1/8) \cdot \sum_{n=0}^\infty (1/4)^n \\\\[5pt]
  &=\ && (1/8) \cdot (1 / (1 - 1/4)) \\\\[5pt]
  &=\ && (1/8) \cdot (4/3) \\\\[5pt]
  &=\ && 1/6.
\end{alignat}
$$

Le raisonnement pour les cinq autres valeurs est similaire. Dans tous les cas, on obtient $1/6$ comme attendu.

### Liens

- [Formule du binôme de Newton](https://fr.wikipedia.org/wiki/Formule_du_binôme_de_Newton)
- [Séries géométriques](https://fr.wikipedia.org/wiki/S%C3%A9rie_g%C3%A9om%C3%A9trique)
