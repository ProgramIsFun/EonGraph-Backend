#!/usr/bin/env python
# coding: utf-8

# In[3]:


p=print
import uuid


# In[2]:


from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE,GITHUB_TOKEN

AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)

from neo4j import GraphDatabase

driver_ = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
session = driver_.session(database=NEO4J_DATABASE)


# In[ ]:


import os
import json
import time
import hashlib

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

import os
import glob

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


# ## Basic information.

# #### get_github_repositories
# 

# In[ ]:


import requests

def get_github_repositories(cache_expiry=600):
    CACHE_KEY = 'github_user_repos_v1'   # Can be made more specific e.g. by username
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

    # Markdown table output
    print("| Name | Full Name | Private | HTML URL |")
    print("|------|-----------|---------|----------|")
    for repo in repos:
        print(f"| {repo['name']} | {repo['full_name']} | {repo['private']} | {repo['html_url']} |")
    return repos


# In[12]:


a=get_github_repositories()


# #### get_specific_node_with_specific_id

# In[ ]:


def get_record_with_specific_id(tx, id):
    p("get_record_with_specific_id called with id:", id)
    query = f'''

    MATCH (n)
        WHERE n.user_generate_id_7577777777 = "{id}"
        RETURN n
    '''
    result = tx.run(query)
    return list(result)

# k=session.execute_read(get_record_with_specific_id, id="9b6097ab-f834-4789-a542-ced4f9478cc5")


# In[ ]:


def get_specific_node_with_specific_id(id):
    p("get_specific_node_with_specific_id called with id:", id)
    k=session.execute_read(get_record_with_specific_id, id=id)
    nodes = []
    for record in k:
        node = record['n']
        node_dict = dict(node)  # properties as dict
        label_list = list(node.labels)  # labels as list
        # Gather everything into one dict
        nodes.append({
            "properties": node_dict,
            "labels": label_list
        })
    return nodes
# get_specific_node_with_specific_id("9b6097ab-f834-4789-a542-ced4f9478cc5")


# #### get_nodewith_specific_property

# In[ ]:


def get_nodewith_specific_property(tx, property):
    p("get_nodewith_specific_property called with property:", property)
    query = f'''

    MATCH (n)
        WHERE n.`{property}` IS NOT NULL
        RETURN n
    '''
    result = tx.run(query)
    return list(result)
# k=session.execute_read(get_nodewith_specific_property, property="ue_location_X")


# In[29]:


# len(k)


# #### print_number_of_node_and_number_of_connections

# In[ ]:


def print_number_of_node_and_number_of_connections(session):
    p("print_number_of_node_and_number_of_connections called")
    # Get total number of node in the database.
    def get_number_of_nodes():
        result = session.run("MATCH (n) RETURN count(n) as total")
        for record in result:
            print(record["total"])
    get_number_of_nodes()


    # Get number of connections.
    def get_number_of_connections():
        result = session.run("MATCH ()-->() RETURN count(*) as total")
        for record in result:
            print(record["total"])
    get_number_of_connections()


# In[31]:


# print_number_of_node_and_number_of_connections(session)


# #### get_every_node

# In[ ]:


def get_every_node(tx):
    p("get_every_node called")
    return list(tx.run(
        '''
        MATCH (n) RETURN n

        '''
    ))
# result = session.execute_read(get_every_node)
# ppp=result[0]
# ppp2=ppp["n"]
# type(ppp2)
# ppp2.keys()
# dict(ppp2)


# In[ ]:


# ppp2


# In[ ]:


# ppp2.element_id


# In[ ]:





# #### get_all_node_and_their_connections13

# In[ ]:


