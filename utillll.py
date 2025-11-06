

from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

from neo4j import GraphDatabase

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
session = driver.session(database=NEO4J_DATABASE)
