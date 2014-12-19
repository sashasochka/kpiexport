"""Model

This module descibes DB models/entities implementation
"""


import calendar
import os
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from hashlib import sha256

from motorengine import Document, StringField, EmailField, DateTimeField, \
                        IntField, BinaryField, \
                        ReferenceField, ListField, EmbeddedDocumentField


__all__ = [
            "University", "Group", "User",
            "Schedule", "DayTimetable",
            "Lesson", "Comment"
            ]


class User(Document):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    id = IntField(unique=True)
    email = EmailField()

    _salt = BinaryField(12)
    # 64 is the length of the SHA-256 encoded string length
    _password = StringField(64)

    group = ReferenceField('scheduler.model.Group')
    timetable = EmbeddedDocumentField('scheduler.model.Schedule')


class Comment(Document):
    user = ReferenceField(reference_document_type=User)
    lesson = ReferenceField('Lesson')
    #user_picture_url
    text = StringField(required=True)
    time = DateTimeField()


class Lesson(Document):
    id = IntField()
    name = StringField(required=True)
    audience = StringField()
    teacher_name = StringField()
    lesson_type = StringField()
    start_time = StringField()
    color = StringField()
    comments = ListField(EmbeddedDocumentField(embedded_document_type=Comment))
    day = ReferenceField('DayTimetable')


class DayTimetable(Document):
    name = StringField(required=True)
    lessons = ListField(EmbeddedDocumentField(Lesson()))
    schedule = ReferenceField('scheduler.model.Schedule')


class Schedule(Document):
    days = ListField(EmbeddedDocumentField(DayTimetable()))
    user = ReferenceField(reference_document_type=User)
    group = ReferenceField('scheduler.model.Group')
    pass


class Group(Document):
    id = IntField()
    name = StringField(required=True)
    users = ListField(ReferenceField('User'))
    university = ReferenceField('University')
    timetable = EmbeddedDocumentField(Schedule())


class University(Document):
    id = IntField()
    name = StringField(required=True)
    groups = ListField(EmbeddedDocumentField(Group()))
