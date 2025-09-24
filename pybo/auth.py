from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic here (e.g., form handling)
    return render_template('register.html')

@auth.route('/login')
def login():
    return 'Login Page'

# Example of using url_for correctly
@auth.route('/some-other-page')
def some_other_page():
    # Redirecting to the register page using url_for
    return redirect(url_for('auth.register'))