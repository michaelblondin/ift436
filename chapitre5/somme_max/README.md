# Problème de la sous-séquence maximale

Rappelons le problème où, étant donné une séquence de _n_ nombres, on cherche à identifier la somme maximale
parmi toutes les sous-séquences contigües non vides. Par exemple, sur cette séquence, la somme maximale est 9:

```
s = [3, 1, -5, 𝟒, -𝟐, 𝟏, 𝟔, -3]
```

En classe (A24), des personnes ont proposé deux approches prometteuses afin de résoudre le problème.
Ce billet décrit les algorithmes obtenus en suivant autant que possible la réflexion faite en classe.

## Approche 1

Expliquons l'approche à l'aide de l'exemple précédent. On procède en trois étapes.

### Étape A

On calcule d'abord la valeur de chaque préfixe de la séquence,
c.-à-d.   _val_pref[j] := s[1] + ... + s[j]_ pour chaque _j_:

```
  val_pref ← [s[1]]

  pour j ∈ [2..n]:
    ajouter (val_pref[j-1] + s[j]) à val_pref
```
Dans notre exemple, on obtient:

```
       s = [3, 1, -5, 4, -2, 1, 6, -3]
val_pref = [3, 4, -1, 3,  1, 2, 8,  5]
```

### Étape B

Conceptuellement, on aimerait ensuite calculer, pour chaque _i_,
la séquence _sommes[i]_ telle que _sommes[i][j] := s[i] + ... + s[j]_.
Dans notre exemple, on aurait:

```
        s = [3, 1, -5,  4, -2,  1, 6, -3]

sommes[1] = [3, 4, -1,  3,  1,  2, 𝟖,  5]
sommes[2] = [–, 1, -4,  0, -2, -1, 𝟓,  2]
sommes[3] = [–, –, -5, -1, -3, -2, 𝟒,  1]
sommes[4] = [–, –,  –,  4,  2,  3, 𝟗,  6]
sommes[5] = [–, –,  –,  –, -2, -1, 𝟓,  2]
sommes[6] = [–, –,  –,  –,  –,  1, 𝟕,  4]
sommes[7] = [–, –,  –,  –,  –,  –, 𝟔,  3]
sommes[8] = [–, –,  –,  –,  –,  –, –, -𝟑]
```

Remarquons que _sommes[1] = val_pref_. Ainsi, la première séquence a déjà été
calculée à l'étape A. On pourrait calculer _sommes[2]_ à partir de _s[1]_
et _sommes[1]_, et ainsi de suite.
Par contre, le calcul de ces _n - 1_ autres séquences s'effectuerait forcément
en temps quadratique puisqu'il y a _(n-1) + (n-2) + … + 1 = n(n-1)/2_ valeurs.

Nous allons donc éviter de calculer toutes ces séquences. L'information qui
nous intéresse réellement est la valeur maximale de _sommes[i]_. Ces nombres
apparaissent en gras dans l'exemple ci-dessus. Remarquons que

```
max(sommes[i]) = max(s[i], s[i] + max(sommes[i+1])).
```

En effet, la meilleure somme qui débute à la position _i_ est ou
bien _s[i]_ (l'élément seul), ou bien une somme de la forme
_s[i] + s[i+1] + … + s[j]_. La meilleure somme de la forme _s[i+1] + … + s[j]_
est par définition _max(sommes[i+1])_.

Cette identité nous permet donc de calculer _max(sommes[i])_ à rebours:

```
  max_sommes ← [-∞, ... ,-∞, s[n]]

  pour i de n-1 à 1:
    max_sommes[i] ← max(s[i], s[i] + max_sommes[i+1])
```

Dans notre exemple, nous obtenons:

```
max_sommes = [𝟖, 𝟓, 𝟒, 𝟗, 𝟓, 𝟕, 𝟔, -𝟑]
```

### Étape C

Il ne reste plus qu'à retourner la meilleure valeur:

```
  m ← -∞

  pour i ∈ [1..n]:
    m ← max(m, max_sommes[i])

  retourner m
```

### Algorithme complet

En combinant les trois étapes, on obtient un algorithme qui fonctionne en temps _O(n)_:

```
  // Étape A
  val_pref ← [s[1]]

  pour j ∈ [2..n]:
    ajouter (val_pref[j-1] + s[j]) à val_pref

  // Étape B
  max_sommes ← [-∞, ... ,-∞, s[n]]

  pour i de n-1 à 1:
    max_sommes[i] ← max(s[i], s[i] + max_sommes[i+1])

  // Étape C
  m ← -∞

  pour i ∈ [1..n]:
    m ← max(m, max_sommes[i])

  retourner m
```

### Simplification du code

Remarquons que l'étape A est complètement inutile! En effet, la séquence _val_pref_ n'est
jamais utilisée. Elle n'a été décrite que pour donner de l'intuition.
De plus, il est possible de simplifier le code en effecutant les étapes B et C
en même temps, et en remarquant qu'il est inutile de stocker la séquence _max_sommes_:

```
  // Étapes B et C
  max_sommes_actuel ← s[n]
  m ← max_sommes_actuel

  pour i de n-1 à 1:
    max_sommes_actuel ← max(s[i], s[i] + max_sommes_actuel)
    m ← max(m, max_sommes_actuel)
```

Nous venons donc de réinventer l'[algorithme de Kadane](https://en.wikipedia.org/wiki/Maximum_subarray_problem#Kadane's_algorithm)!
Il s'agit un exemple d'algorithme qui exploite la programmation dynamique; un paradigme qui sera couvert plus tard dans la
session.

## Approche 2

***Cette section est en construction; ignorez-la pour l'instant.***

La première approche considère la somme de la séquence complète, et fait pointer _i_ et _j_
respectivement vers le début et la fin de la séquence. À chaque itération, on détermine
ce qui semble le plus profitable entre incrémenter _i_ et décrémenter _j_:

```
  i ← 1
  j ← n

  somme_actuelle  ← s[1] + ... + s[n]
  meilleure_somme ← somme_actuelle

  tant que i < j:
    si somme_actuelle - s[i] > somme_actuelle - s[j]:
      somme_actuelle ← somme_actuelle - s[i]
      i ← i + 1
    sinon:
      somme_actuelle ← somme_actuelle - s[j]
      j ← j - 1

    meilleure_somme ← max(meilleure_somme, somme_actuelle)

  return meilleure_somme
```

La procédure maintient ces invariants:

```
somme_actuelle  = s[i] + ... + s[j]
meilleure_somme = max{s[x] + ... + s[y] : x ≤ i et j ≤ y}
```

Ainsi, lorsqu'on termine, on a

```
meilleure_somme = max{s[x] + ... + s[y] : x ≤ i ≤ y}
```

```
s = [3, 5, -5, 4]


i = 1
j = 4
somme_actuelle = 7
meilleure_somme = 7

i = 2
j = 4
somme_actuelle = 4
meilleure_somme = 7

i = 2
j = 3
somme_actuelle = 0
meilleure_somme = 7

i = 2
j = 2
somme_actuelle = 5
meilleure_somme = 7
```
