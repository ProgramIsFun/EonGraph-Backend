import logging
import os

from flask import Flask, g, request, render_template, jsonify
from flask_cors import CORS
from flask_json import FlaskJSON
from neo4j import GraphDatabase, basic_auth
from db_operations import get_all_nodes__and__their_connections
from db_operations import update_position_of_all_node
from db_operations import create_node_with_generate_id_and_position
from db_operations import get_specific_node_with_specific_id, update_color_of_all_nodes
from db_operations import get_github_repositories, clear_all_caches, run_cypher_any
from db_operations import delete_node_with_specific_id
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NODE_ID_ACCESSOR
from flasgger import Swagger, swag_from

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logger.info("Neo4j driver creating...")
driver = GraphDatabase.driver(
    NEO4J_URI, auth=basic_auth(NEO4J_USERNAME, str(NEO4J_PASSWORD))
)
logger.info("Neo4j driver created.")


logger.info("Checking if node_id_accessor exists on all nodes...")
with driver.session() as session:
    result = session.run(
        f"MATCH (n) WHERE n.{NODE_ID_ACCESSOR} IS NULL RETURN count(n) AS count"
    )
    count = result.single().get("count", 0)
    if count > 0:
        logger.error("There are %d nodes without the '%s' property.", count, NODE_ID_ACCESSOR)
        exit(1)
    else:
        logger.info("All nodes have the '%s' property.", NODE_ID_ACCESSOR)



logger.info("Flask app creating...")
app = Flask(__name__)
logger.info("Flask app created.")

logger.info("Enabling CORS...")
CORS(app)

logger.info("Initializing FlaskJSON...")
FlaskJSON(app)

# Initialize Flasgger with your Flask app
swagger = Swagger(app)


# Place error handler function here 
@app.errorhandler(Exception)
def handle_exception(e):
    # You can also log the error here
    response = {
        "success": False,
        "error": str(e)
    }
    logger.error("Returning error response: %s", response)
    return jsonify(response), 500

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
if not app.config['SECRET_KEY']:
    raise RuntimeError("SECRET_KEY environment variable is not set. Refusing to start with an insecure default.")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
if not ADMIN_TOKEN:
    logger.warning("ADMIN_TOKEN is not set. The /api/v0/run_any_cypher endpoint will be inaccessible.")

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()

# --- API ENDPOINTS ---

# general

@app.route('/health', methods=['GET'])
@swag_from({
    'tags': ["health"],
    'responses': {
        200: {
            'description': 'Health check',
            'examples': {
                "application/json": {"message": "ok, no problem, version 1.0.0"}
            }
        }
    }
})
def health():
    return {"message": "ok, no problem, version 1.0.0"}, 200

@app.route('/sampleHtml', methods=['GET'])
@swag_from({
    'tags': ["general"],
    'responses': {
        200: {
            'description': 'Serve original index.html',
            'examples': {
                "text/html": "<!DOCTYPE html>..."
            }
        }
    }
})
def index():
    print('Request for index page received')
    return render_template('index.html')


# run any cypher
@app.route('/api/v0/run_any_cypher', methods=['POST'])
@swag_from({
    'tags': ["cypher"],
    'parameters': [
        {
            'name': 'X-Admin-Token',
            'in': 'header',
            'required': True,
            'type': 'string',
            'description': 'Admin authentication token'
        },
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'string',
                        'example': 'MATCH (n) RETURN n LIMIT 5'
                    }
                },
                'required': ['data']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Cypher query executed successfully',
            'examples': {
                "application/json": {"results": []}
            }
        },
        401: {
            'description': 'Unauthorized',
            'examples': {
                "application/json": {"message": "Unauthorized"}
            }
        },
        400: {
            'description': 'Bad Request',
            'examples': {
                "application/json": {"message": "No data provided"}
            }
        }
    }
})
def api_run_any_cypher():
    token = request.headers.get('X-Admin-Token')
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        return {'message': 'Unauthorized'}, 401
    db = get_db()
    data = request.get_json()
    logger.info('run_any_cypher %s', data)
    if not data or 'data' not in data:
        return {'message': 'No data provided'}, 400
    cypher_query = data['data']
    if cypher_query.strip() == "":
        return {'message': 'Empty cypher query'}, 400
    result = run_cypher_any(db, cypher_query)
    return jsonify(result), 200


