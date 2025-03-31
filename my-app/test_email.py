from flask_mail import Mail, Message
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

with app.app_context():
    msg = Message("Prueba Flask-Mail", sender=app.config["MAIL_USERNAME"], recipients=["juansebastian812005@gmail.com"])
    msg.body = "Este es un mensaje de prueba."
    try:
        mail.send(msg)
        print("✅ Correo enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
