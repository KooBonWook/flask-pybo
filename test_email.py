import smtplib
import ssl
from email.message import EmailMessage

# 프로젝트의 config.py 파일에서 설정을 가져옵니다.
try:
    import config
except ImportError:
    print("[오류] config.py 파일을 찾을 수 없습니다. 이 스크립트를 프로젝트 루트 폴더에 저장했는지 확인하세요.")
    exit()

# --- 설정값 ---
SMTP_SERVER = config.MAIL_SERVER
SMTP_PORT = config.MAIL_PORT
SENDER_EMAIL = config.MAIL_USERNAME
SENDER_PASSWORD = config.MAIL_PASSWORD
RECEIVER_EMAIL = config.MAIL_USERNAME  # 자기 자신에게 테스트 메일 발송

# --- 이메일 내용 ---
subject = "Pybo SMTP 이메일 테스트"
body = "이 메일은 Python smtplib를 사용하여 보낸 테스트 메일입니다."

msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg.set_content(body)

context = ssl.create_default_context()

try:
    print(f"'{SMTP_SERVER}:{SMTP_PORT}' 서버에 연결을 시도합니다...")
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        print(f"'{SENDER_EMAIL}' 계정으로 로그인을 시도합니다...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        print(f"\n[성공] '{RECEIVER_EMAIL}' 주소로 테스트 이메일을 성공적으로 발송했습니다.")
        print("Gmail 받은 편지함을 확인해보세요.")
except smtplib.SMTPAuthenticationError as e:
    print("\n[실패] SMTP 인증에 실패했습니다.")
    print("config.py 파일의 MAIL_USERNAME 또는 MAIL_PASSWORD 값을 다시 확인해주세요.")
    print("Google 계정에 2단계 인증이 설정된 경우, 일반 비밀번호가 아닌 '앱 비밀번호'를 사용해야 합니다.")
    print(f"원본 오류 메시지: {e.smtp_code} {e.smtp_error.decode('utf-8')}")
except Exception as e:
    print(f"\n[실패] 이메일 발송 중 예상치 못한 오류가 발생했습니다: {e}")