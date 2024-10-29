from enum import Enum

class Tuile(Enum):
    A = "\033[0;32m▌\033[0;30m█"
    B = "\033[0;36m█\033[0;30m█"
    C = "\033[0;34m▙"
    D = "\033[0;35m▜\033[0;30m█\033[0;30m█"

def pavages(n):
    if n == 0:
        return [[]]
    if n == 1:
        return [[Tuile.A]]
    else:
        P = pavages(n - 1)
        Q = pavages(n - 2)

        return ([[Tuile.A] + p for p in P] +
                [[Tuile.B] + q for q in Q] +
                [[Tuile.C, Tuile.D] + q for q in Q])

# Exemple
if __name__ == "__main__":
    n = 3
    s = pavages(n)

    for p in s:
        print("".join(map(lambda t: t.value, p)))
