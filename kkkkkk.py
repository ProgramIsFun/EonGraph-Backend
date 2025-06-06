import uuid

p=print

def update_position_of_all_node_772(session,d):



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
    #
    # for i in updated_nodes:
    #     p(i)

def get_all_node_and_their_connections13(session):
    # get_all_node_and_their_connections
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




def create_node_tx(tx, name, id8):
    query = ("CREATE (n:normalNode588888888 {"
             "name: $name, "
             "user_generate_id_7577777777:$id8 }) "
             "RETURN n.user_generate_id_7577777777 AS node_id")
    result = tx.run(query, name=name, id8=id8)
    record = result.single()
    return record["node_id"]

def create_note_with_generate_id(session, name):
    node_id = session.execute_write(create_node_tx, name, str(uuid.uuid4()))
    return node_id


def create_node_tx_with_position(tx, name, id8, x, y, z):
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

def create_note_with_generate_id_and_position(session, name, x, y, z):
    node_id = session.execute_write(create_node_tx_with_position, name, str(uuid.uuid4()), x, y, z)
    return node_id


