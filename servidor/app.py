from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>¡Hola! El backend de mi proyecto LSV está funcionando.</p>"

if __name__ == "__main__":
    # Importante: host='0.0.0.0' permite que se conecte con el navegador de Android
    app.run(host='0.0.0.0', port=5000, debug=True)
