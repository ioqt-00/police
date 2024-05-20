from flask import Blueprint, request, jsonify, Response

from config import db
from model import ResourceEvent

resource_event_bp = Blueprint('resource_event_bp', __name__)


@resource_event_bp.route('/', methods=['POST'])
def create_resource_event() -> tuple[Response, int]:
    data = request.json
    new_event = ResourceEvent(
        resource_id=data['resource_id'],
        event_date=data['event_date'],
        event_place=data['event_place']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201


@resource_event_bp.route('/<int:id>', methods=['GET'])
def get_resource_event(id: int) -> tuple[Response, int]:
    event = ResourceEvent.query.get_or_404(id)
    return jsonify(event.to_dict())


@resource_event_bp.route('/<int:id>', methods=['PUT'])
def update_resource_event(id: int) -> tuple[Response, int]:
    data = request.json
    event = ResourceEvent.query.get_or_404(id)
    if 'event_date' in data:
        event.event_date = data['event_date']
    if 'event_place' in data:
        event.event_place = data['event_place']
    db.session.commit()
    return jsonify(event.to_dict())


@resource_event_bp.route('/<int:id>', methods=['DELETE'])
def delete_resource_event(id: int) -> tuple[Response, int]:
    event = ResourceEvent.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return '', 204
