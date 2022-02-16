import functools
import json
from bson import json_util
from flask import Blueprint, jsonify, request, abort
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, get_jwt_identity
from server.model.userModel import UserModel

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def register():

    try:
        userData = request.json

        email = UserModel.getUserByEmail(userData["email"])

        if email == None:
            userData["password"] = sha256.hash(userData['password'])
            userId = UserModel.createUser(userData)

            access_token = create_access_token(identity=userData['email'], expires_delta=False)

            response = {
                "data": {
                    "access_token": access_token,
                    "email": userData["email"]
                }
            }
            return json.dumps(response, default=json_util.default), 200, {
                'Content-Type': 'application/json; charset=utf-8'}
        else:
            response = jsonify({"message": "User already exists"})
            response.status_code = 400
            return response

    except Exception:
        abort(500)


@users.route('/login', methods=['POST'])
def login():

    try:
        userData = request.json

        user = UserModel.getUserByEmail(userData["email"])

        if user == None:
            response = jsonify({"message": "The email is incorrect or not registered"})
            response.status_code = 400
            return response

        else:
            if sha256.verify(userData["password"], user["password"]):
                access_token = create_access_token(identity=userData['email'], expires_delta=False)
                del user["password"]

                response = {
                        "data": {
                        "access_token": access_token,
                        "user": user
                    }
                }

                return json.dumps(response, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

            response = jsonify({"message": "Acess Denied."})
            response.status_code = 403
            return response

    except Exception:
        abort(500)

@users.route('/users/delete', methods=['DELETE'])
def deleteUser():
    try:
        user = request.json
        #user = UserModel.getUserByEmail(get_jwt_identity())
        suer = UserModel.getUserByEmail(user["email"])
        if suer != None:
            UserModel.deleteUser(suer["email"])
            response = jsonify({"message": "User Deleted."})
            response.status_code = 200
            return response
    except Exception:
        abort(500)

@users.route('/users', methods=['GET'])
def getUsers():
    return json.dumps(list(UserModel.getAllUsers()), default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

def admin_required(view):
    @functools.wraps(view)
    def admin(*args, **kwargs):
        user = UserModel.getUserByEmail(get_jwt_identity())
        from server.app import app
        if 'role' not in user or user["role"] != app.config['ADMIN_ROLE']:
            abort(403)
        return view(*args, **kwargs)
    return admin
