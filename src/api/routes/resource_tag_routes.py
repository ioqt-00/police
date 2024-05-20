from flask import Blueprint, request, jsonify, Response

from config import db
from model import ResourceTag

resource_tag_bp = Blueprint('resource_tag_bp', __name__)


@resource_tag_bp.route('/', methods=['POST'])
def create_resource_tag() -> tuple[Response, int]:
    data = request.json
    new_tag = ResourceTag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify(new_tag.to_dict()), 201


@resource_tag_bp.route('/<int:id>', methods=['GET'])
def get_resource_tag(id: int) -> tuple[Response, int]:
    tag = ResourceTag.query.get_or_404(id)
    return jsonify(tag.to_dict()), 200


@resource_tag_bp.route('/<int:id>', methods=['PUT'])
def update_resource_tag(id: int) -> tuple[Response, int]:
    data = request.json
    tag = ResourceTag.query.get_or_404(id)
    if 'name' in data:
        tag.name = data['name']
    db.session.commit()
    return jsonify(tag.to_dict())


@resource_tag_bp.route('/<int:id>', methods=['DELETE'])
def delete_resource_tag(id: int) -> tuple[Response, int]:
    tag = ResourceTag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return '', 204
