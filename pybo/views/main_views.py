from flask import Blueprint, url_for
from werkzeug.utils import redirect
from ..models import Question, Category

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo! hello'

@bp.route('/')
def index():
    # 가장 최근 질문을 기준으로 카테고리를 찾습니다.
    latest_question = Question.query.order_by(Question.create_date.desc()).first()
    
    if latest_question and latest_question.category:
        # 최근 질문이 속한 카테고리의 목록으로 리디렉션합니다.
        return redirect(url_for('question._list', category_name=latest_question.category.name))
    else:
        # 질문이 하나도 없으면, 첫 번째 카테고리 또는 기본 페이지로 리디렉션합니다.
        first_category = Category.query.first()
        return redirect(url_for('question._list', category_name=first_category.name if first_category else '질문과답변'))
