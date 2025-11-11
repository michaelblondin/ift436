;; À copier/coller sur https://compsys-tools.ens-lyon.fr/z3/ ou
;;                                                        en ligne de commande
;;
;; Problème du sac à dos avec c = 900, v = [ 50,   5,  65, 10,  12,  20]
;;                                  et p = [700, 320, 845, 70, 420, 180]

(declare-const x1 Int)
(declare-const x2 Int)
(declare-const x3 Int)
(declare-const x4 Int)
(declare-const x5 Int)
(declare-const x6 Int)
(declare-const valeur Int)

(assert (and (>= x1 0) (<= x1 1)))
(assert (and (>= x2 0) (<= x2 1)))
(assert (and (>= x3 0) (<= x3 1)))
(assert (and (>= x4 0) (<= x4 1)))
(assert (and (>= x5 0) (<= x5 1)))
(assert (and (>= x6 0) (<= x6 1)))

(assert (= valeur (+ (* 50 x1) (* 5 x2) (* 65 x3) (* 10 x4) (* 12 x5) (* 20 x6))))
(assert (<= (+ (* 700 x1) (* 320 x2) (* 845 x3) (* 70 x4) (* 420 x5) (* 180 x6)) 900))

(maximize valeur)

(check-sat)
(get-model)
