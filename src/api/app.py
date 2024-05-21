import os

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from model import User
from config import db, app
from routes.user import user_bp
from routes.resource import resource_bp
from routes.resource_event import resource_event_bp
from routes.event_tag import event_tag_bp
from routes.resource_tag import resource_tag_bp


@app.route('/login', methods=['POST'])
def create_token() -> tuple[Response, int]:
    data = request.json
    username = data["username"]
    password = data["password"]
    user = User.query.filter(User.username == username).scalar()
    if user is None or not user.check_password(password):
        return jsonify({"message": "Wrong credentials"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200


@app.route('/logout', methods=['POST'])
def logout() -> tuple[Response, int]:
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200


app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(resource_bp, url_prefix='/resources')
app.register_blueprint(resource_event_bp, url_prefix='/resource_events')
app.register_blueprint(resource_tag_bp, url_prefix='/resource_tags')
app.register_blueprint(event_tag_bp, url_prefix='/event_tags')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    env = os.getenv("FLASK_ENV")
    port = os.getenv("FLASK_PORT")
    if env == "development":
        app.run(host="0.0.0.0", debug=True)
    else:
        from waitress import serve
        import logging
        logger = logging.getLogger('waitress')
        logger.setLevel(logging.INFO)
        serve(app, host="0.0.0.0", port=port)
