from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Toy, ToyStore
app = Flask(__name__)

engine = create_engine('sqlite:///toystoredb.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def returnToystores():
    """Gets all available toystores"""
    stores = session.query(ToyStore).all()
    return stores

def returnRecentToys():
    """Returns the ten most recent toys"""
    recentToys = session.query(Toy).limit(10)
    return recentToys


def returnToystore(toystore_id):
    """returns a single store by id"""
    store = session.query(ToyStore).filter_by(id=toystore_id).one()
    return store

def returnToysForStore(toystore_id):
    """Returns all the toys for a specific store"""
    toysforstore = session.query(Toy).filter_by(toystore_id=toystore_id)
    return toysforstore

def returnToy(toy_id):
    """Returns a single toy"""
    toy = session.query(Toy).filter_by(id=toy_id).one()
    return toy

def returnToys():
    """Returns all toys"""
    alltoys = recentToys = session.query(Toy)
    return alltoys
    