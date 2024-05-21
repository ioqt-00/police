from typing import Any
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from config import db


# Association tables for many-to-many relationships
resource_tag_association = db.Table('resource_tag_association',
                                    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), primary_key=True),
                                    db.Column('tag_id', db.Integer, db.ForeignKey('resource_tag.id'), primary_key=True)
                                    )

resource_event_association = db.Table('resource_event_association',
                                      db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), primary_key=True),
                                      db.Column('event_id', db.Integer, db.ForeignKey('resource_event.id'), primary_key=True)
                                      )

event_tag_association = db.Table('event_tag_association',
                                 db.Column('event_id', db.Integer, db.ForeignKey('resource_event.id'), primary_key=True),
                                 db.Column('tag_id', db.Integer, db.ForeignKey('event_tag.id'), primary_key=True)
                                 )

event_link_association = db.Table('event_link_association',
                                  db.Column('event_id', db.Integer, db.ForeignKey('resource_event.id'), primary_key=True),
                                  db.Column('linked_event_id', db.Integer, db.ForeignKey('resource_event.id'), primary_key=True)
                                  )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    resources = db.relationship('Resource', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'resources': [resource.to_dict() for resource in self.resources]
        }

    # Methods for password hashing and verification
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    source_date = db.Column(db.Date, nullable=True)
    source_time = db.Column(db.Time, nullable=True)
    source_place = db.Column(db.String(200), nullable=True)
    source_place_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    resource_events = db.relationship('ResourceEvent', secondary=resource_event_association, backref=db.backref('resources', lazy='dynamic'))
    tags = db.relationship('ResourceTag', secondary=resource_tag_association, backref=db.backref('resources', lazy='dynamic'))

    def __repr__(self) -> str:
        return f"<Resource(id={self.id}, resource_type='{self.resource_type}', user_id={self.user_id})>"

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'resource_type': self.resource_type,
            'uploaded_at': self.uploaded_at.isoformat(),
            'user_id': self.user_id,
            'source_date': self.source_date.isoformat() if self.source_date else None,
            'source_time': self.source_time.isoformat() if self.source_time else None,
            'source_place': self.source_place,
            'source_place_type': self.source_place_type,
            'description': self.description,
            'data': 'Binary data not displayed',
            'resource_events': [event.to_dict() for event in self.resource_events],
            'tags': [tag.to_dict() for tag in self.tags]
        }


class ResourceEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.Date, nullable=False)
    event_place = db.Column(db.String(200), nullable=False)
    tags = db.relationship('EventTag', secondary=event_tag_association, backref=db.backref('resources', lazy='dynamic'))
    linked_events = db.relationship(
                                    'ResourceEvent', secondary=event_link_association,
                                    primaryjoin=(event_link_association.c.event_id == id),
                                    secondaryjoin=(event_link_association.c.linked_event_id == id),
                                    backref=db.backref('linked_to', lazy='dynamic')
                                    )

    def __repr__(self) -> str:
        return f"<ResourceEvent(id={self.id}, resource_id={self.resource_id}, event_date={self.event_date})>"

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'resource_id': self.resource_id,
            'event_date': self.event_date.isoformat(),
            'event_place': self.event_place,
            'tags': [tag.to_dict() for tag in self.tags],
            'linked_events': [event.id for event in self.linked_events]
        }


class ResourceTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<ResourceTag(id={self.id}, name='{self.name}')>"

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name
        }


class EventTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<EventTag(id={self.id}, name='{self.name}')>"

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name
        }
