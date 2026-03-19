import os
import json
import time
import hashlib
import glob
import uuid

import requests

from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE, GITHUB_TOKEN, NODE_ID_ACCESSOR

AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

p = print


# --- Helper Functions ---

def get_cache_filename(key: str, cache_dir='.', ext='json'):
    """Generate filename from key (namespace for cache)."""
    hashed = hashlib.sha256(key.encode('utf-8')).hexdigest()
    return os.path.join(cache_dir, f'cache_{hashed}.{ext}')

def load_cache_generic(key, expiry_seconds=600, cache_dir='.'):
    """Load cache by key. Returns None if not found or expired."""
    fn = get_cache_filename(key, cache_dir)
    if not os.path.exists(fn):
        return None
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            cache = json.load(f)
    except Exception:
        return None
    if time.time() - cache.get('time', 0) > expiry_seconds:
        return None
    return cache['data']

def save_cache_generic(key, data, cache_dir='.'):
    """Save cache data with the given key."""
    fn = get_cache_filename(key, cache_dir)
    cache = {'time': time.time(), 'data': data}
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(cache, f)

def clear_all_caches(cache_dir='.'):
    """Remove all cache files created by the generic cache system."""
    pattern = os.path.join(cache_dir, 'cache_*.json')
    deleted = 0
    for cache_file in glob.glob(pattern):
        try:
            os.remove(cache_file)
            deleted += 1
        except Exception as e:
            print(f"Failed to delete {cache_file}: {e}")
    print(f"Deleted {deleted} cache files.")
    return deleted


# --- Cypher Helpers ---

def run_cypher_any(session, query):
    """Run arbitrary Cypher query. Returns list of dicts."""
    result = session.run(query)
    return result.data()


# --- Read Operations ---

def get_record_with_specific_id(tx, id):
    p("get_record_with_specific_id called with id:", id)
    query = f'''
    MATCH (n)
        WHERE n.{NODE_ID_ACCESSOR} = $id
        RETURN n
    '''
    result = tx.run(query, id=id)
    return list(result)

def get_specific_node_with_specific_id(session, id):
    p("get_specific_node_with_specific_id called with id:", id)
    k = session.execute_read(get_record_with_specific_id, id=id)
    nodes = []
    for record in k:
        node = record['n']
        node_dict = dict(node)
        label_list = list(node.labels)
        nodes.append({
            "properties": node_dict,
            "labels": label_list
        })
    return nodes

def get_node_with_specific_property(tx, property):
    p("get_node_with_specific_property called with property:", property)
    query = f'''
    MATCH (n)
        WHERE n.`{property}` IS NOT NULL
        RETURN n
    '''
    result = tx.run(query)
    return list(result)

def print_number_of_node_and_number_of_connections(session):
    p("print_number_of_node_and_number_of_connections called")
    def get_number_of_nodes():
        result = session.run("MATCH (n) RETURN count(n) as total")
        for record in result:
            print(record["total"])
    get_number_of_nodes()

    def get_number_of_connections():
        result = session.run("MATCH ()-->() RETURN count(*) as total")
        for record in result:
            print(record["total"])
    get_number_of_connections()

def get_every_node(tx):
    p("get_every_node called")
    return list(tx.run('MATCH (n) RETURN n'))

def get_all_nodes__and__their_connections(session):
    p("get_all_nodes__and__their_connections called")
    def get_all_node_and_their_connections(session):
        result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
        return list(result)

    k = session.execute_read(get_all_node_and_their_connections)
    nodes = []
    nodesid = {}
    links = []
    for i in k:
        n = i["n"]
        m = i["m"]

        NID = dict(n)[NODE_ID_ACCESSOR]
        MID = dict(m)[NODE_ID_ACCESSOR]
        if NID not in nodesid:
            nodesid[NID] = 1
            nodes.append(dict(n))
        if MID not in nodesid:
            nodesid[MID] = 1
            nodes.append(dict(m))

        links.append({"source": NID, "target": MID})

    p(len(nodes))
    p(len(links))

    def get_alone_nodes(session):
        result = session.run('''
        MATCH (n)
        WHERE NOT EXISTS ((n)--())
        RETURN n
        ''')
        return list(result)

    k = session.execute_read(get_alone_nodes)
    for i in k:
        n = i["n"]
        NID = dict(n)[NODE_ID_ACCESSOR]
        if NID not in nodesid:
            nodesid[NID] = 1
            nodes.append(dict(n))

    return {"nodes": nodes, "links": links}

def get_all_connections(session):
    p("get_all_connections called")
    result = session.run("MATCH ()-[r]->() RETURN r")
    return list(result)

def _get_constraints(tx):
    p("_get_constraints called")
    query = "SHOW CONSTRAINTS"
    result = tx.run(query)
    return [record for record in result]


# --- GitHub ---

