
class Config:
    SECRET_KEY = "1f157c192086567f577cc2fe83a45091"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_SERVER = 'smtp.googlemail.com'