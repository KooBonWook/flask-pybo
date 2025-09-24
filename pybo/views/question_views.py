from datetime import datetime

from sqlalchemy import func, or_
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import QuestionForm, AnswerForm, CommentForm
from ..models import Question, Answer, User, Category
from .auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/', defaults={'category_name': '질문과답변'})
@bp.route('/list/<string:category_name>/')
def _list(category_name):
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    category = Category.query.filter_by(name=category_name).first_or_404()

    question_list = Question.query.filter_by(category=category).order_by(Question.create_date.desc())
    if kw:
        search = f'%%{kw}%%'
        # relationship.any()를 사용하여 질문과 답변, 각 작성자를 모두 포함하는 검색 구현
        # 이 방식은 복잡한 JOIN과 DISTINCT를 피할 수 있어 더 효율적이고 가독성이 좋습니다.
        question_list = question_list.join(Question.user).filter(
            or_(
                Question.subject.ilike(search),
                Question.content.ilike(search),
                User.username.ilike(search),  # 질문 작성자
                Question.answer_set.any(Answer.content.ilike(search)),  # 답변 내용
                Question.answer_set.any(Answer.user.has(User.username.ilike(search)))  # 답변 작성자
            )
        )
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, category=category)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    comment_form = CommentForm()
    question = Question.query.get_or_404(question_id)

    # 조회수 증가
    question.view_count = (question.view_count or 0) + 1
    db.session.commit()

    so = request.args.get('so', type=str, default='recent')
    page = request.args.get('page', type=int, default=1)

    if so == 'recommend':
        answer_voter_table = Answer.voter.property.secondary
        sub_query = db.session.query(answer_voter_table.c.answer_id, func.count('*').label('num_voter'))\
            .group_by(answer_voter_table.c.answer_id).subquery()
        answer_list = Answer.query \
            .outerjoin(sub_query, Answer.id == sub_query.c.answer_id) \
            .filter(Answer.question_id == question_id) \
            .order_by(func.coalesce(sub_query.c.num_voter, 0).desc(), Answer.create_date.desc())
    else:  # recent
        answer_list = Answer.query.filter(Answer.question_id == question_id) \
            .order_by(Answer.create_date.desc())

    answer_list = answer_list.paginate(page=page, per_page=5)

    return render_template('question/question_detail.html', question=question, form=form, answer_list=answer_list, so=so, comment_form=comment_form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
    else:  # GET 요청
        form = QuestionForm(obj=question)
    if form.validate_on_submit():  # POST 요청이며, 내용이 유효한 경우
        question.subject = form.subject.data
        question.content = form.content.data
        question.category = Category.query.get(form.category.data)
        question.modify_date = datetime.now()
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    elif request.method == 'GET':  # GET 요청인 경우, 기존 카테고리 선택
        if question.category:
            form.category.data = question.category.id
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    category_name = question.category.name
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list', category_name=category_name))

@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    elif g.user in _question.voter:
        flash('이미 추천한 글입니다.')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/create/', defaults={'category_name': None}, methods=('GET', 'POST'))
@bp.route('/create/<string:category_name>/', methods=('GET', 'POST'))
@login_required
def create(category_name):
    form = QuestionForm()
    if request.method == 'GET' and category_name:
        category = Category.query.filter_by(name=category_name).first()
        if category:
            form.category.data = category.id

    if form.validate_on_submit():
        category = Category.query.get(form.category.data)
        q = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user, category=category)
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('question._list', category_name=q.category.name))
    return render_template('question/question_form.html', form=form)

@bp.route('/answers/')
def recent_answers():
    """
    최근 작성된 답변 목록을 보여줍니다.
    """
    page = request.args.get('page', type=int, default=1)

    # join을 사용하여 질문이나 사용자가 삭제된 답변은 조회하지 않음
    answer_list = Answer.query.join(Question).join(User)\
        .order_by(Answer.create_date.desc())\
        .paginate(page=page, per_page=15)

    return render_template('answer/answer_list.html', answer_list=answer_list)
