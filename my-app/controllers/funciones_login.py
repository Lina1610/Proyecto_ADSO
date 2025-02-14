# Importandopaquetes desde flask
from flask import session, flash

# Importando conexion a BD
from conexion.conexionBD import connectionBD
# Para  validar contraseña
from werkzeug.security import check_password_hash

import re
# Para encriptar contraseña generate_password_hash
from werkzeug.security import generate_password_hash

def recibeInsertRegisterUser(tipo_documento, documento, nombre, apellido, telefono, correo, contrasena):
    print("Iniciando recibeInsertRegisterUser...")  # Depuración
    print(f"Valores recibidos: tipo_documento={tipo_documento}, documento={documento}, nombre={nombre}, apellido={apellido}, telefono={telefono}, correo={correo}, contrasena={contrasena}")  # Depuración

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
                            tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, created_user
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    valores = (
                        tipo_documento, documento, nombre, apellido, telefono, correo, nueva_password
                    )
                    print(f"Valores a insertar: {valores}")  # Depuración
                    mycursor.execute(sql, valores)
                    conexion_MySQLdb.commit()  # Asegúrate de hacer commit
                    resultado_insert = mycursor.rowcount
                    print(f"Resultado de la inserción: {resultado_insert}")  # Depuración
                    return resultado_insert
        except Exception as e:
            print(f"Error en el Insert users: {e}")  # Depuración
            return []
    else:
        print("Validación fallida, no se insertaron datos.")  # Depuración
        return False

def validarDataRegisterLogin(nombre, correo, contrasena):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM users WHERE correo = %s"
                cursor.execute(querySQL, (correo,))
                userBD = cursor.fetchone()  # Obtener la primera fila de resultados

                if userBD is not None:
                    flash('El registro no fue procesado, ya existe la cuenta.', 'error')
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
                    # La cuenta no existe y los datos del formulario son válidos, puedo realizar el Insert
                    print("Validación exitosa, procediendo a insertar.")  # Depuración
                    return True
    except Exception as e:
        print(f"Error en validarDataRegisterLogin: {e}")  # Depuración
        return []
# Validando la data del Registros para el login
def validarDataRegisterLogin(nombre, correo, contrasena):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM users WHERE correo = %s"
                cursor.execute(querySQL, (correo,))
                userBD = cursor.fetchone()  # Obtener la primera fila de resultados

                if userBD is not None:
                    flash('El registro no fue procesado, ya existe la cuenta.', 'error')
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
                    # La cuenta no existe y los datos del formulario son válidos, puedo realizar el Insert
                    print("Validación exitosa, procediendo a insertar.")  # Depuración
                    return True
    except Exception as e:
        print(f"Error en validarDataRegisterLogin: {e}")  # Depuración
        return []


def info_perfil_session():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT nombre, apellido, telefono, correo FROM users WHERE id = %s"
                cursor.execute(querySQL, (session['id'],))
                info_perfil = cursor.fetchall()
        return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session : {e}")
        return []


def procesar_update_perfil(data_form):
    # Extraer datos del diccionario data_form
    id_user = session['id']
    nombre = data_form['nombre']
    apellido = data_form['apellido']
    telefono = data_form['telefono']
    correo = data_form['correo']
    pass_actual = data_form['pass_actual']
    new_pass_user = data_form['new_pass_user']
    repetir_pass_user = data_form['repetir_pass_user']

    if not pass_actual or not correo:
        return 3

    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            querySQL = """SELECT * FROM users WHERE correo = %s LIMIT 1"""
            cursor.execute(querySQL, (correo,))
            account = cursor.fetchone()
            if account:
                if check_password_hash(account['contrasena'], pass_actual):
                    # Verificar si new_pass_user y repetir_pass_user están vacías
                    if not new_pass_user or not repetir_pass_user:
                        return updatePefilSinPass(id_user, nombre, apellido, telefono)
                    else:
                        if new_pass_user != repetir_pass_user:
                            return 2
                        else:
                            try:
                                nueva_password = generate_password_hash(new_pass_user, method='scrypt')
                                with connectionBD() as conexion_MySQLdb:
                                    with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                                        querySQL = """
                                            UPDATE users
                                            SET 
                                                nombre = %s,
                                                apellido = %s,
                                                telefono = %s,
                                                contrasena = %s
                                            WHERE id = %s
                                        """
                                        params = (nombre, apellido, telefono, nueva_password, id_user)
                                        cursor.execute(querySQL, params)
                                        conexion_MySQLdb.commit()
                                return cursor.rowcount or []
                            except Exception as e:
                                print(f"Ocurrió en procesar_update_perfil: {e}")
                                return []
            else:
                return 0

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
