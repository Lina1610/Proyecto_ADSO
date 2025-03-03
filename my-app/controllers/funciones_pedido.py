from conexion.conexionBD import connectionBD

def obtener_productos():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para obtener solo los productos disponibles
                querySQL = "SELECT * FROM producto WHERE estado = 'Disponible' ORDER BY id DESC"
                cursor.execute(querySQL)
                productos = cursor.fetchall()
                print(f"Productos recuperados: {productos}")  # Log para depuración
                return productos
    except Exception as e:
        print(f"Error en obtener_productos: {e}")
        return []