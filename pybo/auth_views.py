from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools
from datetime import datetime
    

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm, PasswordChangeForm, FindPasswordForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(**kwargs)
    return wrapped_view


@bp.route('/register/', methods=('GET', 'POST'))
def register():

    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_by_username = User.query.filter_by(username=form.username.data).first()
        user_by_email = User.query.filter_by(email=form.email.data).first()

        if user_by_username:
            flash('이미 존재하는 사용자입니다.')
        # elif user_by_email:
        #     flash('이미 존재하는 이메일입니다.')
        else:
            # UserCreateForm에 비밀번호와 비밀번호 확인 필드가 password, password_confirm로 정의되었다고 가정합니다.
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password.data),
                        email=form.email.data
                        create_date=datetime.now()  # create date 현재시간으로 설정 
                        )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    if g.user:
        flash('이미 로그인 상태입니다.')
        return redirect(url_for('main.index'))

    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/change_password/', methods=('GET', 'POST'))
@login_required
def change_password():
    form = PasswordChangeForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = g.user
        if not check_password_hash(user.password, form.old_password.data):
            flash('기존 비밀번호가 일치하지 않습니다.', 'error')
        elif form.new_password1.data == form.old_password.data:
            flash('새 비밀번호는 기존 비밀번호와 다르게 설정해야 합니다.', 'error')
        else:
            user.password = generate_password_hash(form.new_password1.data)
            db.session.commit()
            flash('비밀번호가 성공적으로 변경되었습니다. 다시 로그인해주세요.', 'success')
            return redirect(url_for('auth.logout'))
    return render_template('auth/change_password.html', form=form)

@bp.route('/find_password/', methods=('GET', 'POST'))
def find_password():
    form = FindPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        # TODO: 여기에 이메일로 비밀번호 재설정 링크를 보내는 로직을 구현해야 합니다.
        flash('비밀번호 재설정 안내 메일을 발송했습니다. (실제 발송 기능은 구현해야 합니다.)', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/find_password.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
