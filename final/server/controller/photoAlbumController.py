import json
from os import abort
from bson import json_util, ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from server.controller.userController import admin_required
import server.app as main
from server.model.photoAlbumModel import PhotoAlbumModel
from server.model.userModel import UserModel

photoAlbum = Blueprint('photoAlbum', __name__)


@photoAlbum.route('/photoAlbum', methods=['GET'])
def index():
    try:
        current_user = UserModel.getUserByEmail(get_jwt_identity())

        if current_user is None or current_user["role"] == main.app.config['GUEST_ROLE']:
            images = list(PhotoAlbumModel.getPicturesApproved())
        else:
            images = list(PhotoAlbumModel.getPictures())

        return json.dumps(images, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@photoAlbum.route('/photoAlbum/upload', methods=['POST'])
@jwt_required()
def upload():
    try:

        current_user = UserModel.getUserByEmail(get_jwt_identity())
        if 'file' not in request.files:
            response = jsonify({"message": "Adicione um arquivo."})
            response.status_code = 400
            return response

        file = request.files['file']

        if file.filename == '':
            response = jsonify({"message": "Adicione um arquivo."})
            response.status_code = 400
            return response

        if file is None:
            abort(500)
        print(PhotoAlbumModel.newPicture(file, "nome"))
        response = jsonify({"message": "Upload Image Succeed"}), 200
        return response

    except Exception:
        abort(500)


@photoAlbum.route('/photoAlbum/<id>', methods=['DELETE'])
@jwt_required()
def remove(id):
    try:

        current_user = UserModel.getUserByEmail(get_jwt_identity())
        image = PhotoAlbumModel.getPictureById(ObjectId(id))
        if image is None:
            return json.dumps({"message": "No Image"}, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

        PhotoAlbumModel.deleteImage(image)
        print("fim")
        return jsonify({"message": "Upload Deleted Sucessed"}), 200

    except Exception:
        abort(500)


@photoAlbum.route('/photoAlbum/<id>/approve', methods=['PUT'])
@jwt_required()
@admin_required
def approve(id):
    try:
        current_user = UserModel.getUserByEmail(get_jwt_identity())

        PhotoAlbumModel.approveImage("none", ObjectId(id))
        image = PhotoAlbumModel.getPictureById(ObjectId(id))

        return json.dumps(image, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@photoAlbum.route('/photoAlbum/<id>/disapprove', methods=['PUT'])
@jwt_required()
@admin_required
def disapprove(id):
    try:
        current_user = UserModel.getUserByEmail(get_jwt_identity())

        PhotoAlbumModel.disapproveImage("nome", ObjectId(id))
        image = PhotoAlbumModel.getPictureById(ObjectId(id))

        return json.dumps(image, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)


@photoAlbum.route('/photoAlbum/<id>/like', methods=['PUT'])
@jwt_required()
def like(id):
    try:
        current_user = UserModel.getUserByEmail(get_jwt_identity())

        response = jsonify({"message": "Like Sucessed"}), 200
        result = PhotoAlbumModel.like("some", ObjectId(id))

        image = PhotoAlbumModel.getPictureById(ObjectId(id))

        return json.dumps(image, default=json_util.default), 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception:
        abort(500)