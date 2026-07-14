from flask_bcrypt import Bcrypt
from database import db  # Importamos la DB compartida

bcrypt = Bcrypt()

full_name = 'Administrador'
username = 'admin'
password = '1234'
role_id = 1
level_pref = "INTERMEDIATE"
audio_mode = "FULL_AUDIO"
daily_goal = int(10)
is_simplified = int(0)


def setup():
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user_id = db.execute("INSERT OR IGNORE INTO users (full_name, username, password, role_id) VALUES (?, ?, ?, ?)", full_name, username, hashed_password, role_id)
    if new_user_id:
        db.execute(
            "INSERT OR IGNORE INTO user_preferences (user_id, level_preference, daily_goal, audio_mode, is_simplified) VALUES (?, ?, ?, ?, ?)",
            new_user_id, 
            level_pref, 
            daily_goal, 
            audio_mode, 
            is_simplified
        )
        db.execute(
            """INSERT OR IGNORE  INTO user_game_stats (user_id, current_hearts, total_score, current_streak, max_hearts, last_activity_date) 
               VALUES (?, 5, 0, 0, 5, CURRENT_DATE)""",
            new_user_id
        )
