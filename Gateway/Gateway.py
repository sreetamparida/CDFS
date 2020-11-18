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

def parseQuery(query):
    query = query.strip().split()
    TEMPLATE = {}
    if query[0].lower() == 'admin':
        TEMPLATE['TYPE'] = 'ADMIN'
        TEMPLATE['COMMAND'] = 'LIST'
        TEMPLATE['HAS_FILTER'] = False
        if len(query) > 2:
            TEMPLATE['HAS_FILTER'] = True
            TEMPLATE['FILTERS'] = query[2:]
        return TEMPLATE
    else:
        TEMPLATE['TYPE'] = 'USER'
        TEMPLATE['COMMAND'] = query[1].upper()
        TEMPLATE['USERNAME'] = query[0].upper()
        TEMPLATE['PRODUCT_NAME'] = query[2].upper()
        return TEMPLATE

def executeQuery(COMMAND, ip, data=None, create=False):
    url = 'http://{ip}:5000/'.format(ip=ip)

    if COMMAND == 'ADD':
        if not create:
            url = url + 'addtocart'
            req = requests.post(url, data=data)
            if req.status_code == 200:
                return req.json()
            else:
                return "FAIL"
        else:
            url = url + 'createcart'
            req = requests.post(url, data=data)
            if req.status_code == 200:
                return req.json()
            else:
                return "FAIL"

    elif COMMAND == 'DELETE':
        url = url + 'deletefromcart'
        req = requests.post(url, data=data)
        if req.status_code == 200:
            return req.json()
        else:
            return "FAIL"
    
    elif COMMAND == 'LIST':
        url = url + 'listcart'
        req = requests.post(url, data=data)
        if req.status_code == 200:
            return req.json()
        else:
            return "FAIL"
    
    elif COMMAND == 'UPDATE':
        url = url + 'updatecart'
        req = requests.post(url, data=data)
        if req.status_code == 200:
            return req.json()
        else:
            return "FAIL"
    else:
        return 'FAIL'
def checkVersions(temp):
    return temp

def queryNodes(cart_id, command, data, create=False):
    nodelist = zk.getReplica(cart_id)
    queryResults = {}
    for node in nodelist:
        node_ip = zk.getNodeIP(node)
        res = executeQuery(command, node_ip, data, create=create)
        queryResults[node] = res
    result = checkVersions(queryResults)
    return result
    



def processAdminQuery(FILTERS, HAS_FILTER = True):
    if HAS_FILTER:
        if FILTERS[0].split(':')[0].upper() != 'USER':
            cartlists = []
            for f in FILTERS:
                cartlists.extend(zk.getSecondaryList(f.upper()))
            cartlists = list(set(cartlists))
            


def processUserQuery():
    pass


@app.route('/cdfs.gateway', methods=['GET', 'POST'])
def manage():
    queryParams = request.args
    query = queryParams.get('query')
    parsedQuery = parseQuery(query)


