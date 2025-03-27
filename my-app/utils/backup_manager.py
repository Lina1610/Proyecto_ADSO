import pymysql
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def hacer_copia_de_seguridad():
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    
    print(f"Conectando a MySQL: {db_host} - {db_user} - DB: {db_name}")
    backup_dir = os.path.join(os.getcwd(), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    nombre_archivo = f'backup_hojas_{fecha_actual}.sql'
    ruta_copia = os.path.join(backup_dir, nombre_archivo)
    print(f"Intentando crear backup en: {ruta_copia}")

    try:
        conexion = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
        with conexion.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tablas = cursor.fetchall()
            with open(ruta_copia, 'w', encoding='utf-8') as archivo:
                for tabla in tablas:
                    nombre_tabla = tabla[0]
                    print(f"Procesando tabla: {nombre_tabla}")
                    cursor.execute(f"SHOW CREATE TABLE `{nombre_tabla}`")
                    create_stmt = cursor.fetchone()[1]
                    archivo.write(f"{create_stmt};\n\n")
                    cursor.execute(f"SELECT * FROM `{nombre_tabla}`")
                    filas = cursor.fetchall()
                    if filas:
                        cursor.execute(f"DESCRIBE `{nombre_tabla}`")
                        columnas = [col[0] for col in cursor.fetchall()]
                        for fila in filas:
                            valores = []
                            for valor in fila:
                                if valor is None:
                                    valores.append("NULL")
                                elif isinstance(valor, str):
                                    valor_escapado = valor.replace("'", "''")
                                    valores.append(f"'{valor_escapado}'")
                                elif isinstance(valor, bytes):
                                    valores.append(f"X'{valor.hex()}'")
                                elif isinstance(valor, datetime):
                                    valores.append(f"'{valor.strftime('%Y-%m-%d %H:%M:%S')}'")
                                else:
                                    valores.append(str(valor))
                            archivo.write(f"INSERT INTO `{nombre_tabla}` (`{'`, `'.join(columnas)}`) VALUES ({', '.join(valores)});\n")
                        archivo.write("\n")
        print(f"Backup creado exitosamente en: {ruta_copia}")
        print(f"Tamaño del archivo: {os.path.getsize(ruta_copia)} bytes")
        return {
            "nombre": nombre_archivo,
            "ruta": ruta_copia,
            "fecha_creacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "tamaño": round(os.path.getsize(ruta_copia) / (1024 * 1024), 2)
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
def ejecutar_restauracion(ruta_backup):
    try:
        with open(ruta_backup, 'r', encoding='utf-8') as archivo:
            sql_script = archivo.read()
        
        if not sql_script.strip():
            return {"success": False, "message": "El archivo de backup está vacío."}
        
        conexion = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        
        with conexion.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            for sentencia in sql_script.split(';'):
                sentencia = sentencia.strip()
                if not sentencia:
                    continue
                
                print(f"Procesando: {sentencia}")  # Depuración
                try:
                    if sentencia.upper().startswith("CREATE TABLE"):
                        print("Ignorando CREATE TABLE")
                        continue
                    elif sentencia.upper().startswith("INSERT INTO"):
                        # Usar REPLACE para restaurar datos eliminados
                        sentencia_modificada = sentencia.replace("INSERT INTO", "REPLACE INTO")
                        cursor.execute(sentencia_modificada)
                        print(f"Ejecutado: {sentencia_modificada}")
                    else:
                        print(f"Ignorado (no es INSERT ni CREATE): {sentencia}")
                except pymysql.Error as e:
                    print(f"Error al ejecutar: {sentencia[:100]}... - {str(e)}")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            conexion.commit()
        
        return {"success": True, "message": "Backup restaurado completamente. Todos los datos eliminados fueron recuperados."}
    
    except Exception as e:
        return {"success": False, "message": f"Error crítico al restaurar: {str(e)}"}
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()