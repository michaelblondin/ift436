# Question 1(a) (A24)

Rappelons qu'au #1(a) de l'examen de 2024, nous avons considéré cette fonction:

```math
f_3(n) = \sum_{i=1}^n \sum_{j=i}^n j.
```

Pour la somme interne, l'identité ci-dessous a été proposée par une personne du premier groupe (assise à l'avant),
et confirmée en privé après le cours (par une autre personne assise à l'avant):

**Proposition**: $$\sum_{j=i}^n j = \frac{(n - i + 1)(n + i)}{2}$$.

_Preuve_. Nous avons
```math
\begin{align*}
\sum_{j=i}^n j
&= \sum_{j=1}^n j - \sum_{j=1}^{i-1} j \\[5pt]
&= \frac{n(n+1)}{2} - \frac{(i-1)i}{2} \\[5pt]
&= \frac{n^2 + n - i^2 + i}{2} \\[5pt]
&= \frac{n^2 + ni - ni - i^2 + n + i}{2} \\[5pt]
&= \frac{(n - i + 1)(n + i)}{2}. &&\square
\end{align*}
```

Il y a façon de montrer que $f_3 \in \Theta(n^3)$ sans invoquer cette proposition
et sans faire trop de calculs:

**Proposition**: $$f_3(n) \in \Theta(n^3)$$.

_Preuve_. Nous avons
```math
\begin{align*}
f_3(n)
&= \sum_{i=1}^n \sum_{j=i}^n j \\[5pt]
&= (1 + 2 + 3 + \ldots + n) + (2 + 3 + \ldots + n) + (3 + \ldots + n) + \ldots + n \\[5pt]
&= 1 \cdot 1 + 2 \cdot 2 + 3 \cdot 3 + \ldots + n \cdot n \\[5pt]
&= \sum_{i=1}^n i^2 \\[5pt]
&\in \Theta(n^3) && \text{(vu en classe à l'exercice 1.10)}.\ \square
\end{align*}
```

# Question 1(d) (A24)

Rappelons qu'au #1(d) de l'examen de 2024, nous avons considéré la fonction $(n/2)!$.
Certaines personnes du deuxième groupe ont tenté de me convaincre que $(n/2)! = n!/2!$,
et plus généralement que $(n/c)! = n!/c!$. J'ai failli m'avouer vaincu et y croire, mais
j'ai dit que j'allais garder au moins 1% de doute. Ce doute l'a finalement emporté! :sunglasses:

En fait, les deux termes ne sont égaux que pour $n = 2$:

|n |(n/2)!| n!/2! |
|-:|-----:|------:|
|0 |   1  |      ½|
|2 |   1  |      1|
|4 |   2  |     12|
|6 |   6  |    360|
|8 |  24  |  20160|
|10| 120  |1814400|

En fait, la deuxième fonction croît plus rapidement:

**Proposition**: Nous avons $(n/2)! \in O(n!/2!)$ et $n!/2! \notin O((n/2)!)$.

_Preuve_. La première affirmation découle de $(n/2)! \leq n! = 2 \cdot (n! / 2!)$.

Pour la seconde affirmation, supposons que $n!/2! \in O((n/2)!)$. Il existe donc une
constante $c$ et un seuil $n_0$ tels que $n!/2! \leq c(n/2)!$ pour tout $n \geq n_0$.
Soit $n > 0$ un nombre pair supérieur à $n_0$ et $2c$. Nous obtenons une contradiction:
```math
\begin{align*}
2c
&\geq \frac{n!}{(n/2)!} && (\text{car } n > n_0) \\[5pt]
&= \frac{n \cdot (n-1) \cdots 1}{(n/2) (n/2-1) \cdots 1} \\[5pt]
&= n \cdots (n/2+1) \\[5pt]
&\geq n \\[5pt]
&> 2c. &&\square
\end{align*}
```
