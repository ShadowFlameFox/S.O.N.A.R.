from flask import Flask, jsonify
import index

app = Flask(__name__)

@app.route('/create/<database_name>')
def create_route(database_name):
    result_message = index.create_database(database_name)
    return jsonify({'result': result_message})

@app.route('/store/<database_name>/<key>/<value>')
def store_route(database_name, key, value):
    result_message = index.store(database_name, key, value)
    return jsonify({'result': result_message})

@app.route('/get/<database_name>/<key>')
def load_route(database_name, key):
    result_message = index.load(database_name, key)
    return jsonify({'result': result_message})

@app.route('/list')
def list_route():
    result_message = index.list_subfolders()
    return jsonify({'result': result_message})

@app.route('/delete_key/<database_name>/<key>')
def delete_key_route(database_name, key):
    result_message = index.delete_key(database_name, key)
    return jsonify({'result': result_message})

if __name__ == '__main__':
    app.run(debug=True)
