from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from db import db_session
from models import Categories, Items

bp = Blueprint('category', __name__)

@bp.route('/category/new')
def new():
  return render_template('category.html', categories=Categories.query.all())


@bp.route('/category/save',  methods=['POST'])
def save():
  category = request.form['category']

  old_category = Categories.query.filter(Categories.name == category).first()
  #validation
  error = None
  if category is None:
    error = 'Category field is required.'
  elif old_category is not None:
    error = '{} already exist in database'.format(category)
  
  print(error)
  
  if error is None: 
    c = Categories(name=category)
    db_session.add(c)
    db_session.commit()
    return redirect(url_for('category.new'))

  return "ERROR"


@bp.route('/category/delete/<int:id>',  methods=['GET'])
def delete(id):
  categories = Categories.query.filter(Categories.id == id).one()
  db_session.delete(categories)
  db_session.commit()
  return redirect(url_for('category.new'))
  

@bp.route('/category/<string:category>')
def show(category):
  items = Items.query.all()
  categories = Categories.query.all()
  catgry = Categories.query.filter(Categories.name == category).one()
  same_cat = Items.query.filter(Items.category_id == catgry.id)
  return render_template('category_details.html', items=items, category_item=same_cat, categories=categories, page=category)
