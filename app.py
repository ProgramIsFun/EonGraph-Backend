import hashlib
import os
import ast
import re
import sys
import uuid
from dotenv import load_dotenv, find_dotenv

from functools import wraps

from flask import Flask, g, request, send_from_directory, abort, request_started
from flask_cors import CORS
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import Api, swagger, Schema
from flask_json import FlaskJSON, json_response
from neo4j import GraphDatabase, basic_auth


from kkkkkk import get_all_node_and_their_connections13
from kkkkkk import update_position_of_all_node_772

from kkkkkk import create_note_with_generate_id_and_position
# from kkkkkk import delete_node


def p(*args):
    print(args)

load_dotenv(find_dotenv())

app = Flask(__name__)

CORS(app)
FlaskJSON(app)

api = Api(app, title='Neo4j Movie Demo API', api_version='0.0.10')


@api.representation('application/json')
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)


def env(key, default=None, required=True):
    """
    Retrieves environment variables and returns Python natives. The (optional)
    default will be returned if the environment variable does not exist.
    """
    try:
        value = os.environ[key]
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
    except KeyError:
        if default or not required:
            return default
        raise RuntimeError("Missing required environment variable '%s'" % key)


NEO4J_URI='neo4j+ssc://806970c7.databases.neo4j.io'
NEO4J_USERNAME='neo4j'
NEO4J_PASSWORD="ntVYbR1v-6OrHleeKhs7WC22VRXmpM7fPbhNddc3QRw"
NEO4J_DATABASE="neo4j"





SECRET_KEY="super secret guy"
MOVIE_DATABASE_USERNAME= NEO4J_USERNAME
MOVIE_DATABASE_PASSWORD= NEO4J_PASSWORD
MOVIE_DATABASE_URL= NEO4J_URI


DATABASE_USERNAME = MOVIE_DATABASE_USERNAME
DATABASE_PASSWORD = MOVIE_DATABASE_PASSWORD
DATABASE_URL = MOVIE_DATABASE_URL
app.config['SECRET_KEY'] = SECRET_KEY







driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD)))


def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()


def set_user(sender, **extra):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        g.user = {'id': None}
        return
    match = re.match(r'^Token (\S+)', auth_header)
    if not match:
        abort(401, 'invalid authorization format. Follow `Token <token>`')
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


request_started.connect(set_user, app)



class ApiDocs(Resource):
    def get(self, path=None):
        if not path:
            path = 'index.html'
        return send_from_directory('swaggerui', path)



class get_all_node_and_their_connections(Resource):
    def get(self):

        try:
            p("get_all_node_and_their_connections")
            db = get_db()
            
            # p(db)
            session = db
            p("return_all_nodes1112222222222222222222222222222222222222222222222222222222222222")
            oooo=get_all_node_and_their_connections13(session)
            return oooo
        except Exception as e:
            p('Error111111111111111111111111111:', e)
            return {'message': 'Error occurred', 'error': str(e)}, 500




class update_position_of_all_nodes(Resource):

    def post(self):
        data = request.get_json()

        # p(data)
        db = get_db()
     
        ppppp=update_position_of_all_node_772(db, data)
        p(len(ppppp))
        # Writing JSON data
        save= 0
        if save:
            import json
            with open('data1111111111.json', 'w') as file:
                json.dump(data, file)

        # Return correct code

        return {'message': 'success!!!!!!!!!!!!!!!!!!!!!!!!!'}, 200


file_path = 'example.txt'


class create_node(Resource):

    def post(self):
        data = request.get_json()

        p('create_no77777777')
        p(data)
        n=data['name']
        db = get_db()

        # ue_location_X
        x=data['locationX']
        y=data['locationY']
        z=data['locationZ']
        if 1:

            
            ppppp1=create_note_with_generate_id_and_position(db, n, x, y, z)

            # Open the file in append mode and write the string
            with open(file_path, 'a') as file:
                file.write(ppppp1)

            ppppp={
                "id": ppppp1,
                "name": n

            }
        else:
            ppppp1=str(uuid.uuid4())
            ppppp={
                "id": ppppp1,
                "name": n
            }

        return {'message': 'qqqqqqqqqqqqqq',
            'messag111e': 'success!!!!!!!!!!!!!!!!!!!!!!!!!',
                'id': ppppp['id'],
                'name': ppppp['name']
                }, 200


class delete_node(Resource):

    def post(self):
        data = request.get_json()

        p('delete_node')
        p(data)
        n=data['id']
        db = get_db()

        # ppppp=delete_node(db, n)

        return {'message': 'success!!!!!!!!!!!!!!!!!!!!!!!!!',

                # 'id': ppppp['id']

                }, 200



class health(Resource):
    def get(self):
        return {'message': 'success!!!!!!!!!!!!!!!!!!!!!!!!!',

                }, 200



# basic 
api.add_resource(health, '/health')
api.add_resource(ApiDocs, '/docs', '/docs/<path:path>')

# update
api.add_resource(update_position_of_all_nodes, '/api/v0/update_position_of_all_nodes111')
api.add_resource(create_node, '/api/v0/create_node77777777')
api.add_resource(delete_node, '/api/v0/delete_node')

# read
api.add_resource(get_all_node_and_their_connections, '/api/v0/return_all_nodes111')


from flask import render_template

@app.route('/original')
def index():
   print('Request for index page received')
   return render_template('index.html')


if __name__ == '__main__':
   app.run()
