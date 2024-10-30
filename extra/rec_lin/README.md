# Résolution de récurrences linéaires: explications

Au chapitre 5, nous avons vu une méthode afin de résoudre des récurrences linéaires. Dans le cadre du cours,
il n'est pas nécessaire de comprendre pourquoi cette méthode fonctionne ou comment elle a été inventée.
Néanmoins, certaines personnes ont un malaise à appliquer une méthode sans réellement comprendre son essence. Ainsi,
une annexe avancée des notes de cours démontre que la méthode fonctionne à l'aide d'algèbre linéaire.
Cependant, cette annexe est assez technique. Voyons donc les concepts les plus importants à l'aide d'un exemple.

## Écrire une récurrence linéaire sous forme matricielle

Reconsidérons le problème de pavage du chapitre 5, c'est-à-dire celui où on cherche à paver une grille
_3 × n_ à l'aide de tuiles de cette forme (sans rotations):

```
▌   █   ▙   ▜
```

Soit _t(n)_ le nombre de pavages d'une grille _3 × n_. Nous avons vu que

```
t(1) = 1,
t(2) = 3,
t(n) = t(n-1) + 2·t(n-2) pour n ≥ 3.
```

Ainsi, les premiers termes de la suite _t(1), t(2), t(3), t(4), t(5), t(6), …_ sont _1, 3, 5, 11, 21, 43, …_

Considérons cette matrice carrée A et ce vecteur colonne b:

```
A = 1 2    b = 3
    1 0        1
```

La première ligne de _A_ provient des coefficients du terme général
_t(n) = **1**·t(n-1) + **2**·t(n-2)_. Le vecteur _b_ provient des
cas de base: _t(2) = **3**_ et _t(1) = **1**_. Intuitivement, _b_
donne les deux premiers termes de la suite (dans le sens inverse),
et _A_ indique comment calculer le prochain terme de la suite à partir
des deux derniers. Par exemple:

```
b = 3    Ab = 5    A(Ab) = 11    A(A(Ab)) = 21    A(A(A(Ab))) = 43
    1         3             5               11                  21
```

Ainsi, _Aⁿb_ est le vecteur qui contient les _(n+1)_-ième et _n_-ième termes de la suite.
Ainsi, afin de trouver la valeur de _t(n)_, on peut calculer _Aⁿb_, puis prendre la
deuxième valeur du vecteur obtenu. Autrement dit, _t(n) = (Aⁿb)[2]_.

## Vecteurs et valeurs propres

Rappelons qu'un vecteur _v_ est un _vecteur propre_ de _A_ s'il existe un nombre _λ ≠ 0_
tel que _Av = λv_. La valeur _λ_ s'appelle la _valeur propre_ associée au vecteur _v_.
Remarquons que

```
A(Av) = A(λv) = λAv = λλv = λ²v.
```

Par le même raisonnement, _A(A(Av)) = λ³v_ et plus généralement _Aⁿv = λⁿv_.

De plus, notons que les vecteurs propres de la matrice _A_ précédente sont _v₁ = (1, ½)_ et _v₂ = (-1, 1)_
avec les valeurs propres _λ₁ = 2_ et _λ₂ = -1_. En effet:

```
A · 1 = 2       A · -1 =  1
    ½   1            1   -1
```

Lorsque les valeurs propres sont toutes distinctes, les vecteurs propres forment une base de l'espace
vectoriel. Ainsi, n'importe quel vecteur s'écrit comme une combinaison linéaire des vecteurs propres.
Ainsi, en particulier, le vecteur _b_ est une combinaison linéaire de _v₁_ et _v₂_. Autrement dit,
il existe des nombres _d₁_ et _d₂_ tels que _b = d₁·v₁ + d₂·v₂_. Dans notre cas, nous avons
_d₁ = 8/3_ et _d₂ = -1/3_ car

```
(8/3)·1 + (-1/3)·(-1) = 3
(8/3)·½ + (-1/3)·1    = 1
```

## Forme close

En combinant nos observations, nous obtenons:

```
t(n) = (Aⁿb)[2]
     = (Aⁿ(d₁·v₁ + d₂·v₂))[2]
     = (d₁·Aⁿv₁ + d₂·Aⁿv₂)[2]
     = (d₁·λ₁ⁿv₁ + d₂·λ₂ⁿv₂)[2]
     = d₁·λ₁ⁿ·v₁[2] + d₂·λ₂ⁿ·v₂[2]
     = (d₁·v₁[2])·λ₁ⁿ + (d₂·v₂[2])·λ₂ⁿ.
```

En posant _c₁ = d₁·v₁[2]_ et _c₂ = d₂·v₂[2]_, on obtient une forme close qui correspond à celle
décrite dans les notes de cours:

```
t(n) = c₁·λ₁ⁿ + c₂·λ₂ⁿ.
```

Dans notre exemple, nous avons _c₁ = d₁·v₁[2] = (8/3)·½ = 4/3_ et _c₂ = d₂·v₂[2] = (-1/3)·1 = -1/3_.
Ce sont en effet les deux constantes obtenues dans les notes de cours.

## Polynôme caractéristique

Le _polynôme caractéristique_ d'une matrice carrée _A_ est la fonction _p(x) = det(xI - A)_ où
_I_ est la matrice identité. Il s'avère que les racines du polynôme caractéristique d'une
matrice correspondent aux valeurs propres de la matrice. Dans notre exemple, nous avons:

```
p(x) = det(xI - A) = |x-1  -2| = (x-1)·x - (-2)·(-1) = x² - x - 2 = (x - 2)(x + 1).
                     |-1    x|
```

Les racines de _p_ sont donc _2_ et _-1_, qui sont en effet les valeurs propres
obtenues précédemment.

Ainsi, afin d'identifier les valeures propres, la méthode présentée en classe
identifie plutôt les racines du polynôme caractéristique. De plus, comme la matrice
_A_ a une forme très particulière, il n'est pas nécessaire de calculer le déterminant.
On peut montrer que le polynôme caractéristique possède toujours la forme présentée
dans les notes de cours.
