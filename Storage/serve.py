from Services.Chronos import Chronos
from Services.Worker import Worker
import flask
import requests
from flask import request
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

value = {
    'ID': None,
    'PRODUCT_NAME': None
}
worker = Worker()


@app.route('/createcart', methods=['GET', 'POST'])
def createCart():
    if request.method == 'POST':
        UID = request.form['UID']
        ATTRIB_ID = request.form['ATRRIB_ID']

        value['ID'] = request.form['PRODUCT_ID']
        value['PRODUCT_NAME'] = request.form['PRODUCT_NAME']

        worker.createCart(UID)
        worker.addToCart(UID, value)
        worker.updateMetadata(UID, 1, time.time())
        worker.updateSecondaryIndex(UID, ATTRIB_ID)
        return worker.getMetadata(UID)
    return {'METHOD': 'GET METHOD NOT SUPPORTED'}


@app.route('/addtocart', methods=['GET', 'POST'])
def addToCart():
    if request.method == 'POST':
        UID = request.form['UID']
        ATTRIB_ID = request.form['ATRRIB_ID']

        value['ID'] = request.form['PRODUCT_ID']
        value['PRODUCT_NAME'] = request.form['PRODUCT_NAME']

        worker.addToCart(UID, value)
        meta = worker.getMetadata(UID)
        worker.updateMetadata(UID, int(meta['VERSION'])+1, time.time())
        worker.updateSecondaryIndex(UID, ATTRIB_ID)
        updatedMeta = worker.getMetadata(UID)
        return updatedMeta
    return {'METHOD': 'GET METHOD NOT SUPPORTED'}

@app.route('/deletefromcart', methods=['GET', 'POST'])
def deleteFromCart():
    if request.method == 'POST':
        UID = request.form['UID']
        ATTRIB_ID = request.form['ATRRIB_ID']

        value['ID'] = request.form['PRODUCT_ID']
        value['PRODUCT_NAME'] = request.form['PRODUCT_NAME']

        worker.deleteFromCart(UID, value)
        meta = worker.getMetadata(UID)
        worker.updateMetadata(UID, int(meta['VERSION'])+1, time.time())
        worker.updateSecondaryIndex(UID, ATTRIB_ID, True)
        updatedMeta = worker.getMetadata(UID)
        return updatedMeta
    return {'METHOD': 'GET METHOD NOT SUPPORTED'}

@app.route('/updatecart', methods=['GET', 'POST'])
def updateCart():
    if request.method == 'POST':
        UID = request.form['UID']

        value['ID'] = request.form['PRODUCT_ID']
        value['PRODUCT_NAME'] = request.form['PRODUCT_NAME']

        worker.updateCart(UID, value)
        meta = worker.getMetadata(UID)
        worker.updateMetadata(UID, int(meta['VERSION'])+1, time.time())
        updatedMeta = worker.getMetadata(UID)
        return updatedMeta
    return {'METHOD': 'GET METHOD NOT SUPPORTED'}

@app.route('/listcart', methods=['GET', 'POST'])
def listCart():
    if request.method == 'POST':
        UID = request.form['UID']
        
        return worker.listCart(UID)
    return {'METHOD': 'GET METHOD NOT SUPPORTED'}

@app.route('/handoff', methods=['GET', 'POST'])
def handleHandoff():
    if request.method == 'POST':
        instruction = request.form('INSTRUCTION')
        worker.handleHandoff(instruction)
        return 'SUCCESS: HANDOFF PERFORMED'

@app.route('/product', methods=['GET', 'POST'])
def getProductDetails():
    return worker.getProductDetails()

@app.route('/user', methods=['GET', 'POST'])
def getUserDetails():
    return worker.getUserDetails()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

