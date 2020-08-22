import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


#db_drop_and_create_all()

## ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]
    if len(formatted_drinks) != 0:
        return jsonify({
            "success": True,
            "drinks": formatted_drinks
        })
    abort(404)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(token):
    drinks = [drink.long() for drink in Drink.query.all()]
    if len(drinks) != 0:
        return jsonify({
            "success": True,
            "drinks": drinks
        })
    abort(404)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    payload = request.get_json(force=True)
    title = payload.get('title', None)
    recipe = payload.get('recipe', None)
    if title is None or recipe is None or title == '':
        abort(422)
    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            "success": True,
            "drinks" : [drink.long()],
        })
    except:
        db.session.rollback()
        abort(422)

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(token, id):
    payload = request.get_json(force=True)
    title = payload.get('title', None)
    recipe = payload.get('recipe', None)
    if title is None or recipe is None or title == '':
        abort(422)
    drink = Drink.query.get(id)
    if drink is None:
        abort(404)
    try:
        drink.title = title
        drink.recipe = json.dumps(recipe)
        db.session.commit()
        return jsonify({
        "success": True,
        "drinks" : [drink.long()],
        })
    except:
        db.session.rollback()
        abort(422)

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, id):
    drink = Drink.query.get(id)
    if drink is None:
        abort(404)
    try:
        db.session.delete(drink)
        db.session.commit()
        return jsonify({
        "success": True,
        "delete" : id,
        })
    except:
        db.session.rollback()
        abort(422)


## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(403)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "unauthorized"
    }), 403


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(401)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "auth error"
    }), 401
