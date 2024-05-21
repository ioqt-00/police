from flask import Blueprint, request, jsonify, Response

from model import EventTag
from config import db
from routes.helpers import admin_required

event_tag_bp = Blueprint('event_tag_bp', __name__)


@event_tag_bp.route('/', methods=['POST'])
@admin_required()
def create_event_tag() -> tuple[Response, int]:
    data = request.json
    new_tag = EventTag(name=data['name'])
    db.session.add(new_tag)
    db.session.commit()
    return jsonify(new_tag.to_dict()), 201


@event_tag_bp.route('/<int:id>', methods=['GET'])
def get_event_tag(id: int) -> tuple[Response, int]:
    tag = EventTag.query.get_or_404(id)
    return jsonify(tag.to_dict()), 200


@event_tag_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_event_tag(id: int) -> tuple[Response, int]:
    data = request.json
    tag = EventTag.query.get_or_404(id)
    if 'name' in data:
        tag.name = data['name']
    db.session.commit()
    return jsonify(tag.to_dict()), 200


@event_tag_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_event_tag(id: int) -> tuple[Response, int]:
    tag = EventTag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200
