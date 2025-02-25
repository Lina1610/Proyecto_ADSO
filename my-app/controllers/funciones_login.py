# Importandopaquetes desde flask
from flask import session, flash

# Importando conexion a BD
from conexion.conexionBD import connectionBD
# Para  validar contraseña
from werkzeug.security import check_password_hash

import re
# Para encriptar contraseña generate_password_hash
from werkzeug.security import generate_password_hash

def recibeInsertRegisterUser(tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, rol='cliente', estado='inactivo'):
    print("Iniciando recibeInsertRegisterUser...")  # Depuración
    print(f"Valores recibidos: tipo_documento={tipo_documento}, documento={documento}, nombre={nombre}, apellido={apellido}, telefono={telefono}, correo={correo}, contrasena={contrasena}, rol={rol}, estado={estado}")  # Depuración

    respuestaValidar = validarDataRegisterLogin(nombre, correo, contrasena)

    if respuestaValidar:
        print("Validación de datos exitosa.")  # Depuración
        nueva_password = generate_password_hash(contrasena, method='scrypt')
        try:
            with connectionBD() as conexion_MySQLdb:
                print("Conexión a la base de datos establecida correctamente.")  # Depuración
                with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                    sql = """
                        INSERT INTO users (
                            tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, rol, estado, created_user
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    valores = (
                        tipo_documento, documento, nombre, apellido, telefono, correo, nueva_password, rol, estado
                    )
                    print(f"Valores a insertar: {valores}")  # Depuración
                    mycursor.execute(sql, valores)
                    conexion_MySQLdb.commit()  # Asegúrate de hacer commit
                    resultado_insert = mycursor.rowcount
                    print(f"Resultado de la inserción: {resultado_insert}")  # Depuración
                    return resultado_insert
        except Exception as e:
            print(f"Error en el Insert users: {e}")  # Depuración
            return f"Error en la base de datos: {str(e)}"
    else:
        print("Validación fallida, no se insertaron datos.")  # Depuración
        return "Validación fallida: Verifica los datos ingresados."

def validarDataRegisterLogin(nombre, correo, contrasena):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Verificar si el correo ya está registrado
                querySQL = "SELECT * FROM users WHERE correo = %s"
                cursor.execute(querySQL, (correo,))
                userBD = cursor.fetchone()

                if userBD is not None:
                    flash('El correo ya está registrado.', 'error')
                    print("El correo ya está registrado.")  # Depuración
                    return False
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
                    flash('El correo es inválido.', 'error')
                    print("Correo inválido.")  # Depuración
                    return False
                elif not nombre or not correo or not contrasena:
                    flash('Por favor, llene los campos del formulario.', 'error')
                    print("Faltan campos obligatorios.")  # Depuración
                    return False
                else:
                    # La cuenta no existe y los datos del formulario son válidos
                    print("Validación exitosa, procediendo a insertar.")  # Depuración
                    return True
    except Exception as e:
        print(f"Error en validarDataRegisterLogin: {e}")  # Depuración
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
                info_perfil = cursor.fetchone()  # Obtener la primera fila de resultados
                return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session: {e}")
        return None


def procesar_update_perfil(data_form):
    try:
        id_user = session['id']
        nombre = data_form.get('nombre')
        apellido = data_form.get('apellido')
        telefono = data_form.get('telefono')
        pass_actual = data_form.get('pass_actual')

        if not pass_actual:
            return 3  # Contraseña actual requerida

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT contrasena FROM users WHERE id = %s", (id_user,))
                user = cursor.fetchone()

                if user and check_password_hash(user['contrasena'], pass_actual):
                    cursor.execute("""
                        UPDATE users 
                        SET nombre=%s, apellido=%s, telefono=%s 
                        WHERE id=%s
                    """, (nombre, apellido, telefono, id_user))
                    conexion_MySQLdb.commit()
                    return 1
                else:
                    return 0  # Contraseña actual incorrecta
    except Exception as e:
        print(f"Error al actualizar perfil: {e}")
        return None

def procesar_update_password(data_form):
    try:
        id_user = session['id']
        pass_actual = data_form.get('pass_actual')
        new_pass = data_form.get('new_pass_user')
        confirm_pass = data_form.get('repetir_pass_user')

        if not pass_actual:
            return 3  # Contraseña actual requerida

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT contrasena FROM users WHERE id = %s", (id_user,))
                user = cursor.fetchone()

                if user and check_password_hash(user['contrasena'], pass_actual):
                    if new_pass == confirm_pass:
                        nueva_password = generate_password_hash(new_pass, method='scrypt')
                        cursor.execute("""
                            UPDATE users 
                            SET contrasena = %s 
                            WHERE id = %s
                        """, (nueva_password, id_user))
                        conexion_MySQLdb.commit()
                        return 1
                    else:
                        return 2  # Contraseñas no coinciden
                else:
                    return 0  # Contraseña actual incorrecta
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


