# Wiki ES

## Overview

This repository hosts a comprehensive suite for generating graph-based summaries of entities from user-chosen Wikipedia
pages. Through interconnected modules, it utilizes data from Wikidata and Wikipedia dumps to build a detailed dataset.
The project employs NLP (Natural Language Processing) techniques to refine the labels on the graph's connections,
ensuring these labels are relevant and meaningful. This process enhances the graph's systematic structure and enriches
it with contextual details, providing a thorough understanding of the relationships between entities.
Additionally, the project involves generating auto-generated ground truths, which aid in gaining a clear and
comprehensive view of these entity relationships.

## Modules Overview

1. **WDGB - Wikidata Graph Builder (Java, Spring, Neo4J, Postgres)**:
   Processes Wikidata dump files to create the **Wikidata Graph (WDG)**, storing parsed entity relations in Neo4j and
   PostgreSQL databases.

2. **TVWPC - Top-visited Wiki Pages Collector (Python, wikiapi)**:
   Collects metadata about the top-visited Wikipedia pages.

3. **WPAP - Wikipedia Abstract Processor (Python, Networkx)**:
   Processes Wikipedia dump files to create the **Wikipedia Abstracts Graph (WPAG)**, based on **Root Entities (
   user-selected Wikipedia pages)**.

4. **ESGB - Entity Summarization Graph Builder (Python, Neo4j, Postgres, Networkx)**:
   Constructs the **Entity Summarization Graph (ESG)**, comprising Root Entities and their summaries derived from the
   intersection of WDG and WPAG nodes. This module also ensures ESG remains a single component by adding necessary nodes
   and edges.

5. **ESGE - Entity Summarization Graph Expander (Python, Neo4j-GDS, Postgres)**:
   Constructs **Expand Entity Summarization Graph(EESG)** by sampling from WDG using the Random Walk with Restarts
   algorithm in the Neo4j-GDS plugin, starting from
   the Root Entities.

6. **ESGER - Entity Summarization Graph Edge Refiner (Python, Spacy-NLP, Networkx, Postgres)**:
   Refines the **Entity Summarization Graph (ESG)** by selectively retaining the most relevant edge label for each
   pair of nodes, utilizing NLP tools to evaluate and choose the most pertinent label from multiple edge labels.
   Ultimately, convert the heterogeneous (ESGE) graph to a labeled directed graph named **Expanded Labeled Entity
   Summarization Graph (ELESG)**.

7. **WESC - Wiki Entity Summarization Commons (Python, Neo4j, Postgres)**:
   Utility packages and shared resources.

## Getting Started

- Update the submodules by executing the following:
   ```shell
   git submodule init
   git submodule update --init --remote --recursive
   ```
- Install poetry:
  ```shell
  pip install poetry
  poetry config virtualenvs.in-project true
  poetry install --no-root
  poetry shell
  ```
- Generate config files:
  ```shell
   ./config-files-generator.sh
    ```
- Environment variables:

