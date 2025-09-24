import os

BASE_DIR = os.path.dirname(__file__)

# SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS는 SQLAlchemy의 이벤트를 처리하는 옵션이고, 
# 이 옵션은 파이보에 필요하지 않으므로 False로 비활성화
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLALCHEMY_DATABASE_URI 설정에 의해 SQLite 데이터베이스가 사용되고 데이터베이스 파일은 프로젝트 홈 디렉터리 바로 밑에 pybo.db 파일로 저장됩니다.
# SECRET_KEY는 CSRF(Cross-site request forgery)와 같은 공격을 방지하는 데 사용됩니다. 개발 환경에서는 'dev'와 같은 간단한 문자열을 사용하지만, 운영 환경에서는 복잡하고 예측 불가능한 값을 사용해야 합니다.
SECRET_KEY = "dev"

# Flask-Mail 설정 (이메일 전송을 위한 설정)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS=True
MAIL_USERNAME = 'bwkoo1263@gmail.com'

MAIL_PASSWORD = 'lqsxlqpucclajgpa'
MAIL_DEFAULT_SENDER = 'bwkoo1263@gmail.com'