import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecreto')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'juansebastian812005@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'jpck tqrt svct yzhl')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Imprimir las variables para comprobar que se cargaron correctamente
    print(f"SECRET_KEY: {SECRET_KEY}")
    print(f"MAIL_USERNAME: {MAIL_USERNAME}")
    print(f"MAIL_PASSWORD: {MAIL_PASSWORD}")
