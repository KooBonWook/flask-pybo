from flask import Blueprint, render_template, g, redirect, url_for
from ..models import User, Question, Answer, Comment
from .auth_views import login_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile/')
@login_required
def profile_current_user():
    """
    현재 로그인한 사용자의 프로필 페이지로 리디렉션합니다.
    """
    return redirect(url_for('user.profile', user_id=g.user.id))

@bp.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    """
    사용자 프로필 페이지를 렌더링합니다.
    사용자의 기본 정보, 작성한 질문, 답변, 댓글 목록을 보여줍니다.
    """
    user = User.query.get_or_404(user_id)

    # 사용자가 작성한 질문 (최신 5개)
    questions = Question.query.filter_by(user_id=user.id)\
        .order_by(Question.create_date.desc())\
        .limit(5).all()

    # 사용자가 작성한 답변 (최신 5개)
    answers = Answer.query.filter_by(user_id=user.id)\
        .order_by(Answer.create_date.desc())\
        .limit(5).all()

    # 사용자가 작성한 댓글 (최신 5개)
    comments = Comment.query.filter_by(user_id=user.id)\
        .order_by(Comment.create_date.desc())\
        .limit(5).all()

    # 총 개수
    question_count = Question.query.filter_by(user_id=user.id).count()
    answer_count = Answer.query.filter_by(user_id=user.id).count()
    comment_count = Comment.query.filter_by(user_id=user.id).count()

    return render_template(
        'user/profile.html',
        user=user,
        questions=questions,
        answers=answers,
        comments=comments,
        question_count=question_count,
        answer_count=answer_count,
        comment_count=comment_count
    )