CREATE TABLE
    IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY,
        role_name VARCHAR(30) NOT NULL
    );

INSERT INTO
    roles (role_name)
VALUES
    ('admin'),
    ('teacher'),
    ('user'),
    ('guest');

CREATE TABLE
    IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        username VARCHAR(30) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES roles (role_id)
    );

CREATE TABLE
    IF NOT EXISTS daily_goals (
        daily_goal_id INTEGER PRIMARY KEY,
        minutes INTEGER NOT NULL
    );

INSERT INTO
    daily_goals (minutes)
VALUES
    ('5'),
    ('10'),
    ('20');

CREATE TABLE
    IF NOT EXISTS lsv_levels (
        lsv_level_id INTEGER PRIMARY KEY,
        level_name VARCHAR(20) NOT NULL
    );

INSERT INTO
    lsv_levels (level_name)
VALUES
    ('None'),
    ('Basic'),
    ('Intermediate');

CREATE TABLE
    IF NOT EXISTS user_preferences (
        user_id INTEGER,
        lsv_level_id INTEGER,
        daily_goal_id INTEGER,
        audio_mode VARCHAR(20) NOT NULL,
        is_simplified INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (lsv_level_id) REFERENCES lsv_levels (lsv_level_id),
        FOREIGN KEY (daily_goal_id) REFERENCES daily_goals (daily_goal_id)
    );

CREATE TABLE
    IF NOT EXISTS user_game_stats (
        user_id INTEGER,
        current_hearts INTEGER NOT NULL DEFAULT 5,
        total_score INTEGER NOT NULL DEFAULT 0,
        current_streak INTEGER NOT NULL DEFAULT 0,
        max_hearts INTEGER NOT NULL DEFAULT 5,
        last_activity_date DATE NULLABLE,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    );