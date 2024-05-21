from flask import Blueprint, request, jsonify, Response

from config import db
from model import ResourceTag
from routes.helpers import admin_required

resource_tag_bp = Blueprint('resource_tag_bp', __name__)


@resource_tag_bp.route('/', methods=['POST'])
@admin_required()
def create_resource_tag() -> tuple[Response, int]:
    data = request.json
    new_tag = ResourceTag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify(new_tag.to_dict()), 201


@resource_tag_bp.route('/', methods=['GET'])
def get_resource_tags() -> tuple[Response, int]:
    tags = ResourceTag.query.all()
    tag_list = []
    for tag in tags:
        tag_list.append(tag.to_dict())
    return jsonify(tag_list), 200


@resource_tag_bp.route('/<int:id>', methods=['GET'])
def get_resource_tag(id: int) -> tuple[Response, int]:
    tag = ResourceTag.query.get_or_404(id)
    return jsonify(tag.to_dict()), 200


@resource_tag_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_resource_tag(id: int) -> tuple[Response, int]:
    data = request.json
    tag = ResourceTag.query.get_or_404(id)
    if 'name' in data:
        tag.name = data['name']
    db.session.commit()
    return jsonify(tag.to_dict())


@resource_tag_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_resource_tag(id: int) -> tuple[Response, int]:
    tag = ResourceTag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return '', 204
