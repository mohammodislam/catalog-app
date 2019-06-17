from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from db import db_session
from models import Categories, Items

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
  all_Items = db_session.query(Items, Categories).join(Categories)
  categories = Categories.query.all()
  return render_template('home.html', categories=categories, items=all_Items)


