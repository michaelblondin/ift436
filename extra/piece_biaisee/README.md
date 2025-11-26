
# Pièce biaisée: analyse à l'aide d'un graphe de probabilités

Rappelons qu'en séance d'exercices, nous avons cherché à implémenter
algorithmiquement une pièce non biaisée à l'aide d'une pièce biaisée.
Ici, «biaisée» réfère au fait que la pièce tombe sur pile avec
probabilité _p_, et sur face avec probabilité _1 - p_, où _p ≠ 1/2_.

## Algorithme

L'approche présentée en classe consiste à choisir deux bits à l'aide
de la pièce biaisée, et de recommencer tant que les deux bits sont
égaux. Lorsqu'ils ne sont pas égaux, on retourne ```pile``` si le
premier bit est zéro (l'inverse fonctionnerait aussi, c'est
arbitraire):

```
faire:
  choisir un bit x avec la pièce biaisée
  choisir un bit y avec la pièce biaisée
tant que x = y

si x = 0: retourner "pile"
sinon:    retourner "face"
```

[Vous pouvez voir l'algorithme en action ici](https://www.youtube.com/watch?v=5DN7es3JqHs).

## Analyse à l'aide d'un graphe de probabilités

En classe (A21), j'ai tenté en vain d'analyser l'algorithme, pour le cas
particulier où _p = 1/3_, à l'aide de ce graphe de probabilités (mieux
connu sous le nom savant de _[chaîne de Markov à temps
discret](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_Markov)_):

```
                2/3           1/3          2/3          1/3
 "pile" (01) <------- (0?) <------- (??) ------> (1?) -------> (10) "face"
                       |            ^  ^           |
                       ------------/    \-----------
                            1/3             2/3
```

Ici, chaque sommet de la forme ```(ab)``` indique que le bit _a_ a été
assigné à la variable _x_, et que le bit _b_ a été assigné à la
variable _y_, où ```?``` signifie que rien n'a été assigné.

### Cycles

Voici une analyse qui fonctionne. Cherchons à identifier la
probabilité de débuter dans le sommet ```??``` et d'atteindre le
sommet ```01``` qui correspond au verdict ```pile```. Il est possible
d'utiliser les cycles simples ```?? → 0? → ??``` et ```?? → 1? → ??```
un certain nombre de fois. Appelons ces deux cycles ```g``` et
```d```. Il y a plusieurs façons de combiner ces cycles, par
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
cycle de gauche, est de _1/3 · 1/3 = 1/9_. Similairement, la
probabilité de produire un ```d```, c.-à-d. de choisir le cycle de
droite, est de _2/3 · 2/3 = 4/9_.

### Probabilité d'obtenir "pile"

Pour atteindre le sommet ```01``` à partir du sommet ```??```, on doit:

* débuter en ```??``` et y revenir en combinant les deux cycles _n_
  fois en utilisant _k_ fois le cycle de gauche (pour certains _n_,
  _k_);
* suivre les deux arêtes vers la gauche.

La probabilité d'obtenir ```pile``` est donc de 1/2 comme attendu:

```
     ∞     n
    \¯¯   \¯¯     /n\        k       n-k
    /__   /__     \k/ · (1/9) · (4/9)   · (1/3) · (2/3)
   n = 0 k = 0

            ∞     n
           \¯¯   \¯¯     /n\        k       n-k
= (2/9) ·  /__   /__     \k/ · (1/9) · (4/9)
           n = 0 k = 0

             ∞  
            \¯¯        n
= (2/9) ·   /__   (5/9)      [par la formule du binôme de Newton avec x = 1/9 et y = 4/9]
           n = 0

               1  
= (2/9) ·  ---------         [car série géométrique de raison 5/9]
           (1 - 5/9)

= (2/9) · (9/4)

= 1/2.
```

### Liens

- [Formule du binôme de Newton](https://fr.wikipedia.org/wiki/Formule_du_binôme_de_Newton)
- [Séries géométriques](https://fr.wikipedia.org/wiki/S%C3%A9rie_g%C3%A9om%C3%A9trique)
