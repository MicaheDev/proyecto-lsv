from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt

from database import db
from models.schemas import User, Role, UserPreference, UserGameStats

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1')

@auth_bp.route('/login', methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Bad Request", "message": "Falta el JSON en la petición"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"error": "Bad Request", "message": "Usuario y contraseña son obligatorios"}), 400

    try:
        # 1. Buscar al usuario usando el ORM de Flask-SQLAlchemy
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"error": "Unauthorized", "message": "Usuario o contraseña incorrectos"}), 401

        # 2. Verificar la contraseña
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "Unauthorized", "message": "Usuario o contraseña incorrectos"}), 401

        # 3. Obtener relaciones (Rol y Estadísticas de juego)
        role = Role.query.get(user.role_id)
        stats = UserGameStats.query.filter_by(user_id=user.id).first()

        # 4. Generar el JWT
        access_token = create_access_token(identity=str(user.id))

        # 5. Responder con la estructura esperada por tu frontend
        return jsonify({
            "status": "success",
            "message": "¡Inicio de sesión exitoso!",
            "token": access_token,
            "user": {
                "user_id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "role": role.role_name if role else "USER",
                "stats": {
                    "current_level": stats.current_level_id if stats else None,
                    "current_hearts": stats.current_hearts if stats else 5,
                    "max_hearts": stats.max_hearts if stats else 5,
                    "total_score": stats.total_score if stats else 0,
                    "current_streak": stats.current_streak if stats else 0
                }
            }
        }), 200

    except Exception as e:
        print("Error en login:", str(e))
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error en el servidor."}), 500


@auth_bp.route('/register', methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"error": "Bad Request", "message": "Falta el JSON en la petición"}), 400

    data = request.json
    full_name = data.get("full_name")
    username = data.get("username")
    password = data.get("password")
    preferences = data.get("preferences", {})

    if not full_name or not username or not password:
        return jsonify({"error": "Bad Request", "message": "Todos los campos son obligatorios"}), 400

    # 1. Comprobar si el usuario ya existe
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Conflict", "message": "El nombre de usuario ya está en uso"}), 409

    # 2. Generar el hash de la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        # Obtener el rol de usuario por defecto ("USER")
        user_role = Role.query.filter_by(role_name="USER").first()
        role_id = user_role.id if user_role else 3

        # Formatear preferencias
        raw_level = preferences.get("level_preference", "NONE")
        level_pref = str(raw_level).upper() if raw_level else "NONE"

        raw_audio = preferences.get("audio_mode", "FULL_AUDIO")
        audio_mode = str(raw_audio).upper() if raw_audio else "FULL_AUDIO"

        try:
            daily_goal = int(preferences.get("daily_goal", 10))
            if daily_goal not in [5, 10, 20]:
                daily_goal = 10
        except (ValueError, TypeError):
            daily_goal = 10

        # 3. Crear nuevo objeto Usuario
        new_user = User(
            full_name=full_name,
            username=username,
            password=hashed_password,
            role_id=role_id
        )
        db.session.add(new_user)
        db.session.flush()  # Genera el new_user.id para referenciarlo

        # 4. Crear registro de Preferencias
        new_preferences = UserPreference(
            user_id=new_user.id,
            level_preference=level_pref,
            daily_goal=daily_goal,
            audio_mode=audio_mode
        )

        # 5. Inicializar Estadísticas de Juego
        new_stats = UserGameStats(
            user_id=new_user.id,
            current_hearts=5,
            total_score=0,
            current_streak=0,
            max_hearts=5,
            last_activity_day=date.today()
        )

        db.session.add(new_preferences)
        db.session.add(new_stats)
        
        # Confirmar todos los cambios en la BD de una sola vez
        db.session.commit()

        # 6. Generar JWT
        access_token = create_access_token(identity=str(new_user.id))

        return jsonify({
            "status": "success",
            "message": "¡Usuario registrado con éxito!",
            "token": access_token,
            "user": {
                "user_id": new_user.id,
                "username": username,
                "full_name": full_name,
                "role": "USER",
                "stats": {
                    "current_level": None,
                    "current_hearts": 5,
                    "max_hearts": 5,
                    "total_score": 0,
                    "current_streak": 0
                }
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # Revierte los cambios si ocurre un error inesperado
        print("Error en registro:", str(e))
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error al guardar en la base de datos."}), 500


@auth_bp.route("/verify", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()

    try:
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "Unauthorized", "msg": "El usuario ya no existe"}), 401

        return jsonify({
            "status": "success",
            "message": "Token válido",
            "user": {
                "user_id": user.id,
                "username": user.username,
                "role_id": user.role_id
            }
        }), 200

    except Exception as e:
        print("Error en verificación:", str(e))
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error en el servidor."}), 500