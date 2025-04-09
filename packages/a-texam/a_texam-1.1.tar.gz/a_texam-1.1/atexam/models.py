from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class RegistrationRequest(db.Model):
    __tablename__ = 'registration_requests'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password_plain = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_plain = password
        self.password_hash = generate_password_hash(password)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password_plain = db.Column(db.String(128), nullable=True)
    is_banned = db.Column(db.Boolean, default=False)  # Новое поле для бана

    def set_password(self, password):
        self.password_plain = password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    scheduled_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, default=30)
    is_hidden = db.Column(db.Boolean, default=False)
    max_attempts = db.Column(db.Integer, nullable=True)
    display_mode = db.Column(db.String(10), default='single')
    questions = db.relationship(
        'Question',
        backref='test',
        lazy=True,
        cascade="all, delete-orphan"
    )

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id', ondelete='CASCADE'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=0)
    answers = db.relationship('Answer', backref='question', cascade="all, delete-orphan")
    attachments = db.relationship('Attachment', backref='question', cascade="all, delete-orphan")

    @property
    def correct_answer(self):
        return next((answer for answer in self.answers if answer.is_correct), None)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)  # Можно здесь сохранять username
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Integer, default=0)
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.relationship(
        'ResultDetail',
        backref='result',
        cascade="all, delete-orphan"
    )

class ResultDetail(db.Model):
    __tablename__ = 'result_details'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    user_answer_id = db.Column(db.Integer, db.ForeignKey('answers.id', ondelete='CASCADE'))
    is_correct = db.Column(db.Boolean, default=False)
    question = db.relationship('Question', foreign_keys=[question_id])
    user_answer = db.relationship('Answer', foreign_keys=[user_answer_id])
