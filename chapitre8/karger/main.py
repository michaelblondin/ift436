from manim  import *
from random import randint, randrange

                          # Pour graphe aléatoire:
LAYOUT       = "circular" # "kamada_kawai"
FIX_RADIUS   = False      # True
SHOW_LABELS  = True       # False
RADIUS       = 0.3        # 0.05
EDGE_WIDTH   = 2          # 0.25
BAR_WIDTH    = 0.1        # 0.2
X_LENGTH     = 3
CHART_FONT   = 16
CHART_LABELS = True       # False
TALLY_X_MAX  = 14         # 250
TALLY_Y_MAX  = 30         # 20
TALLY_Y_TICK = 20         # 5
BASE_SPEED   = 1          # 0.1
NUM_REP      = 100

def arete(u, v):
    return frozenset({u, v})

class Karger(Scene):
    def extract(self, u, v):
        return (u, v) if (u, v) in self.G.edges else (v, u)

    def update_chart(self, init = False):
        if CHART_LABELS:
            labels = [str(i) for i in range(1, len(self.tally) + 1)]
        else:
            labels = None
            
        chart  = BarChart(self.tally,
                          bar_names = labels,
                          bar_width = BAR_WIDTH,
                          y_range   = (0, TALLY_Y_MAX, TALLY_Y_TICK),
                          x_length  = X_LENGTH,
                          y_length  = 2,
                          x_axis_config = {"font_size":     CHART_FONT,
                                           "include_ticks": CHART_LABELS},
                          y_axis_config = {"font_size":     CHART_FONT})
        
        chart.scale(1.0)
        chart.to_corner(UL)

        val  = "∞" if init else min([i + 1 for i, v in enumerate(self.tally)
                                     if v > 0])
        text = Text("Minimum: " + str(val),
                    font_size = 16).next_to(chart, DOWN)

        if init:
            self.chart = chart
            self.text  = text
            self.play(Create(chart), run_time = self.speed)
            self.play(Write(text),   run_time = self.speed)
            self.wait(duration = self.speed)
        else:
            old_chart  = self.chart
            old_text   = self.text
            self.chart = chart
            self.text  = text
            self.play(ReplacementTransform(old_chart, chart,
                                           run_time = self.speed))
            self.remove(old_text)
            self.play(Write(text), run_time = self.speed)
        
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

        config = {uv: {"stroke_color": BLUE,
                       "stroke_width": 5}}

        if FIX_RADIUS:
            config[uv]["radius"] = RADIUS
        
        self.play(self.G.animate.add_vertices(uv,
                                              labels = SHOW_LABELS,
                                              positions     = {uv: pos},
                                              vertex_config = config),
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
        self.wait(duration = self.speed)

        self.tally[val-1] += 1
        self.update_chart()

        self.remove(res)

    def gen_graph(self):
        # # Graphe des notes de cours
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

        # # Graphe aléatoire
        # self.V = set("v" + str(i) for i in range(50))
        # self.E = {arete(u, v) for u in self.V for v in self. V
        #           if u != v and randint(1, 6) == 1}
        
        self.P = {e: 1 for e in self.E}

        vertices = list(self.V)
        edges    = list(map(tuple, self.E))
        
        return Graph(vertices,
                     edges,
                     layout = LAYOUT,
                     labels = SHOW_LABELS,
                     vertex_config = {v: {"radius": RADIUS} for v in self.V},
                     edge_config   = {e: {"stroke_width": EDGE_WIDTH}
                                      for e in edges})

    # Point d'entrée de la scène
    def construct(self):
        self.speed = BASE_SPEED
        self.n     = NUM_REP

        # Générer et afficher graphe
        self.G = self.gen_graph()
        self.play(Create(self.G), run_time = self.speed)
        self.wait(duration = self.speed)

        # Générer diagramme des décomptes
        self.tally = [0] * TALLY_X_MAX
        self.update_chart(init = True)
    
        # Exécuter l'algo. de Karger n fois
        for _ in range(self.n):
            self.exec_karger()
            self.speed /= 5.0

            self.remove(self.G)
            
            self.G = self.gen_graph()
            self.play(Create(self.G), run_time = self.speed)
            self.wait(duration = self.speed)

        self.wait(duration = 2)