def get_all_node_and_their_connections13(session):
    p("get_all_node_and_their_connections13 called")
    def get_all_node_and_their_connections(session):
        result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
        return list(result)

    k= session.execute_read(get_all_node_and_their_connections)
    len(k)
    k2=k[0]
    k2.keys()
    nodes=[]
    nodesid={}
    links=[]
    for i in k:
        n=i["n"]
        m=i["m"]

        NID=dict(n)["user_generate_id_7577777777"]
        Ninternal_id=n.element_id
        MID=dict(m)["user_generate_id_7577777777"]
        Minternal_id=m.element_id
        if NID not in nodesid:
            nodesid[NID]=1
            kkkk=dict(n)
            # kkkk["element_id"]=n.element_id
            nodes.append(kkkk)
        if MID not in nodesid:
            nodesid[MID]=1
            kkkk=dict(m)
            # kkkk["element_id"]=m.element_id
            nodes.append(kkkk)

        links.append({"source":

                          NID,
                      "target":
                            MID,
                      }
                        )


    p(len(nodes))
    p(len(links))

    def get_all_node_and_their_connections2(session):
        result = session.run('''
        MATCH (n)
    WHERE NOT EXISTS ((n)--())
    RETURN n


        ''')
        return list(result)

    k=session.execute_read(get_all_node_and_their_connections2)
    for i in k:
        n=i["n"]
        NID=dict(n)["user_generate_id_7577777777"]

        if NID not in nodesid:
            nodesid[NID]=1
            kkkk=dict(n)
            # kkkk["element_id"]=n.element_id
            nodes.append(kkkk)

    oooo={"nodes":nodes, "links":links}
    len(nodes)
    return oooo


# In[34]:


# get_all_node_and_their_connections13(session)


# In[ ]:


# Get all connections
def get_all_connections():
    p("get_all_connections called")
    result = session.run(""
                         "MATCH ()-[r]->() RETURN r"
                         ""
                         ""
                         ""
                         "")
    return list(result)
# r=get_all_connections()
# r1=r[0]
# r2=r1["r"]
# r2.nodes


# #### _get_constraints

# In[38]:


def _get_constraints(tx):
        p("_get_constraints called")
        query = "SHOW CONSTRAINTS"
        result = tx.run(query)
        return [record for record in result]
# k=session.execute_read(_get_constraints)


# ## Editing things.

# #### update_position_of_all_node_772

# In[ ]:


def update_position_of_all_node_772(session,d):

    p("update_position_of_all_node_772 called with data:", d)

    output_data = []

    for item in d:
        # Add a new dictionary to output_data with the flattened structure.
        output_data.append({
            "ID": item["ID"],
            "X": item["unreal_engine_location_728"]["X"],
            "Y": item["unreal_engine_location_728"]["Y"],
            "Z": item["unreal_engine_location_728"]["Z"]
        })


    def update_nodes(tx, data):
        query = """

        UNWIND $data AS item
        MATCH (n {user_generate_id_7577777777: item.ID})
        SET n.ue_location_X = item.X,
            n.ue_location_Y = item.Y,
            n.ue_location_Z = item.Z
        RETURN n.ID, n.ue_location_X, n.ue_location_Y, n.ue_location_Z

        """
        result = tx.run(query, data=data)
        return list(result)


    updated_nodes = session.execute_write(update_nodes, output_data)
    return updated_nodes

# d=[
#       {
#         "ID": "9b6097ab-f834-4789-a542-ced4f9478cc5",
#         "unreal_engine_location_728": {
#           "X": -1056.2984697348495,
#           "Y": -188.69419245425595,
#           "Z": 535.1348803507144
#         }
#       }
#     ]
# a=update_position_of_all_node_772(session,d)


# #### update_color_of_all_nodes
# 
# 

# In[2]:


def update_color_of_all_nodes(session, color):
    # Implement the logic to update the color of all nodes in the database
    query = '''
    MATCH (n)
    SET n.color = $color
    RETURN n
    '''
    result = session.run(query, color=color)
    return [record['n'] for record in result]


# In[ ]:


# a=update_color_of_all_nodes(session, "#FFFFFF")

# a


# ## Creating things.

# In[ ]:


