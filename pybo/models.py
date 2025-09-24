# 파이보에 ORM을 적용하려면 데이터베이스 설정이 필요
# ORM 라이브러리 설치하기
# Flask-Migrate 라이브러리를 설치하면 SQLAlchemy도 함께 설치함 

from pybo import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), unique=True, nullable=False)
    question_set = db.relationship('Question', back_populates='category')

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='question_set')
    answer_set = db.relationship('Answer', back_populates='question', cascade='all, delete-orphan')
    voter = db.relationship('User', secondary=question_voter, back_populates='question_voter_set')
    comment_set = db.relationship('Comment', back_populates='question', cascade='all, delete-orphan')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False, server_default=db.text('1'))
    category = db.relationship('Category', back_populates='question_set')
    view_count = db.Column(db.Integer, server_default='0', nullable=False)

answer_voter= db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    question = db.relationship('Question', back_populates='answer_set')
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='answer_set')
    voter = db.relationship('User', secondary=answer_voter, back_populates='answer_voter_set')
    comment_set = db.relationship('Comment', back_populates='answer', cascade='all, delete-orphan')
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)   # email 중복허용 
    create_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    question_set = db.relationship('Question', back_populates='user', cascade='all, delete-orphan')
    answer_set = db.relationship('Answer', back_populates='user', cascade='all, delete-orphan')
    question_voter_set = db.relationship('Question', secondary=question_voter, back_populates='voter')
    answer_voter_set = db.relationship('Answer', secondary=answer_voter, back_populates='voter')
    comment_set = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='comment_set')
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', back_populates='comment_set')
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', back_populates='comment_set')
