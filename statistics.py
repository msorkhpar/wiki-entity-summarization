import os
import pickle
import networkx as nx
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def basics(eesg):
    graph_type = {
        nx.MultiDiGraph: " Multi Directed Graph",
        nx.MultiGraph: " Multi Graph",
        nx.DiGraph: "Directed Graph",
        nx.Graph: "Undirected Graph",
    }
    print(f"Graph type: {graph_type[type(eesg)]}")
    print(f"Number of Nodes: [{eesg.number_of_nodes()}]")
    print(f"Number of Edges: [{eesg.number_of_edges()}]")
    print(f"Density: [{nx.density(eesg)}]")
    print(f"Average Degree {sum(dict(eesg.degree()).values()) / eesg.number_of_nodes()}")
    print(f"Number of Triangles: {sum(nx.triangles(eesg.to_undirected()).values()) / 3}")

    # Connected Components
    if type(eesg) == nx.MultiDiGraph or type(eesg) == nx.DiGraph:
        print(f"Weakly Connected Components : [{nx.number_weakly_connected_components(eesg)}]")
    else:
        print(f"Connected Components : [{nx.number_connected_components(eesg)}]")


def diameter(undirected_eesg):
    print(f"Diameter: [{nx.diameter(undirected_eesg)}]")
    print(f"Average Shortest Path Length: [{nx.average_shortest_path_length(undirected_eesg)}]")


def degree_distribution(eesg):
    degrees = [eesg.degree(n) for n in eesg.nodes()]

    plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(2, 3)

    ax1 = plt.subplot(gs[0, 0])
    ax1.hist([d for d in degrees if 0 <= d <= 6], bins=4, color='blue')
    ax1.set_title('Degrees 0-6')

    ax2 = plt.subplot(gs[0, 1])
    ax2.hist([d for d in degrees if 6 < d <= 15], bins=5, color='red')
    ax2.set_title('Degrees 7-15')

    ax3 = plt.subplot(gs[0, 2])
    ax3.hist([d for d in degrees if 15 < d <= 100], bins=8, color='green')
    ax3.set_title('Degrees 16-100')

    ax4 = plt.subplot(gs[1, 0])
    ax4.hist([d for d in degrees if 100 < d <= 600], bins=8, color='gray')
    ax4.set_title('Degrees 100-600')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    load_dotenv(".env")
    os.makedirs(os.path.dirname(os.getenv("OUTPUT_VOLUME_PATH")), exist_ok=True)
    load_dotenv("configs/esge.env")
    eesg_path = os.getenv("EESG_PICKLE_PATH")

    with open(eesg_path, 'rb') as f:
        eesg = pickle.load(f)

    undirected_eesg = nx.Graph()
    undirected_eesg.add_nodes_from(eesg.nodes(data=True))
    for u, v in eesg.edges():
        undirected_eesg.add_edge(u, v)

    basics(eesg)
    diameter(undirected_eesg)
    degree_distribution(eesg)
