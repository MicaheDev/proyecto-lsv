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
        return jsonify({"error": "Bad Request", "message": "Falta el JSON en la petición"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"error": "Bad Request", "message": "Usuario y contraseña son obligatorios"}), 400

    try:
        # 1. Buscar al usuario por su username (Suelto, estilo CS50)
        user_rows = db.execute("""SELECT u.user_id, u.username, u.password, u.full_name, r.role_name,
                      s.current_level, s.current_hearts, s.max_hearts, s.total_score, s.current_streak
               FROM users u
               LEFT JOIN roles r ON u.role_id = r.role_id 
               LEFT JOIN user_game_stats s ON u.user_id = s.user_id
               WHERE u.username = ?""", username)

        if not user_rows:
            return jsonify({"error": "Unauthorized", "message": "Usuario o contraseña incorrectos"}), 401
        
        user = user_rows[0]

        # 2. Verificar si la contraseña coincide con el hash
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"error": "Unauthorized", "message": "Usuario o contraseña incorrectos"}), 401
        
        user_id = user["user_id"]
        # 3. Generar el token de acceso JWT
        access_token = create_access_token(identity=str(user_id))
        
        # 4. Responder con los datos correctos de la tabla
        return jsonify({
            "status": "success",
            "message": "¡Inicio de sesión exitoso!",
            "token": access_token,
            "user": {
                "user_id": user['user_id'],   
                "username": user['username'],    
                "full_name": user['full_name'],
                "role": user["role_name"],
                "stats": {
                    "current_level": user["current_level"],
                    "current_hearts": user.get('current_hearts', 5),
                    "max_hearts": user.get('max_hearts', 5),
                    "total_score": user.get('total_score', 0),
                    "current_streak": user.get('current_streak', 0)
                }
            }
        }), 200

    except Exception as e:
        print("Error en login:", str(e)) # Para que veas el desglose exacto en la consola si algo más falla
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

    # Validación básica en el servidor
    if not full_name or not username or not password:
        return jsonify({"error": "Bad Request", "message": "Todos los campos son obligatorios"}), 400

    # 1. Verificar si el usuario ya existe
    # Nota: Si tu objeto 'db' devuelve una lista, verificamos si tiene elementos
    existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
    if existing_user:
        return jsonify({"error": "Conflict", "message": "El nombre de usuario ya está en uso"}), 409

    # 2. Generar el hash seguro de la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:

       # El rol por defecto ahora es 3 ('USER' en tu tabla roles)
        role_id = 3 

        # ◄ .upper() convierte 'none' o 'basic' a 'NONE' o 'BASIC' para pasar el CHECK
        raw_level = preferences.get("level_preference", "NONE")
        level_pref = str(raw_level).upper() if raw_level else "NONE"
        
        # ◄ .upper() convierte 'full_audio' o 'no_voice' a 'FULL_AUDIO' o 'NO_VOICE'
        raw_audio = preferences.get("audio_mode", "FULL_AUDIO")
        audio_mode = str(raw_audio).upper() if raw_audio else "FULL_AUDIO"

        # Aseguramos que daily_goal sea entero y esté en los permitidos (5, 10, 20)
        try:
            daily_goal = int(preferences.get("daily_goal", 10))
            if daily_goal not in [5, 10, 20]:
                daily_goal = 10
        except (ValueError, TypeError):
            daily_goal = 10

        is_simplified = 1 if preferences.get("is_simplified") else 0

        # 3. Insertar el usuario en la tabla 'users'
        # Nota: Asegúrate de que tu wrapper de BD devuelva el ID del registro insertado (lastrowid)
        new_user_id = db.execute(
            "INSERT INTO users (full_name, username, password, role_id) VALUES (?, ?, ?, ?)",
            full_name, 
            username, 
            hashed_password, 
            role_id
        )

        # 4. Insertar las preferencias vinculadas al nuevo user_id
        db.execute(
            "INSERT INTO user_preferences (user_id, level_preference, daily_goal, audio_mode, is_simplified) VALUES (?, ?, ?, ?, ?)",
            new_user_id, 
            level_pref, 
            daily_goal, 
            audio_mode, 
            is_simplified
        )

        # 5. Inicializar las estadísticas de juego (corazones, racha, puntaje) para el niño/usuario
        db.execute(
            """INSERT INTO user_game_stats (user_id, current_hearts, total_score, current_streak, max_hearts, last_activity_date) 
               VALUES (?, 5, 0, 0, 5, CURRENT_DATE)""",
            new_user_id
        )
        # 6. Generar el JWT para dejarlo logueado de una vez
        access_token = create_access_token(identity=str(new_user_id))
        
        return jsonify({
            "status": "success",
            "message": "¡Usuario registrado con éxito!",
            "token": access_token,
            "user": {
                "user_id": new_user_id,
                "username": username,
                "full_name": full_name,
                "role": "USER",
                "stats": {
                    "current_level": "A1",
                    "current_hearts": 5,
                    "max_hearts": 5,
                    "total_score": 0,
                    "current_streak": 0
                }
            }
        }), 201

    except Exception as e:
        print("Error en registro:", str(e)) # Para que lo veas en la consola de Flask
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error al guardar en la base de datos."}), 500

@auth_bp.route("/verify", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    
    try:
        user_rows = db.execute("SELECT username, role_id FROM users WHERE user_id = ?", current_user_id)
        if not user_rows:
            return jsonify({"error": "Unauthorized", "msg": "User no longer exists"}), 401
            
        user = user_rows[0]
        
        return jsonify({
            "status": "success",
            "message": "¡Inicio de sesión exitoso!",
            "user": {
                "user_id": current_user_id,
                "username": user["username"],
                "role_id": user["role_id"]
            }
        }), 200
    
    except Exception as e:
        print("Error en registro:", str(e)) # Para que lo veas en la consola de Flask
        return jsonify({"error": "Internal Server Error", "message": "Ocurrió un error al guardar en la base de datos."}), 500
