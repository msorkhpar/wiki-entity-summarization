import os
import pickle
import networkx as nx
from dotenv import load_dotenv
from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, MultiLine, NodesAndLinkedEdges
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8
from bokeh.transform import linear_cmap


# Load if you want to use bokeh in jupyter notebook
# output_notebook()

def map_numeric_label(eesg):
    G = nx.Graph()
    G.add_nodes_from(eesg.nodes(data=True))
    for u, v in eesg.edges():
        G.add_edge(u, v)

    mapping = dict((n, i) for i, n in enumerate(G.nodes))
    G = nx.relabel_nodes(G, mapping)
    for node in G.nodes:
        for key in G.nodes[node]:
            G.nodes[node][key] = str(G.nodes[node][key])
    mapping = {v: k for k, v in mapping.items()}
    return G, mapping


# https://melaniewalsh.github.io/Intro-Cultural-Analytics/06-Network-Analysis/02-Making-Network-Viz-with-Bokeh.html#import-libraries
def generate_chart(G, output_path=None, title="Entity Summarization Graph", width=1024, height=920, scale=100 ):
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'adjusted_node_size'
    node_highlight_color = 'white'
    edge_highlight_color = 'black'
    color_palette = Blues8
    plot_width = width
    plot_height = height

    degrees = dict(nx.degree(G))
    nx.set_node_attributes(G, name='degree', values=degrees)

    number_to_adjust_by = 3
    adjusted_node_size = dict([(node, degree + number_to_adjust_by) for node, degree in nx.degree(G)])
    nx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

    tooltips = [
        ("Wikipedia Title", "@wikipedia_title"),
        ("Is a Root", "@is_root"),
        ("Wikidata Id", "@wikidata_id"),
        ("Wikidata Label", "@wikidata_label"),
        ("Wikidata Description", "@wikidata_description"),
        ("Degree", "@degree")
    ]

    plot = figure(tooltips=tooltips,
                  tools="pan,wheel_zoom,save,reset,tap", active_scroll='wheel_zoom',
                  width=plot_width, height=plot_height,
                  x_range=Range1d(-scale - .1, scale + .1), y_range=Range1d(-scale - .1, scale + .1), title=title)

    network_graph = from_networkx(G, nx.spring_layout, scale=scale, center=(0, 0))

    minimum_value_color = min(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    maximum_value_color = max(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute,
                                               fill_color=linear_cmap(color_by_this_attribute, color_palette,
                                                                      minimum_value_color, maximum_value_color))
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.35, line_width=0.5)

    network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                     line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color,
                                                         line_width=2)
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(network_graph)

    # show(plot)
    save(plot, filename=os.path.join(output_path, f"{title}.html"))


if __name__ == '__main__':
    load_dotenv(".env")
    os.makedirs(os.path.dirname(os.getenv("OUTPUT_VOLUME_PATH")), exist_ok=True)
    load_dotenv("configs/esger.env")
    elesg_path = os.getenv("ELESG_PICKLE_PATH")

    with open(elesg_path, 'rb') as f:
        elesg = pickle.load(f)

    G, mapping = map_numeric_label(elesg)
    generate_chart(
        G,
        os.getenv("OUTPUT_VOLUME_PATH"),
        "Wiki-ES(100_roots_with_200_random_walks)"
    )