def get_github_repositories(cache_expiry=60000000000000):
    CACHE_KEY = 'github_user_repos_v1'
    repos = load_cache_generic(CACHE_KEY, expiry_seconds=cache_expiry)
    if repos is not None:
        print("Loaded from cache")
    else:
        url = "https://api.github.com/user/repos"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        repos = []
        page = 1
        while True:
            response = requests.get(url, headers=headers, params={'per_page': 100, 'page': page})
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
                break
            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1
        save_cache_generic(CACHE_KEY, repos)

    print("| Name | Full Name | Private | HTML URL |")
    print("|------|-----------|---------|----------|")
    for repo in repos:
        print(f"| {repo['name']} | {repo['full_name']} | {repo['private']} | {repo['html_url']} |")
    return repos


# --- Write Operations ---

def update_position_of_all_node(session, data, prefix):
    p("update_position_of_all_node called with data:", data)

    output_data = []
    for item in data:
        output_data.append({
            "ID": item[NODE_ID_ACCESSOR],
            "X": item["X"],
            "Y": item["Y"],
            "Z": item["Z"]
        })

    def update_nodes(tx, data):
        query = (
            f"""
            UNWIND $data AS item
            MATCH (n {{{NODE_ID_ACCESSOR}: item.ID}})
            SET n.{prefix}_X = item.X,
                n.{prefix}_Y = item.Y,
                n.{prefix}_Z = item.Z
            RETURN n.{NODE_ID_ACCESSOR} AS node_id, n.{prefix}_X AS X, n.{prefix}_Y AS Y, n.{prefix}_Z AS Z
            """
        )
        result = tx.run(query, data=data)
        return list(result)

    updated_nodes = session.execute_write(update_nodes, output_data)
    return updated_nodes

def update_color_of_all_nodes(session, color):
    query = '''
    MATCH (n)
    SET n.color = $color
    RETURN n
    '''
    result = session.run(query, color=color)
    return [record['n'] for record in result]


# --- Create Operations ---

def _create_constraint(tx, label, property):
    p("_create_constraint called with label:", label, "and property:", property)
    query = f"CREATE CONSTRAINT FOR  (n:{label}) REQUIRE  n.{property} IS UNIQUE"
    tx.run(query)

def create_node_tx(tx, name, id8):
    print("create_node_tx called with name:", name, "and id8:", id8)
    query = (
        f"CREATE (n:normalNode588888888 {{"
        f"name: $name, "
        f"{NODE_ID_ACCESSOR}: $id8}}) "
        f"RETURN n.{NODE_ID_ACCESSOR} AS node_id"
    )
    result = tx.run(query, name=name, id8=id8)
    record = result.single()
    return record["node_id"] if record else None

def create_node_with_generate_id(session, name):
    p("create_node_with_generate_id called with name:", name)
    node_id = session.execute_write(create_node_tx, name, str(uuid.uuid4()))
    return node_id

def create_node_tx_with_position(tx, name, id8, x, y, z):
    print("create_node_tx_with_position called with name:", name, "id8:", id8, "x:", x, "y:", y, "z:", z)
    query = (
        f"CREATE (n:normalNode588888888 {{"
        f"name: $name, "
        f"{NODE_ID_ACCESSOR}: $id8, "
        f"ue_location_X: $x, "
        f"ue_location_Y: $y, "
        f"ue_location_Z: $z}}) "
        f"RETURN n.{NODE_ID_ACCESSOR} AS node_id"
    )
    result = tx.run(query, name=name, id8=id8, x=x, y=y, z=z)
    record = result.single()
    return record["node_id"] if record else None

def create_node_with_generate_id_and_position(session, name, x, y, z):
    p("create_node_with_generate_id_and_position called with name:", name, "x:", x, "y:", y, "z:", z)
    node_id = session.execute_write(create_node_tx_with_position, name, str(uuid.uuid4()), x, y, z)
    return node_id


# --- Delete Operations ---

def remove_all(session):
    p("remove_all called")
    session.run("MATCH (n) DETACH DELETE n")

def delete_node_with_specific_id(tx, id):
    print("delete_node_with_specific_id called with id:", id)
    query = (
        f'''
        MATCH (n)
        WHERE n.{NODE_ID_ACCESSOR} = $id
        DETACH DELETE n
        RETURN count(n) as deletedCount
        '''
    )
    result = tx.run(query, id=id)
    record = result.single()
    return record["deletedCount"] if record else 0

def delete_node_with_specific_id_and_label(tx, label, id):
    print("delete_node_with_specific_id_and_label called with label:", label, "and id:", id)
    query = (
        f'''
        MATCH (n:{label})
        WHERE n.{NODE_ID_ACCESSOR} = $id
        DETACH DELETE n
        RETURN count(n) as deletedCount
        '''
    )
    result = tx.run(query, id=id)
    record = result.single()
    return record["deletedCount"] if record else 0
