import os
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No se encontró el archivo"}), 400
    
    file = request.files['file']
    try:
        # Leemos cualquier Excel
        df = pd.read_excel(file)
        
        # Limpieza RGPD/Ley 1581: Borramos columnas que suelen tener datos personales
        columnas_sensibles = ['nombre', 'apellido', 'telefono', 'correo', 'email', 'direccion', 'cedula', 'dni', 'id']
        for col in df.columns:
            if any(sensible in col.lower() for sensible in columnas_sensibles):
                df = df.drop(columns=[col])
        
        # Convertimos el contenido a un formato que la IA entiende (JSON texto)
        contenido_datos = df.to_json(orient='records')
        
        return jsonify({
            "status": "success",
            "datos_crudos": contenido_datos
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
