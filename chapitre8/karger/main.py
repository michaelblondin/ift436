from manim  import *
from random import randint, randrange

EDGE_WIDTH = 3
LAYOUT     = "circular"

def arete(u, v):
    return frozenset({u, v})

class Karger(Scene):
    def extract(self, u, v):
        return (u, v) if (u, v) in self.G.edges else (v, u)

    # Générer décompte des coupes
    def gen_tab(self):
        FORMAT = "#{:>2}:"
        label  = Text(FORMAT.format(1),
                      font_size = 16,
                      font = "Fira Mono").to_edge(UL)

        self.tab = [{"label": label, "value": 0}]

        for i in range(1, len(self.E)):
            label = Text(FORMAT.format(i+1),
                         font_size = 16,
                         font = "Fira Mono").next_to(label, DOWN)
        
            self.tab.append({"label": label, "value": 0})

        animation = []
        
        for i, _ in enumerate(self.tab):
            label = self.tab[i]["label"]
            tally = Text("0",
                         font_size = 16,
                         font = "Fira Mono").next_to(label, RIGHT)
            
            self.tab[i]["tally"] = tally

            animation.append(Write(label))
            animation.append(Write(tally))

        self.play(*animation)
        self.wait(duration = self.speed)
        
    # Animer une itération de l'algo. de Karger
    def anim_merge(self, u, v):
        self.G[u].stroke_width = 5
        self.G[u].stroke_color = "RED"

        self.G[v].stroke_width = 5
        self.G[v].stroke_color = "RED"

        e = self.extract(u, v)
        
        self.G.edges[e].stroke_width = 5
        self.G.edges[e].stroke_color = "RED"

        uv  = u + v
        pos = (self.G.vertices[u].get_center() +
               self.G.vertices[v].get_center()) / 2
        
        self.play(self.G.animate.add_vertices(
            uv,
            labels = True,
            positions     = {uv: pos},
            vertex_config = {uv: {"stroke_color": BLUE,
                                  "stroke_width": 5}}),
            run_time = self.speed)
        self.wait(duration = self.speed)
                
        self.play(Transform(self.G[u], self.G[uv]), run_time = self.speed)
        self.play(Transform(self.G[v], self.G[uv]), run_time = self.speed)

        to_remove = {arete(u, v)}
        to_create = set()
        
        for e in self.E:
            if len(e & arete(u, v)) == 1:
                x, y = e
                f = self.extract(x, y)
                c = self.P[e]

                z = x if y in arete(u, v) else y
                g = arete(uv, z)
                
                to_remove.add(e)
                self.P.pop(e)
                self.G.remove_edges(f)

                if g not in to_create:
                   to_create.add(g)

                   self.P[g] = c
                   
                   self.G.add_edges((uv, z))
                   self.G.edges[uv, z].stroke_width = EDGE_WIDTH * c
                else:
                    self.P[g] += c
                    self.G.edges[uv, z].stroke_width += EDGE_WIDTH * c
                   
        self.G.remove_vertices(u)
        self.G.remove_vertices(v)

        self.V.remove(u)
        self.V.remove(v)
        self.V.add(uv)

        self.E -= to_remove
        self.E |= to_create

        self.P.pop(arete(u, v))

        self.G.vertices[uv].stroke_width = 1
        self.G.vertices[uv].stroke_color = "WHITE"

        self.play(self.G.animate.change_layout(LAYOUT),
                  run_time = self.speed)
        self.wait(duration = self.speed)

    # Animer une exécution de l'algo. de Karger
    def exec_karger(self):
        while len(self.V) > 2:
            u, v = list(self.E)[randrange(len(self.E))]

            self.anim_merge(u, v)

        u, v = self.V

        val  = self.P[arete(u, v)]
        pos  = (self.G.vertices[u].get_center() +
                self.G.vertices[v].get_center()) / 2
        res  = Text(str(val)).next_to(pos, DOWN)

        self.add(res)

        # Mettre décompte à jour
        entry = self.tab[val-1]
        
        entry["value"] += 1
        
        count     = entry["value"]
        new_tally = Text(str(count),
                         font_size = 16,
                         font = "Fira Mono").next_to(entry["label"])

        self.play(Transform(entry["tally"], new_tally),
                  run_time = self.speed)

        self.wait(duration = self.speed)
        self.remove(res)

    def gen_graph(self):
        # Graphe des notes de cours
        # self.V = {"a", "b", "c", "d", "e"}
        # self.E = {arete("a", "b"), arete("a", "c"),
        #           arete("a", "d"), arete("b", "c"),
        #           arete("b", "d"), arete("b", "e"),
        #           arete("c", "d"), arete("c", "e")}

        # Autre graphe
        self.V = {"a", "b", "c", "d", "e", "f", "g", "h", "i"}
        self.E = {arete("a", "b"), arete("a", "c"), arete("a", "d"),
                  arete("a", "i"), arete("b", "d"), arete("b", "e"),
                  arete("b", "g"), arete("b", "i"), arete("c", "d"),
                  arete("c", "f"), arete("c", "i"), arete("d", "e"),
                  arete("d", "f"), arete("d", "h"), arete("d", "i"),
                  arete("e", "f"), arete("e", "g"), arete("e", "h"),
                  arete("f", "g"), arete("f", "h"), arete("g", "h")}
        
        self.P = {e: 1 for e in self.E}

        vertices = list(self.V)
        edges    = list(map(tuple, self.E))
        
        return Graph(vertices,
                     edges,
                     layout = LAYOUT,
                     labels = True,
                     vertex_config = {v: {"radius": 0.3} for v in self.V},
                     edge_config   = {e: {"stroke_width": EDGE_WIDTH}
                                      for e in edges})

    # Point d'entrée de la scène
    def construct(self):
        self.speed = 1

        # Générer et afficher graphe
        self.G = self.gen_graph()
        self.play(Create(self.G), run_time = self.speed)
        self.wait(duration = self.speed)

        # Générer tableau des décomptes
        self.gen_tab()

        # Exécuter l'algo. de Karger n fois
        n = 100
        
        for _ in range(n):
            self.exec_karger()
            self.speed /= 5.0

            self.remove(self.G)

            self.G = self.gen_graph()
            self.play(Create(self.G), run_time = self.speed)
            self.wait(duration = self.speed)