# read

# using post because we might have sensitive data to send along in the future
@app.route('/api/v0/get_specific_node_with_specific_id', methods=['POST'])
@swag_from({
    'tags': ["nodes"],
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nodeIdAccess': {
                        'type': 'string',
                        'example': '{the id value}'
                    }
                },
                'required': ['nodeIdAccess']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Node retrieved successfully',
            'examples': {   
                "application/json": {"node": "node object"}
            }
        },
        400: {
            'description': 'Bad Request',
            'examples': {
                "application/json": {"message": "No data provided"}
            }
        },
        404: {
            'description': 'Node not found',
            'examples': {
                "application/json": {"message": "Node not found"}
            }
        }
    }
})
def api_get_specific_node():
    data = request.get_json()
    if not data or 'nodeIdAccess' not in data:
        return {'message': 'Missing required field: nodeIdAccess'}, 400
    logger.info('get_specific_node_with_specific_id %s', data)
    node_id = data['nodeIdAccess']
    db = get_db()
    nodeObject = get_specific_node_with_specific_id(db, node_id)
    if not nodeObject:
        return {'message': 'Node not found'}, 404
    return jsonify({'node': nodeObject}), 200

@app.route('/api/v0/return_all_nodes_and_their_connections_if_any', methods=['GET'])
@swag_from({
    'tags': ["nodes"],
    'responses': {
        200: {
            'description': 'All nodes and their connections retrieved successfully',
            'examples': {
                "application/json": {"nodes": [], "connections": []}
            }
        },
        500: {
            'description': 'Internal Server Error',
            'examples': {
                "application/json": {"message": "Error occurred", "error": "error details"}
            }
        }
    }
})
def api_get_all_nodes():
    try:
        logger.info("get_all_nodes_and_their_connections")
        db = get_db()
        nodes_and_connections = get_all_nodes__and__their_connections(db)
        return jsonify(nodes_and_connections)
    except Exception as e:
        logger.error('Error fetching nodes and connections: %s', e)
        return {'message': 'Error occurred', 'error': str(e)}, 500




# get the id property that exist on all the node
@app.route('/api/v0/get_nodeIdAccessor', methods=['GET'])
@swag_from({
    'tags': ["nodes"],
    'responses': {
        200: {
            'description': 'Node ID accessor retrieved successfully',
            'examples': {
                "application/json": {"id_ref": "example_id_value"}
            }
        }
    }
})
def api_get_all_node_ids():
    application_ids = NODE_ID_ACCESSOR
    return jsonify({"id_ref": application_ids}), 200


@app.route('/api/v0/get_all_github_repositories', methods=['GET'])
@swag_from({
    'tags': ["github"],
    'responses': {
        200: {
            'description': 'GitHub repositories retrieved successfully',
            'examples': {
                "application/json": {"repositories": []}
            }
        },
        500: {
            'description': 'Internal Server Error',
            'examples': {
                "application/json": {"message": "Error occurred", "error": "error details"}
            }
        }
    }
})
def api_get_all_github_repositories():
    repos=get_github_repositories()
    return jsonify(repos), 200

# create 
@app.route('/api/v0/create_node', methods=['POST'])
@swag_from({
    'tags': ["nodes"],
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'example': 'Node Name'
                    },
                    'locationX': {
                        'type': 'number',
                        'example': 0.0
                    },
                    'locationY': {
                        'type': 'number',
                        'example': 0.0
                    },
                    'locationZ': {
                        'type': 'number',
                        'example': 0.0
                    }
                },
                'required': ['name', 'locationX', 'locationY', 'locationZ']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Node created successfully',
            'examples': {
                "application/json": {"message": "success.", "id": "node_id", "name": "Node Name"}
            }
        },
        400: {
            'description': 'Bad Request',
            'examples': {
                "application/json": {"message": "No data provided"}
            }
        }
    }
})
def api_create_node():
    data = request.get_json()
    if not data:
        return {'message': 'No data provided'}, 400
    for field in ('name', 'locationX', 'locationY', 'locationZ'):
        if field not in data:
            return {'message': f'Missing required field: {field}'}, 400
    logger.info('create_node %s', data)
    name = data['name']
    db = get_db()
    node_id = create_node_with_generate_id_and_position(
        db, name, data['locationX'], data['locationY'], data['locationZ']
    )
    return {'message': 'success.', 'id': node_id, 'name': name}, 200

