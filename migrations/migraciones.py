# migrations/migraciones.py
from conexion.conexionBD import connectionBD

class MigradorEntregas:
    @staticmethod
    def migrar_users_id():
        """Migra users_id en entregas que no lo tienen asignado"""
        try:
            with connectionBD() as conexion_MySQLdb:
                with conexion_MySQLdb.cursor() as cursor:
                    # Actualizar entregas presenciales sin users_id
                    cursor.execute("""
                        UPDATE entrega e 
                        JOIN pedido p ON e.id = p.entrega_id 
                        SET e.users_id = p.users_id 
                        WHERE e.tipo = 'Presencial' AND e.users_id IS NULL
                    """)
                    presenciales = cursor.rowcount
                    
                    # Actualizar entregas a domicilio sin users_id
                    cursor.execute("""
                        UPDATE entrega e 
                        JOIN direccion d ON e.direccion_id = d.id 
                        SET e.users_id = d.users_id 
                        WHERE e.tipo = 'Domicilio' AND e.users_id IS NULL
                    """)
                    domicilio = cursor.rowcount
                    
                    conexion_MySQLdb.commit()
                    return presenciales + domicilio
        except Exception as e:
            print(f"Error en MigradorEntregas.migrar_users_id: {e}")
            if 'conexion_MySQLdb' in locals():
                conexion_MySQLdb.rollback()
            return None