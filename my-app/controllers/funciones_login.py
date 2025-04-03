from flask import session, flash
from conexion.conexionBD import connectionBD
from werkzeug.security import check_password_hash, generate_password_hash
import re

def recibeInsertRegisterUser(tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, rol='cliente', estado='inactivo'):
    print("Iniciando recibeInsertRegisterUser...")
    print(f"Valores recibidos: tipo_documento={tipo_documento}, documento={documento}, nombre={nombre}, apellido={apellido}, telefono={telefono}, correo={correo}, contrasena={contrasena}, rol={rol}, estado={estado}")

    respuestaValidar = validarDataRegisterLogin(nombre, correo, contrasena)

    if respuestaValidar:
        print("Validación de datos exitosa.")
        nueva_password = generate_password_hash(contrasena, method='scrypt')
        try:
            with connectionBD() as conexion_MySQLdb:
                print("Conexión a la base de datos establecida correctamente.")
                with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                    sql = """
                        INSERT INTO users (
                            tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, rol, estado, created_user
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    valores = (
                        tipo_documento, documento, nombre, apellido, telefono, correo, nueva_password, rol, estado
                    )
                    print(f"Valores a insertar: {valores}")
                    mycursor.execute(sql, valores)
                    conexion_MySQLdb.commit()
                    resultado_insert = mycursor.rowcount
                    print(f"Resultado de la inserción: {resultado_insert}")
                    return resultado_insert
        except Exception as e:
            print(f"Error en el Insert users: {e}")
            return f"Error en la base de datos: {str(e)}"
    else:
        print("Validación fallida, no se insertaron datos.")
        return "Validación fallida: Verifica los datos ingresados."

def validarDataRegisterLogin(nombre, correo, contrasena):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM users WHERE correo = %s"
                cursor.execute(querySQL, (correo,))
                userBD = cursor.fetchone()

                if userBD is not None:
                    flash('El correo ya está registrado.', 'error')
                    print("El correo ya está registrado.")
                    return False
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
                    flash('El correo es inválido.', 'error')
                    print("Correo inválido.")
                    return False
                elif not nombre or not correo or not contrasena:
                    flash('Por favor, llene los campos del formulario.', 'error')
                    print("Faltan campos obligatorios.")
                    return False
                else:
                    print("Validación exitosa, procediendo a insertar.")
                    return True
    except Exception as e:
        print(f"Error en validarDataRegisterLogin: {e}")
        return False

def info_perfil_session():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT tipo_documento, documento, nombre, apellido, telefono, correo, rol, estado 
                    FROM users 
                    WHERE id = %s
                """
                cursor.execute(querySQL, (session['id'],))
                info_perfil = cursor.fetchone()
                return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session: {e}")
        return None

def procesar_update_perfil(data_form):
    try:
        id_user = session['id']
        pass_actual = data_form.get('pass_actual', '').strip()
        nombre = data_form.get('nombre', '').strip()
        apellido = data_form.get('apellido', '').strip()
        telefono = data_form.get('telefono', '').strip()

        if not pass_actual:
            return 3  # Contraseña actual obligatoria

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT contrasena FROM users WHERE id = %s", (id_user,))
                user = cursor.fetchone()

                if not user or not check_password_hash(user['contrasena'], pass_actual):
                    return 0  # Contraseña actual incorrecta

                # Preparar la consulta, permitiendo campos vacíos
                update_query = "UPDATE users SET "
                params = []
                if nombre:
                    update_query += "nombre = %s, "
                    params.append(nombre)
                if apellido:
                    update_query += "apellido = %s, "
                    params.append(apellido)
                if telefono:
                    update_query += "telefono = %s, "
                    params.append(telefono)
                update_query = update_query.rstrip(", ") + " WHERE id = %s"
                params.append(id_user)

                cursor.execute(update_query, tuple(params))
                conexion_MySQLdb.commit()
                return 1  # Éxito

    except Exception as e:
        print(f"Error al actualizar perfil: {e}")
        return -1

def procesar_update_password(data_form):
    try:
        id_user = session.get('id')
        if not id_user:
            return None  # Sesión inválida

        pass_actual = data_form.get('pass_actual')
        new_pass = data_form.get('new_pass_user')
        confirm_pass = data_form.get('repetir_pass_user')

        # Validar campos obligatorios
        if not pass_actual or not new_pass or not confirm_pass:
            return 3

        # Validar longitud
        if len(new_pass) < 8 or len(new_pass) > 20:
            return 4

        # Validar complejidad
        tiene_letras = any(c.isalpha() for c in new_pass)
        tiene_numeros = any(c.isdigit() for c in new_pass)
        tiene_especiales = any(c in '@$!%*?&' for c in new_pass)
        tipos_presentes = sum([tiene_letras, tiene_numeros, tiene_especiales])

        if tipos_presentes < 2:
            return 5
        if not tiene_letras and tiene_numeros and not tiene_especiales:
            return 6
        if tiene_letras and not tiene_numeros and not tiene_especiales:
            return 7

        # Validar coincidencia
        if new_pass != confirm_pass:
            return 2

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT contrasena FROM users WHERE id = %s", (id_user,))
                user = cursor.fetchone()

                if not user:
                    return 0  # Usuario no encontrado

                # Validar contraseña actual y que no sea igual a la nueva
                if check_password_hash(user['contrasena'], pass_actual):
                    if new_pass == pass_actual:
                        return 8
                    nueva_password = generate_password_hash(new_pass, method='scrypt')
                    cursor.execute("""
                        UPDATE users 
                        SET contrasena = %s 
                        WHERE id = %s
                    """, (nueva_password, id_user))
                    conexion_MySQLdb.commit()
                    return 1
                else:
                    return 0
    except Exception as e:
        print(f"Error al actualizar contraseña: {e}")
        return None

def updatePefilSinPass(id_user, nombre, apellido, telefono):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    UPDATE users
                    SET 
                        nombre = %s,
                        apellido = %s,
                        telefono = %s
                    WHERE id = %s
                """
                params = (nombre, apellido, telefono, id_user)
                cursor.execute(querySQL, params)
                conexion_MySQLdb.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Ocurrió un error en la funcion updatePefilSinPass: {e}")
        return []

def dataLoginSesion():
    inforLogin = {
        "id": session['id'],
        "nombre": session['nombre'],
        "apellido": session['apellido'],
        "telefono": session['telefono'],
        "correo": session['correo'],
        "documento": session['documento']
    }
    return inforLogin
