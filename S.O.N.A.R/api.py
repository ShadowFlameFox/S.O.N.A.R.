from flask import Flask, jsonify
import index
import configparser
from termcolor import colored

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

app = Flask(__name__)

@app.route('/create/<database_name>')
def create_route(database_name):
    message, content ,status_code = index.create_database(database_name)
    return jsonify({'message': message, 'value':content, 'status_code': status_code}), status_code

@app.route('/store/<database_name>/<key>/<value>')
def store_route(database_name, key, value):
    message, content, status_code = index.store(database_name, key, value)
    return jsonify({'message': message, 'value':content, 'status_code': status_code}), status_code

@app.route('/get/<database_name>/<key>')
def load_route(database_name, key):
    message, content, status_code = index.load(database_name, key)
    return jsonify({'message': message, 'value':content, 'status_code': status_code}), status_code

@app.route('/list')
def list_route():
    message, content, status_code = index.list_subfolders()
    return jsonify({'message': message, 'value':content, 'status_code': status_code}), status_code

@app.route('/delete_key/<database_name>/<key>')
def delete_key_route(database_name, key):
    message, content, status_code = index.delete_key(database_name, key)
    return jsonify({'message': message, 'value':content, 'status_code': status_code}), status_code

@app.route('/delete_database/<database_name>')
def delete_database_route(database_name):
    message, content, status_code = index.delete_database(database_name)
    return jsonify({'message': message, 'value':content, 'status_code': status_code}), status_code

@app.route('/temp_key/<database_name>/<key>/<value>/<expiry_date>')
def temp_key(database_name, key, value, expiry_date):
    message, content, status_code = index.gen_temp_key(database_name,key,value,expiry_date)
    return jsonify({'message': message, 'value':content, 'status_code': status_code}), status_code

if __name__ == '__main__':
    config_file_path = 'sonar.conf'
    config = read_config(config_file_path)

    host = config.get('API', 'host')
    port = config.getint('API', 'port')
    version = config.get("GENERAL", "version")
    if version != "0.0.1":
        print(colored("This API version is deprecated. Some features may not be supported.", "yellow"))

    app.run(debug=True, port=port, host=host)