def _create_constraint(tx, label, property):
    p("_create_constraint called with label:", label, "and property:", property)
    query = f"CREATE CONSTRAINT FOR  (n:{label}) REQUIRE  n.{property} IS UNIQUE"
    tx.run(query)
# session.execute_write(_create_constraint, "normalNode588888888", "user_generate_id_7577777777")



# In[ ]:


def create_node_tx(tx, name, id8):
    p("create_node_tx called with name:", name, "and id8:", id8)
    query = ("CREATE (n:normalNode588888888 {"
             "name: $name, "
             "user_generate_id_7577777777:$id8 }) "
             "RETURN n.user_generate_id_7577777777 AS node_id")
    result = tx.run(query, name=name, id8=id8)
    record = result.single()
    return record["node_id"]


# #### create_note_with_generate_id

# In[ ]:


def create_note_with_generate_id(session, name):
    p("create_note_with_generate_id called with name:", name)
    node_id = session.execute_write(create_node_tx, name, str(uuid.uuid4()))
    return node_id


# In[ ]:


def create_node_tx_with_position(tx, name, id8, x, y, z):
    p("create_node_tx_with_position called with name:", name, "id8:", id8, "x:", x, "y:", y, "z:", z)
    query = ("CREATE (n:normalNode588888888 {"
             "name: $name, "
             "user_generate_id_7577777777: $id8, "
             "ue_location_X: $x, "
             "ue_location_Y: $y, "
             "ue_location_Z: $z}) "
             "RETURN n.user_generate_id_7577777777 AS node_id")
    result = tx.run(query, name=name, id8=id8, x=x, y=y, z=z)
    record = result.single()
    return record["node_id"]


# #### create_note_with_provided_position_with_generate_id

# In[ ]:


def create_note_with_generate_id_and_position(session, name, x, y, z):
    p("create_note_with_generate_id_and_position called with name:", name, "x:", x, "y:", y, "z:", z)
    node_id = session.execute_write(create_node_tx_with_position, name, str(uuid.uuid4()), x, y, z)
    return node_id


# In[ ]:


already_exists_id="9b6097ab-f834-4789-a542-ced4f9478cc5"
def testing_constraint(session):
    p("testing_constraint called")
    node_id = session.execute_write(create_node_tx, "1", already_exists_id)
    return node_id
# k=testing_constraint(session)


# In[ ]:


# testing_name_777="to_be_deleted"


# In[ ]:


# node_id = create_note_with_generate_id(session, testing_name_777)
# 


# In[ ]:


# testing_id_777


# In[ ]:


# node_id


# In[ ]:


# delete_note_with_specific_id(session, node_id)


# In[29]:





# In[ ]:


