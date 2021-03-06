from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Toy, ToyStore, User
import database_functions
app = Flask(__name__)

engine = create_engine('sqlite:///toystoredb.db')


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

def login_required(func):
    """check if the user is logged in"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """func decorator"""
        if 'username' not in login_session:
            return redirect('/login')
        return func(*args, **kwargs)
    return decorated_function

def is_authorised(creator):
    """checks if the user is also the creator"""
    return creator.id == login_session['user_id']

def auth_bool(creator):
    """checks if the user is authorised and sets a bool"""
    if creator.id != login_session['user_id']:
        authorised = False
    else:
        authorised = True
    return authorised

def logged_in_bool():
    """checks if the user is logged in and sets a bool"""
    if 'username' not in login_session:
        logged_in = False
    else:
        logged_in = True
    return logged_in

@app.route('/')

@app.route('/login')
def showLogin():
    """shows the google login page"""
    logged_in = logged_in_bool()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', logged_in=logged_in, STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

     # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    """creates a new user"""
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """get the user information from their id"""
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """gets the user's email"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None



@app.route('/gdisconnect')
def gdisconnect():
    """The logout function"""
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
    login_session.clear()
    return response


@app.route('/toystores/')
def toystores():
    """The main page"""
    logged_in = logged_in_bool()
    toys = dbq.returnRecentToys()
    stores = dbq.returnToystores()
    return render_template('main.html', toys=toys, logged_in=logged_in, stores=stores)

@app.route('/toys/')
def toys():
    """lists all the toys on a page"""
    logged_in = logged_in_bool()
    alltoys = dbq.returnToys()
    return render_template('toys.html', logged_in=logged_in, toys=alltoys)

@app.route('/toystores/<int:toystore_id>/')
def toystoreDescription(toystore_id):
    """Description of the toystore"""
    toystore = dbq.returnToystore(toystore_id)
    creator = getUserInfo(toystore.user_id)
    store = dbq.returnToystore(toystore_id)
    storetoys = dbq.returnToysForStore(toystore_id)

    logged_in = logged_in_bool()
    if logged_in:
        authorised = auth_bool(creator)
    else:
        authorised = False

    return render_template('store_info.html', store=store, logged_in=logged_in,
                           authorised=authorised, storetoys=storetoys)


@app.route('/toys/<int:toystore_id>/<int:toy_id>/')
def toyDescription(toystore_id, toy_id):
    """shows description of the individual toy"""
    toy = dbq.returnToy(toy_id)
    creator = getUserInfo(toy.user_id)

    logged_in = logged_in_bool()
    if logged_in:
        authorised = auth_bool(creator)
    else:
        authorised = False

    return render_template('toy_info.html', toy=toy, logged_in=logged_in,
                           authorised=authorised, toystore_id=toystore_id)


@app.route('/toystores/new/', methods=['GET', 'POST'])
@login_required
def newToystore():
    """adds a new toystore"""
    logged_in = logged_in_bool()

    if request.method == 'POST':
        newStore = ToyStore(name=request.form['name'],
                            description=request.form['description'],
                            address=request.form['address'],
                            phone_number=request.form['phone_number'],
                            user_id=login_session['user_id'])
        session.add(newStore)
        session.commit()
        flash("New toysore added")
        return redirect(url_for('toystores'))
    else:
        return render_template('add_toystore.html', logged_in=logged_in)


@app.route('/toystores/<int:toystore_id>/add-toy/', methods=['GET', 'POST'])
@login_required
def newToy(toystore_id):
    """adds a new toy"""
    toystore = dbq.returnToystore(toystore_id)
    creator = getUserInfo(toystore.user_id)
    logged_in = logged_in_bool()
    if not is_authorised(creator):
        return redirect(url_for('toystoreDescription', toystore_id=toystore_id))

    toystore = dbq.returnToystore(toystore_id)
    if request.method == 'POST':
        addNewToy = Toy(name=request.form['name'],
                        description=request.form['description'],
                        price=request.form['price'],
                        color=request.form['color'],
                        toystore_id=toystore_id,
                        user_id=toystore.user_id)
        session.add(addNewToy)
        session.commit()
        toy_id = addNewToy.id
        return redirect(url_for('toyDescription', toystore_id=toystore_id, toy_id=toy_id))
    else:
        return render_template('add_toy.html', logged_in=logged_in, toystore_id=toystore_id)


@app.route('/toystores/<int:toystore_id>/edit/', methods=['GET', 'POST'])
@login_required
def editToystore(toystore_id):
    """edit the toystore details"""
    toystore = dbq.returnToystore(toystore_id)
    creator = getUserInfo(toystore.user_id)
    logged_in = logged_in_bool()

    if not is_authorised(creator):
        return redirect(url_for('toystoreDescription', toystore_id=toystore_id))

    editedStore = session.query(ToyStore).filter_by(id=toystore_id).one()
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
            'edit_toystore.html', logged_in=logged_in, toystore_id=toystore_id, item=editedStore)

@app.route('/toys/<int:toystore_id>/<int:toy_id>/edit', methods=['GET', 'POST'])
@login_required
def editToy(toy_id,toystore_id):
    """edit individual toy"""
    toystore = dbq.returnToystore(toystore_id)
    creator = getUserInfo(toystore.user_id)

    if not is_authorised(creator):
        return redirect(url_for('toyDescription', toy_id=toy_id,  toystore_id=toystore_id))

    logged_in = logged_in_bool()
    editedToy = session.query(Toy).filter_by(id=toy_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedToy.name = request.form['name']
        if request.form['description']:
            editedToy.description = request.form['description']

        if request.form['color']:
            editedToy.color = request.form['color']

        if request.form['price']:
            editedToy.price = request.form['price']

        session.add(editedToy)
        session.commit()
        toy_id = editedToy.id
        return redirect(url_for('toyDescription', toystore_id=toystore_id, toy_id=toy_id))
    else:
        return render_template('edit_toy.html', logged_in=logged_in, toystore_id=toystore_id,
                               toy_id=toy_id, toy=editedToy)


@app.route('/toystores/<int:toystore_id>/delete', methods=['GET', 'POST'])
@login_required
def toystoreDelete(toystore_id):
    """Delete toystore function"""
    toystore = dbq.returnToystore(toystore_id)
    creator = getUserInfo(toystore.user_id)
    logged_in = logged_in_bool()

    if not is_authorised(creator):
        return redirect(url_for('toystoreDescription', toystore_id=toystore_id))

    toystoredelete = session.query(ToyStore).filter_by(id=toystore_id).one()
    if request.method == 'POST':
        session.delete(toystoredelete)
        session.commit()
        return redirect(url_for('toystores'))
    else:
        return render_template('delete_toystore.html', logged_in=logged_in, item=toystoredelete)

@app.route('/toys/<int:toystore_id>/<int:toy_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteToy(toy_id, toystore_id):
    """Delete toystore function"""
    toystore = dbq.returnToystore(toystore_id)
    creator = getUserInfo(toystore.user_id)
    logged_in = logged_in_bool()

    if not is_authorised(creator):
        return redirect(url_for('toyDescription', toy_id=toy_id, toystore_id=toystore_id))

    toy = session.query(Toy).filter_by(id=toy_id).one()
    if request.method == 'POST':
        session.delete(toy)
        session.commit()
        return redirect(url_for('toystoreDescription', logged_in=logged_in,
                                toystore_id=toystore_id))
    else:
        return render_template('delete_toy.html', toy=toy, toystore_id=toystore_id)


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
