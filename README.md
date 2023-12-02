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

2. **TWPC - Top-visited Wiki Pages Collector (Python, wikiapi)**:
   Collects metadata about the top-visited Wikipedia pages.

3. **WPAP - Wikipedia Abstract Processor (Python, Networkx)**:
   Processes Wikipedia dump files to create the **Wikipedia Abstracts Graph (WPAG)**, based on **Target Entities (
   user-selected Wikipedia pages)**.

4. **ESGB - Entity Summarization Graph Builder (Python, Neo4j, Postgres, Networkx)**:
   Constructs the **Entity Summarization Graph (ESG)**, comprising Target Entities and their summaries derived from the
   intersection of WDG and WPAG nodes. This module also ensures ESG remains a single component by adding necessary nodes
   and edges.

5. **ESGE - Entity Summarization Graph Expander (Python, Neo4j-GDS, Postgres)**:
   Expands ESG by sampling from WDG using the Random Walk with Restarts algorithm in the Neo4j-GDS plugin, starting from
   the Target Entities.

6. **ESGER - Entity Summarization Graph Edge Refiner (Python, Spacy-NLP, Networkx, Postgres)**:
   Refines the **Entity Summarization Graph (ESG)** by selectively retaining the most relevant edge label for each
   pair of nodes, utilizing NLP tools to evaluate and choose the most pertinent label from multiple edge labels.
   Ultimately, transforming the ESG into a directed, labeled graph with meaningful context-based connections.

7. **WESC - Wiki Entity Summarization Commons (Python, Neo4j, Postgres)**:
   Utility packages and shared resources.

## Getting Started

- Update the submodules by executing the following:
   ```shell
   git submodule init
   git submodule update
   ```
