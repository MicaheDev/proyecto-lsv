from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>¡Hola! El backend de mi proyecto LSV está funcionando.</p>"

@app.route('/datos-lsv')
def obtener_datos():
    conn = sqlite3.connect('lsv.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Ejemplo: trayendo las señas registradas
    cursor.execute("SELECT * FROM señas") 
    filas = cursor.fetchall()
    
    # Convertimos a lista de diccionarios para que Vite lo entienda como JSON
    resultado = [dict(f) for f in filas]
    
    conn.close()
    return jsonify(resultado)


if __name__ == "__main__":
    # Importante: host='0.0.0.0' permite que se conecte con el navegador de Android
    app.run(host='0.0.0.0', port=5000, debug=True)
