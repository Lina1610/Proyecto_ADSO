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
                    cursor.execute(f"SHOW CREATE TABLE `{nombre_tabla}`")
                    create_stmt = cursor.fetchone()[1]
                    archivo.write(f"{create_stmt};\n\n")

                    # Obtener los datos
                    cursor.execute(f"SELECT * FROM `{nombre_tabla}`")
                    filas = cursor.fetchall()

                    if filas:
                        # Obtener nombres de columnas
                        cursor.execute(f"DESCRIBE `{nombre_tabla}`")
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

                            archivo.write(f"INSERT INTO `{nombre_tabla}` (`{'`, `'.join(columnas)}`) VALUES ({', '.join(valores)});\n")

                        archivo.write("\n")

        print(f"Backup creado exitosamente en: {ruta_copia}")
        print(f"Tamaño del archivo: {os.path.getsize(ruta_copia)} bytes")
        
        return backup_dir, nombre_archivo  # Devuelve directorio y nombre por separado

    except pymysql.Error as e:
        print(f"Error de MySQL: {str(e)}")
        raise Exception(f"Error de MySQL: {str(e)}")

    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()