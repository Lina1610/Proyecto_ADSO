from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from conexion.conexionBD import connectionBD
from controllers.funciones_installment import procesar_abono

router_installment = Blueprint('router_installment', __name__)
@router_installment.route('/registrar-abono', methods=['GET', 'POST'])
def viewFormAbono():
    if 'conectado' in session:
        if request.method == 'POST':
            dataForm = {
                'numero_abonos': request.form.get('numero_abonos'),
                'estado': request.form.get('estado'),
                'monto': request.form.get('monto'),
                'pedido_id': request.form.get('pedido_id')
            }

            resultado = procesar_abono(dataForm)

            if isinstance(resultado, int) and resultado > 0:
                flash('Abono registrado correctamente.', 'success')
            else:
                flash(resultado, 'error')

            return redirect(url_for('router_installment.viewFormAbono'))

        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT p.id AS pedido_id, u.nombre AS nombre_usuario
                    FROM pedido p
                    JOIN users u ON p.users_id = u.id
                """)
                pedidos = cursor.fetchall()

        return render_template('public/abono/registro_abono.html', pedidos=pedidos)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
