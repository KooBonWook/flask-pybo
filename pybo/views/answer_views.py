from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from datetime import datetime

from pybo import db
from pybo.models import Question, Answer
from pybo.forms import AnswerForm
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=['POST'])
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
 
    if form.validate_on_submit():
        # Answer 모델의 user 속성에 g.user 객체를 할당하면
        # SQLAlchemy가 알아서 user_id를 처리합니다.
        answer = Answer(question=question,
                        content=form.content.data,
                        create_date=datetime.now(),
                        user=g.user)
        db.session.add(answer)
        db.session.commit()
        #return redirect(url_for('question.detail', question_id=question_id, _anchor=f'answer_{answer.id}'))
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id))
    # 폼 검증 실패 시, question_detail.html 템플릿에서 form.errors를 통해 오류를 표시할 수 있습니다.
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    
    if request.method == 'POST':
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            #return redirect(url_for('question.detail', question_id=answer.question.id, _anchor=f'answer_{answer.id}'))
            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))
    else:    
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form, answer=answer)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    elif g.user in _answer.voter:
        flash('이미 추천한 글입니다.')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    #return redirect(url_for('question.detail', question_id=_answer.question.id, _anchor=f'answer_{_answer.id}'))
    return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=_answer.question.id), _answer.id))