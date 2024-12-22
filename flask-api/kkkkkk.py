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