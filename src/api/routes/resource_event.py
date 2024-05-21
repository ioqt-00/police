from flask import Blueprint, request, jsonify, Response

from config import db
from model import ResourceEvent
from routes.helpers import admin_required


resource_event_bp = Blueprint('resource_event_bp', __name__)


@resource_event_bp.route('/', methods=['POST'])
@admin_required()
def create_resource_event() -> tuple[Response, int]:
    data = request.json
    new_event = ResourceEvent(
        title=data.get('title', '(notitle)'),
        event_date=data['event_date'],
        event_place=data['event_place']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201


@resource_event_bp.route('/', methods=['GET'])
@admin_required()
def get_resource_events() -> tuple[Response, int]:
    events = ResourceEvent.query.all()
    event_list = []
    for event in events:
        event_list.append(event.to_dict())
    return jsonify(event_list), 200


@resource_event_bp.route('/<int:id>', methods=['GET'])
@admin_required()
def get_resource_event(id: int) -> tuple[Response, int]:
    event = ResourceEvent.query.get_or_404(id)
    return jsonify(event.to_dict())


@resource_event_bp.route('/<int:id>', methods=['PUT'])
@admin_required()
def update_resource_event(id: int) -> tuple[Response, int]:
    data = request.json
    event = ResourceEvent.query.get_or_404(id)
    event.title = data.get('title', event.title)
    if 'event_date' in data:
        event.event_date = data['event_date']
    if 'event_place' in data:
        event.event_place = data['event_place']
    db.session.commit()
    return jsonify(event.to_dict())


@resource_event_bp.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete_resource_event(id: int) -> tuple[Response, int]:
    event = ResourceEvent.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return '', 204
