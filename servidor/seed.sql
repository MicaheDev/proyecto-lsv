CREATE TABLE
    IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY,
        role_name VARCHAR(30) NOT NULL
    );

INSERT INTO
    roles (role_name)
VALUES
    ('ADMIN'),
    ('TEACHER'),
    ('USER'),
    ('GUEST');

CREATE TABLE
    IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name VARCHAR(100) NOT NULL,
        username VARCHAR(30) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES roles (role_id)
    );

CREATE TABLE
    IF NOT EXISTS user_preferences (
        user_id INTEGER PRIMARY KEY,
        level_preference VARCHAR(20) NOT NULL DEFAULT 'NONE' CHECK (
            level_preference IN ('NONE', 'BASIC', 'INTERMEDIATE')
        ),
        daily_goal INTEGER NOT NULL DEFAULT 10 CHECK (daily_goal IN (5, 10, 20)),
        audio_mode VARCHAR(20) NOT NULL DEFAULT 'FULL_AUDIO' CHECK (audio_mode IN ('FULL_AUDIO', 'NO_VOICE', 'MUTED')),
        is_simplified INTEGER DEFAULT 0 CHECK (is_simplified IN (0, 1)),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS user_game_stats (
        user_id INTEGER,
        current_level VARCHAR(2) NOT NULL DEFAULT 'A1' CHECK (
            current_level IN ('A1', 'A2', 'B1', 'B2', 'C1', 'C2')
        ),
        current_hearts INTEGER NOT NULL DEFAULT 5,
        total_score INTEGER NOT NULL DEFAULT 0,
        current_streak INTEGER NOT NULL DEFAULT 0,
        max_hearts INTEGER NOT NULL DEFAULT 5,
        last_activity_date DATE NULLABLE,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );