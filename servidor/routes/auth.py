from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt
from database import db  # Importamos la DB compartida

# Inicializamos Bcrypt local y el Blueprint con su prefijo RESTful
bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')

@auth_bp.route('/login', methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Bad Request", "msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"error": "Bad Request", "msg": "Username and password required"}), 400

    user_rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    if not user_rows:
        return jsonify({"error": "Unauthorized", "msg": "Invalid username or password"}), 401
    
    user = user_rows[0]

    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Unauthorized", "msg": "Invalid username or password"}), 401
    
    # Asegúrate de usar la columna exacta de tu DB (user_id o id)
    access_token = create_access_token(identity=str(user["user_id"]))
    
    return jsonify({
        "token": access_token,
        "user": {
            "user_id": user['user_id'],
            "username": user['username'],
            "role": user['role']
        }
    }), 200


@auth_bp.route('/register', methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"error": "Bad Request", "msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    role = request.json.get("role", "user")

    if not username or not password:
        return jsonify({"error": "Bad Request", "msg": "Username and password required"}), 400

    # 1. Verificar si el usuario ya existe
    existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
    if existing_user:
        return jsonify({"error": "Conflict", "msg": "Username is already taken"}), 409

    # 2. Generar el hash seguro de la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        # 3. Insertar nuevo registro
        new_user_id = db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            username, hashed_password, role
        )
        
        # 4. Generar el JWT de una vez para dejarlo logueado
        access_token = create_access_token(identity=str(new_user_id))
        
        return jsonify({
            "status": "success",
            "msg": "User registered successfully",
            "token": access_token,
            "user": {
                "user_id": new_user_id,
                "username": username,
                "role": role
            }
        }), 201
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "msg": str(e)}), 500


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    
    user_rows = db.execute("SELECT username, role FROM users WHERE user_id = ?", current_user_id)
    if not user_rows:
        return jsonify({"error": "Unauthorized", "msg": "User no longer exists"}), 401
        
    user = user_rows[0]
    
    return jsonify({
        "status": "success",
        "logged_in_as": {
            "user_id": current_user_id,
            "username": user["username"],
            "role": user["role"]
        }
    }), 200