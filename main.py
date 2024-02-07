import os
import pickle

from dotenv import load_dotenv
from top_visited_collector.tvwpc import fetch_top_visited_wikipedia_pages
from wikipedia_abstract_processor.wpap import construct_wikipedia_abstract_graph
from graph_builder.esgb import construct_entity_summarization_graph
from graph_expander.eesg import construct_extended_entity_summarization_graph
from edge_refiner.esger import refine_multiple_edges

__stages_order = {
    # Top Visited Wikipedia Pages Collector
    "TVWPC": {
        "previous_stage": None,
        "pickle_env_key": None
    },
    # Wikipedia Abstract Processor
    "WPAP": {
        "previous_stage": None,
        "pickle_env_key": "WPG_PICKLE_PATH",
        "function": construct_wikipedia_abstract_graph
    },
    # Entity Summarization Graph Builder
    "ESGB": {
        "previous_stage": "WPAP",
        "pickle_env_key": "ESG_PICKLE_PATH",
        "function": construct_entity_summarization_graph
    },
    # Entity Summarization Graph Extender
    "ESGE": {
        "previous_stage": "ESGB",
        "pickle_env_key": "EESG_PICKLE_PATH",
        "function": construct_extended_entity_summarization_graph
    },
    # Entity Summarization Graph Edge Refiner
    "ESGER": {
        "previous_stage": "ESGE",
        "pickle_env_key": "ELESG_PICKLE_PATH",
        "function": refine_multiple_edges
    },
}


def get_path(graph_path):
    path = os.getenv(graph_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def construct_graph(**stage_function_kwargs):
    stage_name = os.getenv("APP_MODULE")
    previous_stage_name = __stages_order[stage_name]["previous_stage"]
    previous_stage_pickle_env_key = None if previous_stage_name is None \
        else __stages_order[previous_stage_name]["pickle_env_key"]
    stage_function = __stages_order[stage_name]["function"]
    stage_pickle_path = get_path(__stages_order[stage_name]["pickle_env_key"])

    # Load previous stage graph if exists
    if previous_stage_pickle_env_key is not None:
        previous_stage_pickle_path = os.getenv(previous_stage_pickle_env_key)
        if not os.path.exists(previous_stage_pickle_path):
            raise FileNotFoundError(
                f"`${previous_stage_pickle_path}` does not exist! Please run the {previous_stage_name} first!"
            )

        with open(previous_stage_pickle_path, 'rb') as f:
            previous_stage_graph = pickle.load(f)

        target_stage_graph = stage_function(previous_stage_graph, **stage_function_kwargs)
    # Run an independent stage
    else:
        target_stage_graph = stage_function(**stage_function_kwargs)

    with open(stage_pickle_path, 'wb') as f:
        pickle.dump(target_stage_graph, f)

    print(f"{stage_name} stage is done and its graph has been saved to `{stage_pickle_path}`")


if __name__ == '__main__':
    load_dotenv(".env")
    os.makedirs(os.path.dirname(os.getenv("OUTPUT_VOLUME_PATH")), exist_ok=True)

    app = os.getenv("APP_MODULE")
    if app is None or app not in __stages_order:
        raise ValueError(
            f'Invalid app module should be one of the following:'
            f'"TVWPC" Top-visited Wiki Pages Collector | "WPAP" Wikipedia Abstract Processor |'
            f' "ESGB" Entity Summarization Graph Builder | "ESGE" Entity Summarization Graph Expander |'
            f' "ESGER" Entity Summarization Graph Edge Refiner'
        )

    for root, dirs, files in os.walk("./configs"):
        for file in files:
            if file.endswith(".env"):
                load_dotenv(os.path.join(root, file))

    if app == "TVWPC":
        fetch_top_visited_wikipedia_pages(
            top_n=int(os.getenv("TOP_N")),
            output_csv_path=get_path("TOP_VISITED_CSV_PATH"),
            to_year=int(os.getenv("TO_YEAR")),
            to_month=int(os.getenv("TO_MONTH")),
            from_year=int(os.getenv("FROM_YEAR")),
            from_month=int(os.getenv("FROM_MONTH"))
        )
    elif app == "WPAP":
        construct_graph(
            dumps_path=os.getenv("WIKIPEDIA_DUMPS_PATH"),
            multistream=bool(os.getenv("WIKIPEDIA_MULTISTREAM"))
        )
    elif app == "ESGE":
        construct_graph(
            walk_len=int(os.getenv("EESG_WALK_LENGTH")),
            max_limit_per_node=int(os.getenv("EESG_MAX_WALK_PER_NODE"))
        )
    else:
        construct_graph()
