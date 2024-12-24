import binascii
import hashlib
import os
import ast
import re
import sys
import uuid
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from functools import wraps

from flask import Flask, g, request, send_from_directory, abort, request_started
from flask_cors import CORS
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import Api, swagger, Schema
from flask_json import FlaskJSON, json_response

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time

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

DATABASE_USERNAME = env('MOVIE_DATABASE_USERNAME')
DATABASE_PASSWORD = env('MOVIE_DATABASE_PASSWORD')
DATABASE_URL = env('MOVIE_DATABASE_URL')

driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD)))

app.config['SECRET_KEY'] = env('SECRET_KEY')


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


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {'message': 'no authorization provided'}, 401
        return f(*args, **kwargs)

    return wrapped


def hash_password(username, password):
    if sys.version[0] == 2:
        s = '{}:{}'.format(username, password)
    else:
        s = '{}:{}'.format(username, password).encode('utf-8')
    return hashlib.sha256(s).hexdigest()


def hash_avatar(username):
    if sys.version[0] == 2:
        s = username
    else:
        s = username.encode('utf-8')
    return hashlib.md5(s).hexdigest()


class ApiDocs(Resource):
    def get(self, path=None):
        if not path:
            path = 'index.html'
        return send_from_directory('swaggerui', path)



class return_all_nodes111(Resource):
    def get(self):
        db = get_db()
        session = db
        # get_all_node_and_their_connections
        def get_all_node_and_their_connections(session):
            result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
            return list(result)

        k = session.execute_read(get_all_node_and_their_connections)
        # len(k)
        k2 = k[0]
        k2.keys()
        nodes = []
        nodesid = {}
        links = []
        for i in k:
            n = i["n"]
            m = i["m"]

            NID = dict(n)["user_generate_id_7577777777"]
            Ninternal_id = n.element_id
            MID = dict(m)["user_generate_id_7577777777"]
            Minternal_id = m.element_id
            if NID not in nodesid:
                nodesid[NID] = 1
                kkkk = dict(n)
                # kkkk["element_id"]=n.element_id
                nodes.append(kkkk)
            if MID not in nodesid:
                nodesid[MID] = 1
                kkkk = dict(m)
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

        k = session.execute_read(get_all_node_and_their_connections2)
        for i in k:
            n = i["n"]
            NID = dict(n)["user_generate_id_7577777777"]

            if NID not in nodesid:
                nodesid[NID] = 1
                kkkk = dict(n)
                # kkkk["element_id"]=n.element_id
                nodes.append(kkkk)

        oooo = {"nodes": nodes, "links": links}
        len(nodes)
        p("hiiiiiiiiii")
        return oooo




class update_position_of_all_nodes111(Resource):
    @swagger.doc({
        'tags': ['users'],
        'summary': 'Login',
        'description': 'Login',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {
                            'type': 'string',
                        },
                        'password': {
                            'type': 'string',
                        }
                    }
                }
            },
        ],
        'responses': {
            '200': {
                'description': 'succesful login'
            },
            '400': {
                'description': 'invalid credentials'
            }
        }
    })


    def post(self):
        data = request.get_json()

        # p(data)
        db = get_db()
        from .kkkkkk import update_position_of_all_node_772

        ppppp=update_position_of_all_node_772(db, data)
        p(len(ppppp))
        # Writing JSON data
        # import json
        # with open('data1111111111.json', 'w') as file:
        #     json.dump(data, file)
        #
        # Return correct code

        return {'message': 'success!!!!!!!!!!!!!!!!!!!!!!!!!'}, 200


class create_no77777777(Resource):
    @swagger.doc({
        'tags': ['users'],
        'summary': 'Login',
        'description': 'Login',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {
                            'type': 'string',
                        },
                        'password': {
                            'type': 'string',
                        }
                    }
                }
            },
        ],
        'responses': {
            '200': {
                'description': 'succesful login'
            },
            '400': {
                'description': 'invalid credentials'
            }
        }
    })

    def post(self):
        data = request.get_json()

        p('create_no77777777')
        p(data)
        n=data['name']
        db = get_db()
        from .kkkkkk import create_note_with_generate_id

        ppppp=create_note_with_generate_id(db, n)

        return {'message': 'success!!!!!!!!!!!!!!!!!!!!!!!!!',

                'id': ppppp['id']

                }, 200



api.add_resource(ApiDocs, '/docs', '/docs/<path:path>')

api.add_resource(return_all_nodes111, '/api/v0/return_all_nodes111')

# api.add_resource(Register, '/api/v0/register')
# api.add_resource(Login, '/api/v0/login')
# 111111111111111111111111111111111111111
api.add_resource(update_position_of_all_nodes111, '/api/v0/update_position_of_all_nodes111')

api.add_resource(create_no77777777, '/api/v0/create_node77777777')


# 1/0
# api.add_resource(UserMe, '/api/v0/users/me')





# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8000, debug=True)
