from database import db
from sqlalchemy import text, CheckConstraint

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(30), nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.ForeignKey('roles.id'))

class Level(db.Model):
    __tablename__ = "levels"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level_name = db.Column(db.String(2))

class UserPreference(db.Model):
    __tablename__ = "user_preferences"
    user_id = db.Column(db.ForeignKey('users.id'), primary_key=True)
    level_preference = db.Column(db.String(20), nullable=False, server_default=text("'NONE'"))
    daily_goal = db.Column(db.Integer, nullable=False, server_default=text("10"))
    audio_mode = db.Column(db.String(20), nullable=False, server_default=text("'FULL_AUDIO'"))

    __table_args__ = (
        CheckConstraint(
            "level_preference IN ('NONE', 'BASIC', 'INTERMEDIATE')",
            name="check_level_preference"
        ),
        CheckConstraint(
            "daily_goal IN (5, 10, 20)",
            name="check_daily_goal"
        ),
        CheckConstraint(
            "audio_mode IN ('FULL_AUDIO', 'NO_VOICE', 'MUTED')",
            name="check_audio_mode"
        ),
    )

class UserGameStats(db.Model):
    __tablename__ = "user_game_stats"
    user_id = db.Column(db.ForeignKey('users.id'), primary_key=True)
    current_level_id = db.Column(db.ForeignKey('levels.id'))
    current_hearts = db.Column(db.Integer, nullable=False, server_default=text("5"))
    total_score = db.Column(db.Integer, nullable=False, server_default=text("0"))
    current_streak = db.Column(db.Integer, nullable=False, server_default=text("0"))
    max_hearts = db.Column(db.Integer, nullable=False, server_default=text("5"))
    last_activity_day = db.Column(db.Date, nullable=False)