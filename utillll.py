

NEO4J_URI = 'neo4j+ssc://806970c7.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = "ntVYbR1v-6OrHleeKhs7WC22VRXmpM7fPbhNddc3QRw"
NEO4J_DATABASE = "neo4j"
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

from neo4j import GraphDatabase

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
session = driver.session(database=NEO4J_DATABASE)
