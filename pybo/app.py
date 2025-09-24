from flask import Flask
from auth import auth as auth_blueprint

app = Flask(__name__)  
#app 객체를 전역으로 사용하면 프로젝트 규모가 커질수록 문제가 발생할 확률이 높아진다. 순환 참조(circular import) 오류가 대표적이다

# Register the blueprint
app.register_blueprint(auth_blueprint)

@app.route('/')
def home():
    return 'Welcome to the Home Page!'

if __name__ == '__main__':
    app.run(debug=True)