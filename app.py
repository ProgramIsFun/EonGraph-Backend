import os
import ast
import re
from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, request, send_from_directory, abort, render_template, jsonify
from flask_cors import CORS
from flask_json import FlaskJSON, json_response
from neo4j import GraphDatabase, basic_auth

from kkkkkk import get_all_node_and_their_connections13
from kkkkkk import update_position_of_all_node_772
from kkkkkk import create_note_with_generate_id_and_position
from example import get_specific_node_with_specific_id

def p(*args):
    print(args)

load_dotenv(find_dotenv())

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
FlaskJSON(app)

# --- ENVIRONMENT & CONFIG ---

def env(key, default=None, required=True):
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError(f"Missing required environment variable '{key}'")

app.config['SECRET_KEY'] = "super secret guy"
NEO4J_URI = 'neo4j+ssc://806970c7.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = "ntVYbR1v-6OrHleeKhs7WC22VRXmpM7fPbhNddc3QRw"
NEO4J_DATABASE = "neo4j"

# --- NEO4J SETUP ---

driver = GraphDatabase.driver(
    NEO4J_URI, auth=basic_auth(NEO4J_USERNAME, str(NEO4J_PASSWORD))
)

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()

# --- AUTH DECORATOR ---

@app.before_request
def set_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        g.user = {'id': None}
        return
    match = re.match(r'^Token (\S+)', auth_header)
    if not match:
        abort(401, 'invalid authorization format. Use `Token <token>`')
        return
    token = match.group(1)

    def get_user_by_token(tx, token):
        return tx.run(
            '''
            MATCH (user:User {api_key: $api_key}) RETURN user
            ''', {'api_key': token}
        ).single()
    db = get_db()
    result = db.read_transaction(get_user_by_token, token)
    try:
        g.user = result['user']
    except (KeyError, TypeError):
        abort(401, 'invalid authorization key')
    return

# --- API ENDPOINTS ---




@app.route('/health', methods=['GET'])
def health():
    return {"message": "ok, no problem"}, 200

@app.route('/docs/<path:path>', methods=['GET'])
@app.route('/docs', methods=['GET'])
def api_docs(path=None):
    if not path:
        path = 'index.html'
    return send_from_directory('swaggerui', path)


# read

@app.route('/api/v0/get_specific_node_with_specific_id', methods=['POST', 'OPTIONS'])
def api_get_specific_node():
    if request.method == 'OPTIONS':
        return {}, 200
    data = request.get_json()
    p('get_specific_node_with_specific_id', data)
    node_id = data['nodeIdAccess']
    oooo = get_specific_node_with_specific_id(node_id)
    p("oooo111", oooo)
    if not oooo:
        return {'message': 'Node not found'}, 404
    return {'node': oooo}, 200

@app.route('/api/v0/return_all_nodes111', methods=['GET'])
def api_get_all_nodes():
    try:
        p("get_all_node_and_their_connections")
        db = get_db()
        oooo = get_all_node_and_their_connections13(db)
        return jsonify(oooo)
    except Exception as e:
        p('Error occurred while fetching nodes and connections:', str(e))
        return {'message': 'Error occurred', 'error': str(e)}, 500

# create 

@app.route('/api/v0/create_node77777777', methods=['POST'])
def api_create_node():
    data = request.get_json()
    p('create_no77777777', data)
    n = data['name']
    db = get_db()
    x = data['locationX']
    y = data['locationY']
    z = data['locationZ']
    ppppp1 = create_note_with_generate_id_and_position(db, n, x, y, z)
    ppppp = {
        "id": ppppp1,
        "name": n
    }
    return {'message': 'qqqqqqqqqqqqqq',
            'messag111e': 'success!',
            'id': ppppp['id'],
            'name': ppppp['name']
            }, 200

# update
@app.route('/api/v0/update_position_of_all_nodes111', methods=['POST'])
def api_update_positions():
    data = request.get_json()
    db = get_db()
    ppppp = update_position_of_all_node_772(db, data)
    p(len(ppppp))
    # Save JSON data if needed...
    return {'message': 'success!'}, 200

# delete

@app.route('/api/v0/delete_node', methods=['POST'])
def api_delete_node():
    data = request.get_json()
    p('delete_node', data)
    n = data['id']
    db = get_db()
    # ppppp=delete_node(db, n)
    return {'message': 'ok, no problem'}, 200

@app.route('/original')
def index():
    print('Request for index page received')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()