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


@users_bp.route('/me/preferences', methods=["POST"])
@jwt_required()
def update_preferences():
    current_user_id = get_jwt_identity()
    try:

        print("hello")
        

    except Exception as e:
        print("Error en verificación:", str(e))
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error en el servidor."}), 500
