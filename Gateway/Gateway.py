import requests
import flask
from flask import request, jsonify
from Services.CRUSH import CRUSH
from ZooKeeper import ZooKeeper
from Database.Database import Database
from Services.Quorum import Quorum

app = flask.Flask(__name__)
app.config["DEBUG"] = True

db = Database()
crush = CRUSH(3,5)
zk = ZooKeeper()
quorum = Quorum()

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
        TEMPLATE['PRODUCT_NAME'] = ' '.join(query[2:]).upper()
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
                return 'FAIL'
        else:
            url = url + 'createcart'
            req = requests.post(url, data=data)
            if req.status_code == 200:
                return req.json()
            else:
                return 'FAIL'

    elif COMMAND == 'DELETE':
        url = url + 'deletefromcart'
        req = requests.post(url, data=data)
        if req.status_code == 200:
            return req.json()
        else:
            return 'FAIL'
    
    elif COMMAND == 'LIST':
        url = url + 'listcart'
        req = requests.post(url, data=data)
        if req.status_code == 200:
            return req.json()
        else:
            return 'FAIL'
    
    elif COMMAND == 'UPDATE':
        url = url + 'updatecart'
        req = requests.post(url, data=data)
        if req.status_code == 200:
            return req.json()
        else:
            return 'FAIL'
    
    elif COMMAND == 'HANDOFF':
        url = url + 'handoff'
        req = requests.post(url, data=data)
        if req.status_code == 200:
            return 'SUCCESS'
        else:
            return 'FAIL'
    else:
        return 'FAIL'

def checkVersions(nodeResults, cart_id):
    versionMap = []
    nodes = list(nodeResults.keys())
    for node in nodes:
        versionMap.append(int(nodeResults[node]['METADATA']['VERSION']))
    currentVersion = max(versionMap)
    resultIndex = versionMap.index(currentVersion)
    result = nodeResults[nodes[resultIndex]]
    for index, version in enumerate(versionMap):
        if version != currentVersion:
            quorum.implementQuorum(nodes[resultIndex], nodes[index], cart_id)

    return result

def queryNodes(cart_id):
    data = {'UID': cart_id}
    nodelist = zk.getReplica(cart_id)
    queryResults = {}
    for node in nodelist:
        node_ip = zk.getNodeIP(node)
        res = executeQuery('LIST', node_ip, data)
        queryResults[node] = res
    failCount = 0
    for node in queryResults:
        if queryResults[node] == 'FAIL':
            failCount += 1
    if failCount > 1:
        return 'FAILURE: Quorum not Satisfied'
    result = checkVersions(queryResults, cart_id)
    return result
    
def updateNodes(command, cart_id, data):
    nodelist = zk.getReplica(cart_id)
    queryResults = {}
    result = {}
    for node in nodelist:
        node_ip = zk.getNodeIP(node)
        res = executeQuery(command, node_ip, data)
        queryResults[node] = res

    failCount = 0
    for node in queryResults:
        if queryResults[node] == 'FAIL':
            instruction = {
                'COMMAND': command,
                'DATA': data
            }
            handoff_ip = zk.getHandoffNodeIP(node)
            state = executeQuery('HANDOFF', handoff_ip, data= instruction)
            if state == 'SUCCESS':
                continue
            else:
                failCount+=1
            # Implemented hinted handoff
        else:
            result = queryResults[node]
    if failCount > 1:
        return 'FAILURE'
    else:
        return result
    
def createNode(username, cart_id, data):
    zk.createCart(cart_id)
    nodes = zk.getNodes()
    nodes.sort()
    nodeindex = crush.select(username)
    failCount = 0
    replica = 1
    for index in nodeindex:
        failCount = 0
        replica = 1
        node_ip = zk.getNodeIP(nodes[index])
        state = executeQuery('ADD', node_ip, data=data, create=True)
        curr = nodes[index]
        while(state == 'FAIL'):
            failCount += 1
            reindex = crush.select(username, reselect=True, data={'replication_number': replica, 'fail_count': failCount})
            curr = nodes[reindex]
            node_ip = zk.getNodeIP(nodes[reindex])
            state = executeQuery('ADD', node_ip, data=data, create=True)
        zk.setReplica(cart_id, curr)
        replica += 1
    return state



def processAdminQuery(FILTERS = None, HAS_FILTER = False):
    result = {}
    if HAS_FILTER:
        if FILTERS[0].split(':')[0].upper() != 'USER':
            cartlists = []
            for f in FILTERS:
                cartlists.extend(zk.getSecondaryList(f.upper()))
            cartlists = list(set(cartlists))
            for cart_id in cartlists:
                result[cart_id] = queryNodes(cart_id)
            return result
        else:
            username = FILTERS[0].split(':')[1].strip().upper()
            uid = db.getUID(username)
            result = queryNodes(uid)
            return result
    else:
        cartlists = zk.getCarts()
        for cart_id in cartlists:
            result[cart_id] = queryNodes(cart_id)
        return result

def generateFilters(productdetails):
    typeFilter = 'TYPE:' + productdetails['TYPE'].upper()
    categoryFilter = 'CATEGORY:' + productdetails['CATEGORY'].upper()
    return [typeFilter, categoryFilter]

def generateData(productDetails, uid):
    data = {}
    data['UID'] = uid
    data['PRODUCT_ID'] = productDetails['PRODUCT_ID']
    data['PRODUCT_NAME'] = productDetails['PRODUCT_NAME']
    data['ATRRIB_ID'] = 'abcdefgh'
    return data



def processUserQuery(username, command, productName):
    uid = db.getUID(username)
    if uid != 'NOT A USER':
        if zk.exists(uid):
            if command == 'LIST':
                result = queryNodes(uid)
                return result
            productDetails = db.getProductDetails(productName)
            filters = generateFilters(productDetails)
            data = generateData(productDetails, uid)
            result = updateNodes(command, uid, data)
            if result != 'FAILURE':
                for f in filters:
                    if command != 'DELETE':
                        zk.updateSecondaryIndex(f, uid)
                    else:
                        zk.updateSecondaryIndex(f, uid, delete=True)
            return result
        else:
            productDetails = db.getProductDetails(productName)
            filters = generateFilters(productDetails)
            data = generateData(productDetails, uid)
            result = createNode(username, uid, data)
            if result != 'FAIL':
                for f in filters:
                    zk.updateSecondaryIndex(f, uid)
            return result
    else:
        return 'NOT A USER'



@app.route('/cdfs.gateway', methods=['GET', 'POST'])
def manage():
    queryParams = request.args
    query = queryParams.get('query')
    parsedQuery = parseQuery(query)
    if parsedQuery['TYPE'] == 'ADMIN':
        if parsedQuery['HAS_FILTER']:
            result = processAdminQuery(parsedQuery['FILTERS'], HAS_FILTER=True)
        else:
            result = processAdminQuery()
    else:
        result = processUserQuery(parsedQuery['USERNAME'], parsedQuery['COMMAND'], parsedQuery['PRODUCT_NAME'])
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0')


