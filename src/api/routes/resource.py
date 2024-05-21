from typing import Any

from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from model import Resource
from routes.helpers import admin_required


resource_bp = Blueprint('resource_bp', __name__)


@resource_bp.route('/', methods=['POST'])
@jwt_required()
def create_resource() -> tuple[Response, int]:
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    user_id = get_jwt_identity()

    data = request.json
    new_resource = Resource(
        resource_type=data['resource_type'],                # type: ignore[index]
        user_id=user_id,
        source_date=data.get('source_date'),                # type: ignore[union-attr]
        source_time=data.get('source_time'),                # type: ignore[union-attr]
        source_place=data.get('source_place'),              # type: ignore[union-attr]
        source_place_type=data.get('source_place_type'),    # type: ignore[union-attr]
        description=data.get('description'),                 # type: ignore[union-attr]
        data=file.read()
    )
    db.session.add(new_resource)
    db.session.commit()
    return jsonify(new_resource.to_dict()), 201


@resource_bp.route('/<int:id>', methods=['GET'])
def get_resource(id: int) -> tuple[Response, int]:
    resource = Resource.query.get_or_404(id)
    return jsonify(resource.to_dict()), 200


@resource_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_resource(id: int) -> tuple[Response, int]:
    data = request.json
    resource = Resource.query.get_or_404(id)
    if 'resource_type' in data:
        resource.resource_type = data['resource_type']          # type: ignore[index]
    if 'source_date' in data:                                   # type: ignore[operator]
        resource.source_date = data['source_date']              # type: ignore[index]
    if 'source_time' in data:                                   # type: ignore[operator]
        resource.source_time = data['source_time']              # type: ignore[index]
    if 'source_place' in data:                                  # type: ignore[operator]
        resource.source_place = data['source_place']            # type: ignore[index]
    if 'source_place_type' in data:                             # type: ignore[operator]
        resource.source_place_type = data['source_place_type']  # type: ignore[index]
    if 'description' in data:                                   # type: ignore[operator]
        resource.description = data['description']              # type: ignore[index]
    db.session.commit()
    return jsonify(resource.to_dict())


@resource_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_resource(id: int) -> tuple[Response, int]:
    resource = Resource.query.get_or_404(id)

    if resource.user_id != get_jwt_identity():
        return jsonify({'message': 'You are not allow to delete this resource'}), 401

    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted'}), 204
