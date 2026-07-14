from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

# Setup JWT
app.config["JWT_SECRET_KEY"] = "Proyecto-LSV"  # ¡Cambia esto en producción!
jwt = JWTManager(app)

# REGISTRO DE BLUEPRINTS
# Al registrarlo aquí, todas las rutas de auth.py heredarán el /api/v1 automáticamente
app.register_blueprint(auth_bp)

@app.route("/")
def hello_world():
    return jsonify({"message": "PLSV Core Server Running Successfully"}), 200


if __name__ == "__main__":
    # host='0.0.0.0' se mantiene firme para tus pruebas con la cámara en Android
    app.run(host='0.0.0.0', port=5000)