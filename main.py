from flask import Flask, request, jsonify
import pandas as pd
import io

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        # Verifica si el archivo llegó correctamente
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No se encontró el archivo"}), 400
        
        file = request.files['file']
        
        # 1. LEER EL EXCEL (Línea 14 corregida)
        df = pd.read_excel(file)

        # 2. ANONIMIZACIÓN (GDPR)
        columnas_a_borrar = ['Nombre', 'Email', 'Telefono', 'Direccion', 'Cliente']
        df_limpio = df.drop(columns=[c for c in columnas_a_borrar if c in df.columns])

        # 3. CÁLCULO DE MÉTRICAS
        ventas_totales = df_limpio['Total'].sum()
        ticket_medio = df_limpio['Total'].mean()
        producto_top = df_limpio.groupby('Producto')['Cantidad'].sum().idxmax()

        # 4. RESPUESTA PARA MAKE
        return jsonify({
            "status": "success",
            "ventas_totales": float(round(ventas_totales, 2)),
            "ticket_medio": float(round(ticket_medio, 2)),
            "producto_estrella": str(producto_top)
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)