def create_example_integrates(tx, name):
    p("create_example_integrates called with name:", name)
    def a1():

        # https://neo4j.com/docs/api/python-driver/current/api.html#neo4j.Session.execute_write
        def create_node_tx(tx, name):
            query = ("CREATE (n:NodeExample {"
                     "name: $name, "
                     "id: randomUUID()}) "
                     "RETURN n.id AS node_id")
            result = tx.run(query, name=name)
            record = result.single()
            return record["node_id"]
        node_id = session.execute_write(create_node_tx, "Bob")


    def a2():
        # https://neo4j.com/docs/api/python-driver/current/api.html#auto-commit-transactions
        def create_person(driver, name):
            # default_access_mode defaults to WRITE_ACCESS
            with driver.session(database="neo4j") as session:
                query = ("CREATE (n:NodeExample {name: $name, id: randomUUID()}) "
                         "RETURN n.id AS node_id")
                result = session.run(query, name=name)
                record = result.single()
                return record["node_id"]

    def a3():
        def create_and_return_node(tx, node):
            query = (
                "CREATE (n:Character "
                "{"
                "id: $id, "
                "group: $group, "
                "indexColor: $indexColor, "
                "bckgDimensions: $bckgDimensions, "
                "index: $index"
                "}"
                ")"
                "RETURN n"
            )
            result = tx.run(query,
                            id=node["id"],
                            group=node["group"],
                            indexColor=node["__indexColor"],
                            bckgDimensions=node["__bckgDimensions"],
                            index=node["index"])
            return result.single()[0]  # Return the created node


        node = {
            "id": "Cosette",
            "group": 5,
            "__indexColor": "#5003bc",
            "__bckgDimensions": [73.80274419464577, 24.2995279120152],
            "index": 26
        }

        node_id = session.execute_write(create_and_return_node, node)

    def a4():
        employee_threshold = 10


        def example():
            for i in range(100):
                name = f"Thor{i}"
                org_id = session.execute_write(employ_person_tx, name)
                print(f"User {name} added to organization {org_id}")


        def employ_person_tx(tx, name):
            # Create new Person node with given name, if not exists already
            result = tx.run("""
                MERGE (p:Person {name: $name})
                RETURN p.name AS name
                """, name=name
                            )

            # Obtain most recent organization ID and the number of people linked to it
            result = tx.run("""
                MATCH (o:Organization)
                RETURN o.id AS id, COUNT{(p:Person)-[r:WORKS_FOR]->(o)} AS employees_n
                ORDER BY o.created_date DESC
                LIMIT 1
            """)
            org = result.single()

            if org is not None and org["employees_n"] == 0:
                print("Most recent organization is empty.")

                raise Exception("Most recent organization is empty.")
                # Transaction will roll back -> not even Person is created!
            # If org does not have too many employees, add this Person to that
            if org is not None and org.get("employees_n") < employee_threshold:
                result = tx.run("""
                    MATCH (o:Organization {id: $org_id})
                    MATCH (p:Person {name: $name})
                    MERGE (p)-[r:WORKS_FOR]->(o)
                    RETURN $org_id AS id
                    """, org_id=org["id"], name=name
                                )
                print(f"Added {name} to existing organization {org['id']}")

            # Otherwise, create a new Organization and link Person to it
            else:
                result = tx.run("""
                    MATCH (p:Person {name: $name})
                    CREATE (o:Organization {id: randomuuid(), created_date: datetime()})
                    MERGE (p)-[r:WORKS_FOR]->(o)
                    RETURN o.id AS id
                    """, name=name
                                )
                print(f"Created new organization and added {name} to it")

            # Return the Organization ID to which the new Person ends up in
            return result.single()["id"]




# ## Removing things

# #### remove_all

# In[ ]:


def remove_all():
    p("remove_all called")
    session.run("MATCH (n) DETACH DELETE n")

# remove_all()


# #### delete_note_with_specific_id
# 

# In[ ]:


def delete_note_with_specific_id(tx, id):
    p("delete_note_with_specific_id called with id:", id)
    # Query that matches any node with the specific ID, deletes it, and counts the deleted nodes.
    query = f'''
    MATCH (n)
    WHERE n.user_generate_id_7577777777 = "{id}"
    DETACH DELETE n
    RETURN count(n) as deletedCount
    '''
    result = tx.run(query)
    return result.single()[0]  # returns the count of deleted nodes


# #### delete_note_with_specific_idand_label

# In[ ]:


def delete_note_with_specific_idand_label(tx, label, id):
    p("delete_note_with_specific_idand_label called with label:", label, "and id:", id)
    # Query that matches node with specific label and ID, deletes it, and counts deleted nodes.
    query = f'''
    MATCH (n:{label})
    WHERE n.user_generate_id_7577777777 = "{id}"
    DETACH DELETE n
    RETURN count(n) as deletedCount
    '''
    result = tx.run(query)
    return result.single()[0]  # returns the count of deleted nodes


# In[ ]:


# k=delete_note_with_specific_idand_label(session, "NodeExample", "9b6097ab-f834-4789-a542-ced4f9478cc5")


# In[ ]:


# k

