# Solutions itératives et récursives

Plusieurs solutions en Python sont disponibles [ici](./algos.py). Attention, certaines fonctionnent en temps exponentiel (voir les commentaires).

# Solution inspirée de l'algorithme de Kahn

Deux étudiants (A21) ont proposé un algorithme intéressant afin de calculer
le nombre maximal d'étoiles qu'on peut obtenir dans un jeu bien conçu.
Leur approche se décrit succinctement comme suit:

```
étoiles ← 0

tant qu'il reste des sommets de degré entrant 0:
  retirer tous ces sommets du graphe
  étoiles ← étoiles + 1
  
retourner étoiles
```

Autrement dit, leur procédure est une modification de l'algorithme de
Kahn où, plutôt que de retirer un sommet de degré entrant _0_ à la
fois, on les retire tous d'un coup. Selon ces deux étudiants, le
nombre de fois qu'on peut répéter cette opération correspond
précisément au nombre maximal d'étoiles qu'on peut obtenir. Par
exemple, l'algorithme fonctionne sur ce jeu bien conçu dont la
solution est _4_:

```
Graphe initial:

    ---> o ---------> o
  /      ^            ^
 /       |           /
o        |          /
 \       |         /
   ----> o  ----> o
 
Après itération 1:

         o ---------> o
         ^            ^
         |           /
         |          /
         |         /
         o  ----> o
 
Après itération 2:

         o ---------> o
                      ^
                     /
                    /
                   /
                  o

Après itération 3:

                      o
                      
Après itération 4:

     [graphe vide]
```

Malgré ma confusion initiale, nous allons montrer que ces deux
étudiants ont raison! Plus précisément, nous allons décrire une
implémentation de l'approche sous forme de pseudocode, puis démontrer
qu'elle est correcte.

## Pseudocode

Voici une description plus bas niveau de l'approche:

```
// Calcul des degrés entrants
deg ← [v ↦ 0 : v ∈ V]

pour (u, v) ∈ E:
  deg[v] ← deg[v] + 1

// Compter les étoiles
traités   ← Ø
à_traiter ← {premier_niveau(G)}
étoiles   ← 0

tant que à_traiter ≠ Ø:
  nouveaux ← Ø
  
  // Mettre à jour les degrés entrants
  pour u ∈ à_traiter:
    pour tout successeur v de u:
      deg[v] ← deg[v] - 1
    
      si deg[v] = 0: ajouter v à nouveaux
  
  traités   ← traités ∪ à_traiter
  à_traiter ← nouveaux
  étoiles   ← étoiles + 1

retourner étoiles
```

## Caractérisation des sommets traités

Pour chaque sommet _v_, définissons _dist(v)_ comme étant la longueur
d'un chemin maximal du premier niveau vers _v_. Le nombre d'étoiles
maximal qu'on peut obtenir en complétant le jeu découle de l'emprunt
d'un chemin de longueur maximal du premier niveau vers le dernier
niveau. Ainsi, nous devons nous assurer que l'algorithme termine avec
_étoiles = dist(dernier niveau) + 1_. Notons que le «+ 1» provient du
fait que la longueur d'un chemin correspond à son nombre d'arêtes,
alors qu'on désire compter son nombre de sommets.

Nous pouvons caractériser les sommets traités de cette façon:

```
Proposition. Un sommet v est traité durant la i-ème itération de la boucle «tant que» ssi dist(v) = i - 1.
```

Démontrons la proposition par induction sur _i_. L'unique sommet
traité durant la premire itération (_i = 1_) est le premier niveau. De
plus, le premier niveau est l'unique sommet à distance _0_ de
lui-même.

Soit _i ≥ 1_. Supposons l'affirmation vraie pour les _i_ premières
itérations. Nous devons montrer que _v_ est traité à l'itération _i+1_
ssi _dist(v) = i_. Montrons les deux directions.

⇒) Soit _v_ un sommet traité durant l'itération _i+1_. Comme _v_ est
traité à cette itération, _deg[v]_ a atteint _0_ à l'itération _i_ via
un prédecesseur _w_. De plus, tous les prédecesseurs de _v_ ont déjà
été traités. Par hypothèse d'induction, nous avons _dist(w) = i - 1_,
et _dist(u) ≤ i - 1_ pour tout prédecesseur _u_ de _v_. De plus,
_dist(v) = max{dist(u) + 1 : u → v}_. Ainsi, _dist(v) = i_.

⇐) Soit _v_ un sommet tel que _dist(v) = i_. Remarquons que _dist(u) <
dist(v)_ pour tout prédecesseur _u_ de _v_.  Ainsi, _dist(u) < i_ pour
tout prédecesseur _u_ de _v_. Par hypothèse d'induction, cela signifie
que tous les prédecesseurs de _v_ ont déjà été traités. De plus, _v_
possède forcément un prédecesseur _w_ tel que _dist(w) = dist(v) -
1_. Ainsi _dist(w) = i - 1_, ce qui signifie que _deg[v]_ atteint _0_
à l'itération _i - 1_. Par conséquent, le sommet _v_ est traité à
l'itération _i_. □

## Correction

```
Théorème. L'algorithme est correct.
```

Comme le dernier niveau est accessible à partir du premier niveau, le
dernier niveau est forcément traité à une certaine itération de la
boucle «tant que». De plus, il est traité à la dernière itération. En
effet, par la proposition, si un sommet _v_ était traité après le
dernier niveau, cela signifierait que _dist(dernier niveau) <
dist(v)_, ce qui est impossible car _v_ peut atteindre le dernier
niveau.

Remarquons que la variable _étoiles_ compte le nombre d'itérations de
la boucle «tant que». Ainsi, par la proposition, l'algorithme se
termine avec _dist(dernier niveau) = étoiles - 1_, ce qui est
équivalent à _étoiles = dist(dernier niveau) + 1_, comme recherché. □
