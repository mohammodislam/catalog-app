import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from db import db_session
from models import Items, Categories
from flask_json import JsonError, json_response, as_json

bp = Blueprint('item', __name__)

@bp.route('/item/new')
def new():
  return render_template('item.html', categories=Categories.query.all())


@bp.route('/item/save', methods=['POST'])
def save():
  category_id = request.form['category']
  user_id = session.get('user_id')
  title = request.form['title']
  description = request.form['description']

  #validation
  error = None
  if title is None:
    error = 'Title is required'
  elif description is None:
    error = 'Description is required'
  
  if error is None:
    itm = Items(category_id=category_id, user_id=user_id, title=title, description=description)
    db_session.add(itm)
    db_session.commit()
    return redirect(url_for('index'))

  flash(error)
  
  return redirect(url_for('item.new'))


@bp.route('/item/details/<int:id>', methods=['GET'])
def details(id):
  item = Items.query.filter(Items.id == id).first()
  return render_template('details.html', item = item)


@bp.route('/item/delete/<int:id>', methods=['GET'])
def delete(id):
  item = Items.query.filter(Items.id == id).one()
  db_session.delete(item)
  db_session.commit()
  return redirect(url_for('index'))


@bp.route('/item/edit/<int:id>', methods=['GET'])
def edit(id):
  item = Items.query.filter(Items.id == id).one()
  return render_template('edit_item.html', categories=Categories.query.all(), item=item)


@bp.route('/item/update', methods=['POST'])
def update():
  id = request.form['id']
  title = request.form['title']
  category = request.form['category']
  description = request.form['description']

  # Validation
  error = None
  if title is None:
    error = 'Title is required'
  elif description is None:
    error = 'Description is required'

  if error is None:
    db_session.query(Items).filter(Items.id == id).update({
      'title': title,
      'category_id': category,
      'description': description
    })
    db_session.commit()

  return redirect(url_for('index'))


@bp.route('/items/json')
@as_json
def all():
  items = Items.query.all()
  list_items = []
  for item in items:
    data = {
      'item_id': item.id, 
      'data': {
        'category_id': item.category_id,
        'user_id': item.user_id,
        'title': item.title,
        'description': item.description
      }
    }
    list_items.append(data)

  return dict(value=list_items)