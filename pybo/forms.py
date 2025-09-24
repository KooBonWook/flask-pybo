from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo,Email


class UserCreateForm(FlaskForm):
    """
    사용자 등록을 위한 폼
    """
    username = StringField('사용자이름', validators=[
        DataRequired(message='사용자이름은 필수입니다.'),
        Length(min=3, max=25, message='사용자이름은 3자 이상 25자 이하로 입력해주세요.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호는 필수입니다.'),
        EqualTo('password_confirm', '비밀번호가 일치하지 않습니다.')
    ])
    password_confirm = PasswordField('비밀번호 확인', validators=[
        DataRequired(message='비밀번호 확인은 필수입니다.')
    ])
    email = StringField('이메일', validators=[
        DataRequired(message='이메일은 필수입니다.'),
        Email(message='올바른 이메일 형식이 아닙니다.')
    ])


class UserLoginForm(FlaskForm):
    """
    사용자 로그인을 위한 폼
    """
    username = StringField('사용자이름', validators=[
        DataRequired(message='사용자이름은 필수입니다.')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호는 필수입니다.')
    ])

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('기존 비밀번호', validators=[DataRequired()])
    new_password1 = PasswordField('새 비밀번호', validators=[
        DataRequired(),
        EqualTo('new_password2', '비밀번호가 일치하지 않습니다.'),
        Length(min=4, message='비밀번호는 4자 이상이어야 합니다.')
    ])
    new_password2 = PasswordField('새 비밀번호 확인', validators=[
        DataRequired(message="비밀번호 확인은 필수입니다.")
    ])

class FindPasswordForm(FlaskForm):
    email = StringField('이메일', validators=[
        DataRequired(message='이메일은 필수입니다.'),
        Email(message='올바른 이메일 형식이 아닙니다.')
    ])

class PasswordResetForm(FlaskForm):
    new_password1 = PasswordField('새 비밀번호', validators=[
        DataRequired(message='비밀번호는 필수입니다.'),
        EqualTo('new_password2', '비밀번호가 일치하지 않습니다.'),
        Length(min=4, message='비밀번호는 4자 이상이어야 합니다.')
    ])
    new_password2 = PasswordField('새 비밀번호 확인', validators=[
        DataRequired(message='비밀번호 확인은 필수입니다.')
    ])


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력항목입니다. ')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력항목입니다. ')])
    category = SelectField('카테고리', coerce=int, validators=[DataRequired('카테고리는 필수입력항목입니다. ')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category  # 순환 참조 방지를 위해 함수 내에서 import
        self.category.choices = [(c.id, c.name) for c in Category.query.order_by('name')]

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력항목입니다. ')])

class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])