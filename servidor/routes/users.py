from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import Bcrypt

from database import db
from models.schemas import User, Role, UserPreference, UserGameStats

bcrypt = Bcrypt()
users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@users_bp.route('/me', methods=["GET"])
@jwt_required()
def me():
    current_user_id = get_jwt_identity()

    try:
        result = db.session.query(User, Role, UserPreference, UserGameStats)\
            .join(Role, User.role_id == Role.id)\
            .outerjoin(UserPreference, User.id == UserPreference.user_id)\
            .outerjoin(UserGameStats, User.id == UserGameStats.user_id)\
            .filter(User.id == current_user_id)\
            .first()

        if not result:
            return jsonify({"error": "Not Found", "message": "Usuario no encontrado"}), 404

        user, role, preferences, stats = result

        return jsonify({
            "status": "success",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "username": user.username,
                "role_name": role.role_name,
                "preferences": {
                    "level_preference": preferences.level_preference if preferences else "NONE",
                    "daily_goal": preferences.daily_goal if preferences else 10,
                    "audio_mode": preferences.audio_mode if preferences else "FULL_AUDIO"
                },
                "stats": {
                    "current_hearts": stats.current_hearts if stats else 5,
                    "total_score": stats.total_score if stats else 0,
                    "current_streak": stats.current_streak if stats else 0,
                    "max_hearts": stats.max_hearts if stats else 5
                }
            }
        }), 200

    except Exception as e:
        print("Error en verificación:", str(e))
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error en el servidor."}), 500


@users_bp.route('/me/preferences', methods=["PUT"])
@jwt_required()
def update_preferences():
    if not request.is_json:
        return jsonify({"error": "Bad Request", "message": "Falta el JSON en la petición"}), 400

    data = request.json
    level = data.get("level_preference")
    daily_goal = data.get("daily_goal")
    audio_mode = data.get("audio_mode")

    if not level or not daily_goal or audio_mode is None:
        return jsonify({"error": "Bad Request", "message": "Todos los campos son obligatorios"}), 400

    current_user_id = get_jwt_identity()

    try:
        current_preferences = db.session.query(UserPreference).filter(UserPreference.user_id == current_user_id).first()
        if current_preferences:
            # 2. EDITAR: Asignar los nuevos valores a las propiedades del objeto
            current_preferences.level_preference = level
            current_preferences.daily_goal = daily_goal
            current_preferences.audio_mode = audio_mode
        else:
            # Opción adicional: Si no existen, las crea
            current_preferences = UserPreference(
                user_id=current_user_id,
                level_preference=level,
                daily_goal=daily_goal,
                audio_mode=audio_mode
            )
            db.session.add(current_preferences)

        # 3. Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({
            "message": "Preferencias actualizadas correctamente",
            "data": {
                "level_preference": current_preferences.level_preference,
                "daily_goal": current_preferences.daily_goal,
                "audio_mode": current_preferences.audio_mode
            }
        }), 200

    except Exception as e:
        print("Error en verificación:", str(e))
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error en el servidor."}), 500
