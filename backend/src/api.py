import os
from json import JSONDecodeError

from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from .error_handler.error_handler import ErrorHandler
from .utils.utils import check_fields_exist
from .client_error_exceptions.client_error_exceptions import BadRequest, UnprocessableEntity, NotFound, \
    ClientErrorException
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
error_handler = ErrorHandler()

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()


# ROUTES
@app.route("/drinks", methods=["GET"])
def get_drinks():
    """
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    :return: status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]

    return jsonify({
        "success": True,
        "drinks": formatted_drinks,
    })


@app.route("/drinks-detail", methods=["GET"])
def get_drinks_detail():
    """
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    :return: status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
    or appropriate status code indicating reason for failure
    """
    drinks = Drink.query.all()
    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({
        "success": True,
        "drinks": formatted_drinks,
    })


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def post_drinks(jwt_payload):
    """
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    :return: status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
    """
    data_string = request.data
    try:
        request_json = json.loads(data_string)
    except JSONDecodeError:
        raise BadRequest()

    missing_field = check_fields_exist(request_json, ["title", "recipe"])
    if missing_field:
        raise UnprocessableEntity.missing_fields(missing_field)

    try:
        drink = Drink(title=request_json["title"], recipe=json.dumps(request_json["recipe"]))
    except:
        raise UnprocessableEntity()

    try:
        drink.insert()
        return jsonify({
            "success": True,
            "drinks": [drink.long()],
        })
    except SQLAlchemyError:
        abort(500)


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drinks(jwt_payload, id):
    """
    PATCH /drinks/<id>
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    :param id: existing model id
    :return: status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
    """
    drink = Drink.query.filter_by(id=id).first()
    if not drink:
        raise NotFound("drink", id)

    data_string = request.data
    try:
        request_json = json.loads(data_string)
    except JSONDecodeError:
        raise BadRequest()
    missing_field = check_fields_exist(request_json, ["title", "recipe"])
    if missing_field:
        raise UnprocessableEntity.missing_fields(missing_field)

    try:
        drink.title = request_json["title"]
        drink.recipe = json.dumps(request_json["recipe"])
    except:
        raise UnprocessableEntity()

    try:
        drink.update()
        return jsonify({
            "success": True,
            "drinks": [drink.long()],
        })
    except SQLAlchemyError:
        abort(500)


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drinks(jwt_payload, id):
    """
    DELETE /drinks/<id>
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    :param id: existing model id
    :return: status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
    """
    drink = Drink.query.filter_by(id=id).first()
    if not drink:
        raise NotFound("drink", id)

    try:
        drink.delete()
        return jsonify({
            "success": True,
            "delete": id,
        })
    except SQLAlchemyError:
        abort(500)


@app.errorhandler(ClientErrorException)
def client_error(error):
    return error_handler.handle_error(error)


@app.errorhandler(AuthError)
def auth_error(error):
    return error_handler.handle_error(error)
