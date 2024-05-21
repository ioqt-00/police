from functools import wraps
from typing import Callable, Any

from flask import jsonify, Response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from model import User


# TODO ...
def admin_required() -> Callable[[], Callable]:
    def admin_required(fn: Callable[[Any], tuple[Response, int]]) -> Callable[[Any], tuple[Response, int]]:
        @wraps(fn)
        def decorator(*args, **kwargs) -> tuple[Response, int]:
            verify_jwt_in_request()
            identity = get_jwt_identity()
            admin_id = User.query.filter(User.username == "ioqt").first().id
            if identity == admin_id:
                return fn(*args, **kwargs)
            else:
                return jsonify({'message': 'Admins only!'}), 403
        return decorator
    return admin_required
