from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from database import db
from setup import setup

from routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

# Configuración de la Base de Datos (ejemplo con SQLite)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plsv.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Setup JWT
app.config["JWT_SECRET_KEY"] = "Proyecto-LSV"  # ¡Cambia esto en producción!
jwt = JWTManager(app)

# Inicializar Flask-SQLAlchemy
db.init_app(app)

# Crear tablas y ejecutar setup dentro del Contexto de Aplicación de Flask
with app.app_context():
    db.create_all()  # Crea todas las tablas automáticamente
    setup()          # Llama a tu función para insertar roles y admin
    
# REGISTRO DE BLUEPRINTS
# Al registrarlo aquí, todas las rutas de auth.py heredarán el /api/v1 automáticamente
app.register_blueprint(auth_bp)

@app.route("/")
def hello_world():
    return jsonify({"message": "PLSV Core Server Running Successfully"}), 200


if __name__ == "__main__":
    # host='0.0.0.0' se mantiene firme para tus pruebas con la cámara en Android
    app.run(host='0.0.0.0', port=5000)