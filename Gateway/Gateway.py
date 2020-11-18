import requests
import flask
from flask import request, jsonify
from Services.CRUSH import CRUSH
from ZooKeeper import ZooKeeper
from Database.Database import Database

app = flask.Flask(__name__)
app.config["DEBUG"] = True

db = Database()
crush = CRUSH
zk = ZooKeeper()



@app.route('/cdfs.gateway', methods=['GET', 'POST'])
def manage():
    queryParams = request.args
    query = queryParams.get('query')
