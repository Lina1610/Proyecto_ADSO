from flask import Blueprint, jsonify, request
from email.message import EmailMessage
import smtplib
from flask import current_app as app

soporte_bp = Blueprint('soporte', __name__)

@soporte_bp.route('/enviar-soporte', methods=['POST'])
def enviar_soporte():
    try:
        data = request.get_json()
        
        # Validación de campos requeridos
        required_fields = ['nombre', 'email', 'asunto', 'mensaje']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Faltan campos requeridos'}), 400

        # Construir mensaje
        msg = EmailMessage()
        msg['Subject'] = f"Soporte - {data['asunto']}"
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = 'juansebastian812005@gmail.com'
        msg['Reply-To'] = data['email']
        
        cuerpo_email = f"""
        Nombre: {data['nombre']}
        Email: {data['email']}
        Mensaje:
        {data['mensaje']}
        """
        msg.set_content(cuerpo_email)

        # Enviar correo
        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()  # Segundo ehlo necesario
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.send_message(msg)
            
        return jsonify({'success': True, 'message': 'Mensaje enviado exitosamente'})

    except smtplib.SMTPException as e:
        app.logger.error(f'Error SMTP: {str(e)}')
        return jsonify({'success': False, 'message': 'Error al enviar el correo'}), 500
        
    except Exception as e:
        app.logger.error(f'Error inesperado: {str(e)}')
        return jsonify({'success': False, 'message': 'Error interno'}), 500