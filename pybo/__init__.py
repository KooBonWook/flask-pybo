from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from flask_mail import Mail

import config

# 네이밍 컨벤션 정의
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# 전역 변수로 db, migrate 객체 생성
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

mail = Mail() # mail 객체 생성 

def create_app():
    """
    Flask 애플리케이션을 생성하고 설정하는 팩토리 함수입니다.
    """
    app = Flask(__name__)
    app.config.from_object(config)  # config.py 파일의 설정을 로드합니다.

    # ORM
    db.init_app(app)  # init_app 메서드를 이용해 app에 등록합니다.
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app,db,render_as_batch=True)
    else:
        migrate.init_app(app,db)

    # 모델 import
    from . import models

    # 메일 초기화 
    mail.init_app(app)
    

    # 불루프린트 임포트 및 등록
    from .views import main_views, question_views, answer_views, auth_views, user_views, comment_views

    # 카테고리별 게시판 기능 추가
    @app.context_processor
    def inject_categories():
        return dict(category_list=models.Category.query.all())

    # 블루프린트 등록
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(user_views.bp)
    app.register_blueprint(comment_views.bp)

    # 필터 등록
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime
    
    # markdown 필터 등록
    from .filter import markdown_filter
    app.jinja_env.filters['markdown'] = markdown_filter

    return app