from flask_bcrypt import Bcrypt
from models.schemas import User, Role, UserPreference, UserGameStats, Level
from database import db
from datetime import date

bcrypt = Bcrypt()

ADMIN_FULL_NAME = 'Administrador'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '1234'
ADMIN_ROLE_ID = 1

def add_admin():
    admin_exists = User.query.filter_by(username='admin').first()
    if not admin_exists:
        admin_role = Role.query.filter_by(role_name='ADMIN').first()
        hashed_password = bcrypt.generate_password_hash('1234').decode('utf-8')
        
        admin_user = User(
            full_name='Administrador',
            username='admin',
            password=hashed_password,
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.flush()  # Para obtener admin_user.id

        admin_prefs = UserPreference(
            user_id=admin_user.id,
            level_preference="INTERMEDIATE",
            daily_goal=10,
            audio_mode="FULL_AUDIO"
        )
        admin_stats = UserGameStats(
            user_id=admin_user.id,
            current_hearts=5,
            total_score=0,
            current_streak=0,
            max_hearts=5,
            last_activity_day=date.today()
        )
        
        db.session.add(admin_prefs)
        db.session.add(admin_stats)
        db.session.commit()

def setup():
    add_admin()