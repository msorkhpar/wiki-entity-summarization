FROM python:3.9.18 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app

FROM base as poetry
RUN pip install poetry==1.7.1
COPY poetry.lock pyproject.toml /app/
RUN poetry export -o requirements.txt

FROM base as build
COPY --from=poetry /app/requirements.txt /tmp/requirements.txt
COPY configs/index_enwiki.db configs/index_enwiki.db
RUN python -m venv .venv && \
    .venv/bin/pip install 'wheel==0.42.0' && \
    .venv/bin/pip install -r /tmp/requirements.txt && \
    .venv/bin/python -m spacy download en_core_web_md  install

FROM python:3.9.18-slim as runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH
COPY --from=build /app/.venv /app/.venv
COPY --from=build /app/configs/index_enwiki.db /app/configs/index_enwiki.db
COPY commons /app/commons
COPY edge_refiner /app/edge_refiner
COPY graph_builder /app/graph_builder
COPY graph_expander /app/graph_expander
COPY top_visited_collector /app/top_visited_collector
COPY wikidata_graph_builder /app/wikidata_graph_builder
COPY wikipedia_abstract_processor /app/wikipedia_abstract_processor
COPY main.py /app/main.py

ENTRYPOINT ["python", "main.py"]
