from conexion.conexionBD import connectionBD
from werkzeug.security import generate_password_hash

def crear_super_admin():
    with connectionBD() as conexion:
        cursor = conexion.cursor()

        # Datos del superadmin
        tipo_documento = 'Cedula ciudadania'
        documento = '237004967'
        nombre = 'jojas'
        apellido = 'Admin'
        telefono = '3000000000'
        correo = 'juansebastian81200@gmail.com'
        contrasena = generate_password_hash('sebastian2005', method='scrypt')
        rol = 'superadmin'
        estado = 'activo'

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM users WHERE documento = %s", (documento,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            print("⚠️ El usuario superadmin ya existe en la base de datos.")
        else:
            # Insertar el superadmin
            sql = """INSERT INTO users (tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, rol, estado)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (tipo_documento, documento, nombre, apellido, telefono, correo, contrasena, rol, estado)

            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Superadmin creado exitosamente.")

# Ejecutar la función
crear_super_admin()
