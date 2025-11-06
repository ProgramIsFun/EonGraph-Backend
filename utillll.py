

pw = "B0QqyzMOAO86pdmKRCh-H6R_jzO_RWOAY2-ReiEIQgo"
us = "neo4j"
# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://7dfcacd0.databases.neo4j.io"
URI2 = "neo4j+ssc://7dfcacd0.databases.neo4j.io"
AUTH = (us, pw)

# ==================================================

URL3='neo4j+s://b8cec73f.databases.neo4j.io'
PW='zFi_GDAUKlbIi-GOzgCibPya_kiVku5BXReI1A25Ifw'
AUTH = (us, PW)


# ==================================================


NEO4J_URI='neo4j+s://806970c7.databases.neo4j.io'
NEO4J_USERNAME='neo4j'
NEO4J_PASSWORD="ntVYbR1v-6OrHleeKhs7WC22VRXmpM7fPbhNddc3QRw"
NEO4J_DATABASE="neo4j"
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

# =========================================

NEO4J_URI = 'neo4j+ssc://806970c7.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = "ntVYbR1v-6OrHleeKhs7WC22VRXmpM7fPbhNddc3QRw"
NEO4J_DATABASE = "neo4j"
AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

from neo4j import GraphDatabase

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
session = driver.session(database=NEO4J_DATABASE)