| Variable                                         | Default                                                                  | File                  | Description                                                                                                                   |
|--------------------------------------------------|--------------------------------------------------------------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------| 
| `POSTGRES_VOLUME_PATH`                           | `/data/pg-data`                                                          | `.env`                | PG container volume path                                                                                                      |
| `NEO4J_VOLUME_PATH`                              | `/data/neo4j-data`                                                       | `.env`                | Neo4j container volume path                                                                                                   |
| `WIKIDATA_DUMPS_PATH`                            | `/data/wikidata/articles/`                                               | `.env`                | Wikidata raw dumps path                                                                                                       |
| `WIKIPEDIA_DUMPS_PATH`                           | `/data/wikipedia/articles/`                                              | `.env`                | Wikipedia raw dumps path                                                                                                      |
| `JUPYTER_VOLUME_PATH`                            | `/data/jupyter-data`                                                     | `.env`                | Jupyter container path                                                                                                        |
| `OUTPUT_VOLUME_PATH`                             | `/data/wiki-es-output`                                                   | `.env`                | Project output directory                                                                                                      |
| `DB_NAME`                                        | `wikies`                                                                 | `.env`                | PG database name                                                                                                              |
| `DB_USER`                                        | `wikies`                                                                 | `.env`                | PG username                                                                                                                   |
| `DB_PASSWORD`                                    | `password`                                                               | `.env`                | PG password                                                                                                                   |
| `NEO4J_USER`                                     | `neo4j`                                                                  | `.env`                | Neo4j user                                                                                                                    |
| `NEO4J_PASSWORD`                                 | `password`                                                               | `.env`                | Neo4j password                                                                                                                |
| `JUPYTER_TOKEN`                                  | `wikies`                                                                 | `.env`                | Jupyter server auth token                                                                                                     |
| `DB_HOST`                                        | `wiki-es-pg`                                                             | `.env`                | PG host name                                                                                                                  |
| `NEO4J_HOST`                                     | `wiki-es-neo`                                                            | `.env`                | Neo4j host name                                                                                                               |
| `DB_PORT`                                        | `5432`                                                                   | `.env`                | PG port number                                                                                                                |
| `APP_MODULE`                                     | `TVWPC`                                                                  | `.env`                | Application mode to run `TVWPC`, `WPAP`,`ESGB`,`ESGE`, or `ESGER`                                                             |
| `NEO4J_PLUGINS`                                  | `'[\"graph-data-science\",\"apoc\"]'`                                    | `configs/neo4j.env`   | Neo4j active plugins                                                                                                          |
| `NEO4J_dbms_security_procedures_unrestricted`    | `gds.*`                                                                  | `configs/neo4j.env`   | GDS security restriction                                                                                                      |
| `NEO4J_server_config_strict__validation_enabled` | `false`                                                                  | `configs/neo4j.env`   | Neo4j strict validation                                                                                                       |
| `NEO4J_server_memory_heap_initial__size`         | `1000m`                                                                  | `configs/neo4j.env`   | https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/#config_server.memory.heap.initial_size |
| `NEO4J_server_memory_heap_max__size`             | `1000m`                                                                  | `configs/neo4j.env`   | https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/#config_server.memory.heap.max_size     |
| `NEO4J_server_memory_pagecache_size`             | `1000m`                                                                  | `configs/neo4j.env`   | https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/#config_server.memory.pagecache.size    |
| `NEO4J_dbms_memory_transaction_total_max`        | `1000m`                                                                  | `configs/neo4j.env`   | https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/#config_db.memory.transaction.total.max |
| `NOTEBOOK_ARGS`                                  | `"--NotebookApp.token='${JUPYTER_TOKEN}'"`                               | `configs/jupyter.env` | Notebook Args                                                                                                                 |
| `TOP_N`                                          | `2000`                                                                   | `configs/tvwpc.env`   | Maximum top N number to keep                                                                                                  |
| `TOP_VISITED_CSV_PATH`                           | `\${OUTPUT_VOLUME_PATH}/top_\${TOP_N}_visited_wikipedia_pages.csv`       | `configs/tvwpc.env`   | Top N pages output file                                                                                                       |
| `TO_YEAR`                                        | `2023`                                                                   | `configs/tvwpc.env`   | End year for top visited pages                                                                                                |
| `TO_MONTH`                                       | `5`                                                                      | `configs/tvwpc.env`   | End month for top visited pages                                                                                               |
| `FROM_YEAR`                                      | `2015`                                                                   | `configs/tvwpc.env`   | Start year for top visited pages                                                                                              |
| `FROM_MONTH`                                     | `7`                                                                      | `configs/tvwpc.env`   | Start month for top visited pages                                                                                             |
| `WPG_PICKLE_PATH`                                | `\${OUTPUT_VOLUME_PATH}/wikipedia-abstract-graph.pkl`                    | `configs/wpap.env`    | Wikipedia abstract pickle file path                                                                                           |
| `ESG_PICKLE_PATH`                                | `\${OUTPUT_VOLUME_PATH}/entity-summarization-multi-graph.pkl`            | `configs/esgb.env`    | Wikidata graph and Wikipedia abstract graph intersection graph pickle file                                                    |
| `EESG_PICKLE_PATH`                               | `\${OUTPUT_VOLUME_PATH}/expanded-entity-summarization-multi-graph.pkl`   | `configs/esge.env`    | Expanded ES graph pickle file                                                                                                 |
| `EESG_WALK_LENGTH`                               | `3`                                                                      | `configs/esge.env`    | Random walk path length                                                                                                       |
| `EESG_MAX_WALK_PER_NODE`                         | `200`                                                                    | `configs/esge.env`    | Number of paths from each target node to run                                                                                  |
| `ELESG_PICKLE_PATH`                              | `\${OUTPUT_VOLUME_PATH}/expanded-labeled-entity-summarization-graph.pkl` | `configs/esger.env`   | Expanded labeled digraph pickle path (the final output)                                                                       |

## Run the project on Docker:
 - Provide the necessary environment variables in the `.env` file and other related to the app mode in the
   corresponding `.env` file in the `configs` directory.
 - Follow [wikimapper's documentation](https://github.com/jcklie/wikimapper) and place the generated sqllite file
   inside the configs as `configs/index_enwiki.db`.
 - Modify `configs/root_entities.csv` to include the root entities wikipedia page-id that you want to build the graph from.
 - Run the docker-compose file:
   ```shell
   docker-compose up -d {container_name} # wdgb, tvwpc, wpap, esgb, esge, esger, jupyter
   ```

## Run the project on local Python environment:
 - Provide the necessary environment variables in the `.env` file and other related to the app mode in the
   corresponding `.env` file in the `configs` directory.
 - Initialize the dependencies:
   ```shell
     poetry install --no-root
     poetry shell
     python -m spacy download en_core_web_md install
   ```
 - Follow [wikimapper's documentation](https://github.com/jcklie/wikimapper) and place the generated sqllite file
   inside the configs as `configs/index_enwiki.db`.
 - Modify `configs/root_entities.csv` to include the root entities wikipedia page-id that you want to build the graph from.
 - Run main.py:
   ```shell
    python main.py
    ```

## Loading the dataset:
The dataset is stored in the GitHub release as a pickle files.
```python
import pickle
import networkx as nx

with open('wikipedia-abstract-graph.pkl', 'rb') as f:
    wpag = pickle.load(f)

with open('entity-summarization-multi-graph.pkl', 'rb') as f:
    esg = pickle.load(f)

with open('expanded-entity-summarization-multi-graph.pkl', 'rb') as f:
    eesg = pickle.load(f)

with open('expanded-labeled-entity-summarization-graph.pkl', 'rb') as f:
    elesg = pickle.load(f)

print(next(iter(elesg.nodes(data=True))))
'''
('Q43416', data = {
    'is_root': True,
    'wikidata_id': 'Q43416',
    'wikipedia_id': 16603,
    'wikipedia_title': 'Keanu_Reeves',
    'wikidata_label': 'Keanu Reeves',
    'wikidata_description': 'Canadian actor'
})
'''

print(next(iter(elesg.edges(data=True))))
'''
('Q43416', 'Q3820', data = {
    'predicate': 'P19',
    'is_summary': True
 })
 
 (Keanu Reeves) - (place of birth) -> (Beirut)  
'''
```