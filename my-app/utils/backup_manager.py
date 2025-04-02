import pymysql
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def hacer_copia_de_seguridad():
    # Configuración desde variables de entorno
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    
    print(f"Conectando a MySQL: {db_host} - {db_user} - DB: {db_name}")  # Depuración

    # Crear el directorio de backups si no existe
    backup_dir = os.path.join(os.getcwd(), 'backups')
    os.makedirs(backup_dir, exist_ok=True)

    # Generar un nombre único para la copia de seguridad
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    nombre_archivo = f'backup_hojas_{fecha_actual}.sql'
    ruta_copia = os.path.join(backup_dir, nombre_archivo)

    print(f"Intentando crear backup en: {ruta_copia}")  # Mensaje de depuración

    try:
        # Conectar a la base de datos
        conexion = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        with conexion.cursor() as cursor:
            # Obtener todas las tablas
            cursor.execute("SHOW TABLES")
            tablas = cursor.fetchall()

            # Abrir el archivo para escribir
            with open(ruta_copia, 'w', encoding='utf-8') as archivo:
                # Para cada tabla
                for tabla in tablas:
                    nombre_tabla = tabla[0]
                    print(f"Procesando tabla: {nombre_tabla}")  # Depuración

                    # Obtener la estructura
                    cursor.execute(f"SHOW CREATE TABLE {nombre_tabla}")
                    create_stmt = cursor.fetchone()[1]
                    archivo.write(f"{create_stmt};\n\n")

                    # Obtener los datos
                    cursor.execute(f"SELECT * FROM {nombre_tabla}")
                    filas = cursor.fetchall()

                    if filas:
                        # Obtener nombres de columnas
                        cursor.execute(f"DESCRIBE {nombre_tabla}")
                        columnas = [col[0] for col in cursor.fetchall()]

                        # Escribir los inserts
                        for fila in filas:
                            valores = []
                            for valor in fila:
                                if valor is None:
                                    valores.append("NULL")
                                elif isinstance(valor, str):
                                    # Escapar correctamente las comillas
                                    valor_escapado = valor.replace("'", "''")
                                    valores.append(f"'{valor_escapado}'")
                                elif isinstance(valor, bytes):
                                    # Manejar datos binarios
                                    valores.append(f"X'{valor.hex()}'")
                                else:
                                    valores.append(str(valor))

                            archivo.write(f"INSERT INTO {nombre_tabla} ({', '.join(columnas)}) VALUES ({', '.join(valores)});\n")

                        archivo.write("\n")

        print(f"Backup creado exitosamente en: {ruta_copia}")
        print(f"Tamaño del archivo: {os.path.getsize(ruta_copia)} bytes")
        
        return {
            "nombre": nombre_archivo,
            "ruta": ruta_copia,
            "fecha_creacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "tamaño": round(os.path.getsize(ruta_copia) / (1024 * 1024), 2)  # Tamaño en MB
        }

    except pymysql.Error as e:
        print(f"Error de MySQL: {str(e)}")
        raise Exception(f"Error de MySQL: {str(e)}")

    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()

def eliminar_datos_existentes():
    try:
        # Conectar a la base de datos
        conexion = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        with conexion.cursor() as cursor:
            # Obtener todas las tablas
            cursor.execute("SHOW TABLES")
            tablas = cursor.fetchall()

            # Eliminar datos de cada tabla
            for tabla in tablas:
                cursor.execute(f"DELETE FROM {tabla[0]}")
            
            conexion.commit()
    except pymysql.Error as e:
        raise Exception(f"Error de MySQL: {e}")
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
def restaurar_backup(nombre_archivo):
    backup_dir = os.path.join(os.getcwd(), 'backups')
    ruta_backup = os.path.join(backup_dir, nombre_archivo)
    
    try:
        # Leer el contenido del archivo de backup
        with open(ruta_backup, 'r', encoding='utf-8') as archivo:
            sql_script = archivo.read()
        
        # Verificar si el contenido es válido
        if not sql_script.strip():
            return {"success": False, "message": "El archivo de backup está vacío."}
        
        # Conectar a la base de datos
        conexion = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        with conexion.cursor() as cursor:
            # 1. Desactivar temporalmente las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # 2. Obtener todas las tablas de la base de datos
            cursor.execute("SHOW TABLES")
            tablas = [tabla[0] for tabla in cursor.fetchall()]
            
            # 3. Vaciar todas las tablas existentes
            for tabla in tablas:
                try:
                    cursor.execute(f"TRUNCATE TABLE {tabla}")
                except pymysql.Error as e:
                    print(f"Error al vaciar la tabla {tabla}: {str(e)}")
            
            # 4. Ejecutar sentencias del backup
            for sentencia in sql_script.split(';'):
                sentencia = sentencia.strip()
                if sentencia:
                    try:
                        if sentencia.upper().startswith("CREATE TABLE"):
                            # Ignorar sentencias CREATE TABLE
                            continue
                        else:
                            cursor.execute(sentencia)
                    except pymysql.Error as e:
                        print(f"Error al ejecutar sentencia: {str(e)}")
            
            # 5. Reactivar las restricciones de clave foránea
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conexion.commit()
        
        return {"success": True, "message": f"Backup {nombre_archivo} restaurado con éxito."}
    
    except Exception as e:
        return {"success": False, "message": f"Error al restaurar el backup: {str(e)}"}
    
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()