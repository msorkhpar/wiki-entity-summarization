from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def find_path(self, start_node, end_node, forbidden_nodes):
        query = """
        MATCH (start {entityName: $start_node}), (end {entityName: $end_node})
        CALL apoc.algo.allSimplePaths(start, end, 'RELATIONSHIP_TYPE', 10) YIELD path
        WHERE NONE(node IN nodes(path) WHERE node.entityName IN $forbidden_nodes)
        RETURN path
        ORDER BY length(path) ASC
        LIMIT 1
        """
        with self.__driver.session() as session:
            result = session.run(query, start_node=start_node, end_node=end_node, forbidden_nodes=forbidden_nodes)
            return [record["path"] for record in result]


# Usage
conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="password")
try:
    path = conn.find_path("StartEntityName", "EndEntityName", ["ForbiddenEntity1", "ForbiddenEntity2"])
    print("Path found:", path)
finally:
    conn.close()
