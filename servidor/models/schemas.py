from database import db
# 1. Importas las cosas directamente de sqlalchemy:
from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, text, event

# 2. Tu código queda súper limpio y con AUTOCOMPLETADO TOTAL:
class Role(db.Model):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(30), nullable=False)

@event.listens_for(Role.__table__, 'after_create')
def insert_initial_roles(target, connection, **kw):
    connection.execute(
        target.insert(),
        [
            {'role_name': 'ADMIN'},
            {'role_name': 'TEACHER'},
            {'role_name': 'USER'},
            {'role_name': 'GUEST'}
        ]
    )

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(ForeignKey('roles.id'))

class Level(db.Model):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    level_name = Column(String(2))

@event.listens_for(Level.__table__, 'after_create')
def insert_initial_levels(target, connection, **kw):
    connection.execute(
        target.insert(),
        [
            {'level_name': 'A1'},
            {'level_name': 'A2'},
            {'level_name': 'B1'},
            {'level_name': 'B2'},
            {'level_name': 'C1'},
            {'level_name': 'C2'}
        ]
    )

class UserPreference(db.Model):
    __tablename__ = "user_preferences"
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    level_preference = Column(String(20), nullable=False, server_default=text("'NONE'"))
    daily_goal = Column(Integer, nullable=False, server_default=text("10"))
    audio_mode = Column(String(20), nullable=False, server_default=text("'FULL_AUDIO'"))

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
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    current_level_id = Column(ForeignKey('levels.id'))
    current_hearts = Column(Integer, nullable=False, server_default=text("5"))
    total_score = Column(Integer, nullable=False, server_default=text("0"))
    current_streak = Column(Integer, nullable=False, server_default=text("0"))
    max_hearts = Column(Integer, nullable=False, server_default=text("5"))
    last_activity_day = Column(Date, nullable=False)

class Section(db.Model):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    level_id = Column(ForeignKey('levels.id'))

class Unit(db.Model):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(ForeignKey('sections.id'))
    title = Column(String(100), nullable=False)
    color_scheme = Column(String(100), nullable=False)

class Node(db.Model):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    unit_id = Column(ForeignKey('units.id'))
    position = Column(Integer, nullable=False)