# update
@app.route('/api/v0/update_color_of_all_nodes', methods=['POST'])
@swag_from({
    'tags': ["nodes"],
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'color': {
                        'type': 'string',
                        'example': '#FF5733'
                    }
                },
                'required': ['color']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Node colors updated successfully',
            'examples': {
                "application/json": {"message": "success."}
            }
        },
        400: {
            'description': 'Bad Request',
            'examples': {
                "application/json": {"message": "No data provided"}
            }
        }
    }
})
def api_update_colors():
    data = request.get_json()
    if not data or 'color' not in data:
        return {'message': 'Missing required field: color'}, 400
    db = get_db()
    updated_nodes = update_color_of_all_nodes(db, data['color'])
    logger.info('Updated color on %d nodes', len(updated_nodes))
    return {'message': 'success.'}, 200

@app.route('/api/v0/update_position_of_all_nodes', methods=['POST'])
@swag_from({
    'tags': ["nodes"],
    'description': 'This route is work in progress............',
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'ID': {
                        'type': 'string',
                        'example': 'node_id'
                    },
                    'X': {
                        'type': 'number',
                        'example': 1.0
                    },
                    'Y': {
                        'type': 'number',
                        'example': 2.0
                    },
                    'Z': {
                        'type': 'number',
                        'example': 3.0
                    }
                },
                'required': ['ID', 'X', 'Y', 'Z']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Node positions updated successfully',
            'examples': {
                "application/json": {"message": "success."}
            }
        },
        400: {
            'description': 'Bad Request',
            'examples': {
                "application/json": {"message": "No data provided"}
            }
        }
    }
})
def api_update_positions():
    data = request.get_json()
    if not data or 'data_points' not in data or 'prefix' not in data:
        return {'message': 'Missing required fields: data_points, prefix'}, 400

    data_points = data["data_points"]
    prefix = data["prefix"]
    logger.info("update_positions prefix=%s, points=%d", prefix, len(data_points))

    # only 'WebApp' is supported for now for prefix
    if prefix != "WebApp":
        return {'message': 'Only "WebApp" prefix is supported for now.'}, 400

    db = get_db()
    result = update_position_of_all_node(db, data_points, prefix)
    logger.info('Updated positions for %d nodes', len(result))
    return {'message': 'success.'}, 200

# delete
@app.route('/api/v0/delete_node', methods=['POST'])
@swag_from({
    'tags': ["nodes"],
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'string',
                        'example': 'node_id_to_delete'
                    }
                },
                'required': ['id']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Node deleted successfully',
            'examples': {
                "application/json": {"message": "ok, no problem"}
            }
        },
        400: {
            'description': 'Bad Request',
            'examples': {
                "application/json": {"message": "No data provided"}
            }
        }
    }
})
def api_delete_node():
    data = request.get_json()
    if not data or 'id' not in data:
        return {'message': 'Missing required field: id'}, 400
    logger.info('delete_node %s', data)
    n = data['id']
    db = get_db()
    deleted = db.execute_write(delete_node_with_specific_id, n)
    return {'message': f'Deleted {deleted} node(s).'}, 200
# clear_all_caches
@app.route('/api/v0/clear_all_caches', methods=['POST'])
@swag_from({
    'tags': ["general"],
    'responses': {
        200: {
            'description': 'Cache cleared successfully',
            'examples': {
                "application/json": {"message": "Cleared X cache files."}
            }
        }
    }
})
def api_clear_all_caches():
    deleted_count = clear_all_caches()
    return {'message': f'Cleared {deleted_count} cache files.'}, 200

if __name__ == '__main__':
    app.run()