from database import db
# 1. Importas las cosas directamente de sqlalchemy:
from sqlalchemy import Column, Integer, LargeBinary,String, Date, ForeignKey, CheckConstraint, text, event

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

class Lesson(db.Model):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    node_id = Column(ForeignKey('nodes.id'))
    required_exp = Column(Integer, nullable=False)

class ChallengeType(db.Model):
    __tablename__ = "challenge_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(100), nullable=False)

@event.listens_for(ChallengeType.__table__, 'after_create')
def insert_initial_challenge_types(target, connection, **kw):
    connection.execute(
        target.insert(),
        [
            {'type_name': 'DEMO'},
            {'type_name': 'QUIZ_MULTIPLE'},
            {'type_name': 'REVERSE_QUIZ'},
            {'type_name': 'MATCHING'},
            {'type_name': 'CAM_VERIFY'},
            {'type_name': 'FREE_PRACTICE'},
        ]
    )

class Challenge(db.Model):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(ForeignKey('lessons.id'))
    challenge_type_id = Column(ForeignKey('challenge_types.id'))
    question = Column(String(100), nullable=False)
    sign_id = Column(ForeignKey('signs.id'))

class Sign(db.Model):
    __tablename__ = "signs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    meaning = Column(String(100), nullable=False)
    category_id = Column(ForeignKey('categories.id'))
    resource_id = Column(ForeignKey('resources.id'))

class Category(db.Model):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False)

class ResourceType(db.Model):
    __tablename__ = "resource_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(100), nullable=False) 

@event.listens_for(ResourceType.__table__, 'after_create')
def insert_initial_resource_types(target, connection, **kw):
    connection.execute(
        target.insert(),
        [
            {'type_name': 'VIDEO'},
            {'type_name': 'STATIC_IMAGE'},
            {'type_name': '3D'},
        ]
    )

class Resource(db.Model):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    resource_type_id = Column(ForeignKey('resource_types.id'))
    content = Column(LargeBinary, nullable=True)


