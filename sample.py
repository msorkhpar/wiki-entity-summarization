from collections import defaultdict
from itertools import chain

import networkx as nx

from edge_refiner.esger import refine_multiple_edges

G = nx.MultiDiGraph()

G.add_node('A', is_root=True)
G.add_node('B', is_root=True)
G.add_node('F', is_root=True)
G.add_node('G', is_root=True)
G.add_node('H', is_root=True)
G.add_node('C', is_root=False)
G.add_node('D', is_root=False)
G.add_node('E', is_root=False)

G.add_edge('A', 'B', 'p2', predicate='p2', summary_for={'A', 'B'})
G.add_edge('A', 'F', 'p3', predicate='p3', summary_for={'A', 'F'})
G.add_edge('A', 'E', 'p5', predicate='p5')
G.add_edge('A', 'G', 'p1', predicate='p1', summary_for={'A'})
G.add_edge('A', 'G', 'p4', predicate='p4', summary_for={'A'})
G.add_edge('A', 'H', 'p4', predicate='p4', summary_for={'A'})

G.add_edge('B', 'A', 'p2', predicate='p2', summary_for={'A', 'B'})
G.add_edge('B', 'C', 'p1', predicate='p1', summary_for={'B'})
G.add_edge('B', 'A', 'p3', predicate='p3', summary_for={'A', 'B'})

G.add_edge('C', 'D', 'p2', predicate='p2')
G.add_edge('C', 'D', 'p3', predicate='p3')

G.add_edge('D', 'C', 'p2', predicate='p2')

G.add_edge('F', 'A', 'p2', predicate='p2', summary_for={'A', 'F'})

G.add_edge('H', 'A', 'p2', predicate='p2', summary_for={'A'})

for u, v, data in G.edges(data=True):
    print(f"({u} - {data['predicate']} -> {v})",
          "" if not data.get('summary_for') else f"summary for: {data['summary_for']}")

G_r = refine_multiple_edges(G)

print("*" * 40)
dataset = defaultdict(list)
for u, v, data in G_r.edges(data=True):
    print(f"({u} - {data['predicate']} -> {v})")
    if data.get('summary_for'):
        for root in data.get('summary_for'):
            dataset[root].append((u, v, data['predicate']))

for root, data in dataset.items():
    edges = ""
    for u, v, p in data:
        edges += f"({u} - {p} -> {v}), "

    print(f"Root: {root} -> {edges[:-2]}")
