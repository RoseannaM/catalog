from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Toy, ToyStore
import database_functions
app = Flask(__name__)

engine = create_engine('sqlite:///toystore.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import session as login_session
import random, string

# IMPORTS FOR THIS GCONNECT
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
dbq = database_functions

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Toystore Catalogue"

@app.route('/')





@app.route('/toystores/')
def toystores():
    toys = dbq.returnRecentToys()
    stores = dbq.returnToystores()
    return render_template('main.html', toys=toys, stores=stores)

@app.route('/toys/')
def toys():
    alltoys = dbq.returnToys()
    return render_template('toys.html', toys=alltoys)

@app.route('/toystores/<int:toystore_id>/')
def toystore(toystore_id):
    store = dbq.returnToystore(toystore_id)
    storetoys = dbq.returnToysForStore(toystore_id)
    return render_template('store_info.html', store=store, storetoys=storetoys)


@app.route('/toys/<int:toystore_id>/<int:toy_id>/')
def toyDescription(toystore_id, toy_id):
    toy = dbq.returnToy(toy_id)
    return render_template('toy_info.html', toy=toy)



@app.route('/toystores/new/', methods=['GET', 'POST'])
def newToystore():
    if request.method == 'POST':
        newStore = ToyStore(name=request.form['name'],
                            description=request.form['description'],
                            address=request.form['address'],
                            phone_number=request.form['phone_number'])
        session.add(newStore)
        session.commit()
        flash("New toysore added")
        return redirect(url_for('toystores'))
    else:
        return render_template('add_toystore.html')

@app.route('/toystores/<int:toystore_id>/add-toy/', methods=['GET', 'POST'])
def newToy(toystore_id):
    print toystore_id
    if request.method == 'POST':
        addNewToy = Toy(name=request.form['name'],
                        description=request.form['description'],
                        price=request.form['price'],
                        color=request.form['color'],
                        toystore_id=toystore_id)
        session.add(addNewToy)
        session.commit()
        flash("New toy added")
        return redirect(url_for('toystores'))
    else:
        print toystore_id
        return render_template('add_toy.html', toystore_id=toystore_id)



@app.route('/toystores/<int:toystore_id>/edit/', methods=['GET', 'POST'])
def editToystore(toystore_id):
    editedStore = session.query(ToyStore).filter_by(id=toystore_id).one()
    print editedStore
    if request.method == 'POST':
        if request.form['name']:
            editedStore.name = request.form['name']
        if request.form['description']:
            editedStore.description = request.form['description']

        if request.form['phone_number']:
            editedStore.phone_number = request.form['phone_number']

        if request.form['address']:
            editedStore.address = request.form['address']

        session.add(editedStore)
        session.commit()
        return redirect(url_for('toystores'))
    else:
        return render_template(
            'edit_toystore.html', toystore_id=toystore_id, item=editedStore)



@app.route('/toystores/<int:toystore_id>/delete', methods=['GET', 'POST'])
def toystoreDelete(toystore_id):
    """Delete toystore function"""
    #confim logged in? 
    toystoredelete = session.query(ToyStore).filter_by(id=toystore_id).one()
    if request.method == 'POST':
        session.delete(toystoredelete)
        session.commit()
        return redirect(url_for('toystores'))
    else:
        return render_template('delete_toystore.html', item=toystoredelete)



#JSON Endpoints

@app.route('/toys/JSON')
def toysJSON():
    """returns all the toys in a json blob"""
    toys = dbq.returnToys()
    return jsonify(Toy=[i.serialize for i in toys])

@app.route('/toystores/JSON')
def toystoresJSON():
    """returns all the toystores in a json blob"""
    toystores = dbq.returnToystores()
    return jsonify(ToyStore=[i.serialize for i in toystores])

@app.route('/toys/<int:toystore_id>/<int:toy_id>/JSON')
def toyDescriptionJSON(toystore_id, toy_id):
    """returns a specific toy's info in a json blob"""
    toy = dbq.returnToy(toy_id)
    return jsonify(Toy=toy.serialize)

@app.route('/toystores/<int:toystore_id>/JSON')
def toystoredescriptionJSON(toystore_id):
    toystore = dbq.returnToystore(toystore_id)
    return jsonify(ToyStore=toystore.serialize)



if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
