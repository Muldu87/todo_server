from flask import Flask, jsonify, make_response
import requests
import os
import mysql.connector
import simplejson as json

app = Flask(__name__)

my_db = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="Martin21",
  database="python_schema"
)


database_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print(database_path)


def index(username):
    cur = my_db.cursor()
    query = "SELECT name as 'name', JSON_ARRAYAGG(todo.todotype) AS 'todo' FROM users inner join todo on userlink = users.id GROUP BY name;"
    # query = "select * from users where name_index = '{}';".format(username)
    cur.execute(query)
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    # for result in rv2:

    return json.dumps(json_data)


def index_list(username):
    return ''


with open("{}/database/users.json".format(database_path), "r") as f:
    usr = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return "Welcome to my little microservice"


@app.route('/users', methods=['GET'])
def users():
    ''' Returns the list of users '''

    resp = make_response(json.dumps(usr, sort_keys=True, indent=4))
    resp.headers['Content-Type']="application/json"
    return resp


@app.route('/users/<username>', methods=['GET'])
def user_data(username):
    ''' Returns info about a specific user '''
    # return jsonify(usr[username])
    return index(username)


@app.route('/users/<username>/lists', methods=['GET'])
def user_lists(username):
    ''' Get lists based on username '''



    try:
        req = requests.get("http://127.0.0.1:5001/lists/{}".format(username))
    except requests.exceptions.ConnectionError:
        return "Service unavailable"
    return req.text


if __name__ == '__main__':
    app.run(port=5000, debug=True)
