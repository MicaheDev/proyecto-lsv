CREATE TABLE
    IF NOT EXISTS roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    IF NOT EXISTS levels (
        level_id INTEGER PRIMARY KEY AUTOINCREMENT,
        level_name VARCHAR(2) NOT NULL
    );
    
INSERT INTO
    levels (level_name) 
VALUES
    ('A1'),
    ('A2'),
    ('B1'),
    ('B2'),
    ('C1'),
    ('C2');

        
CREATE TABLE
    IF NOT EXISTS user_preferences (
        user_id INTEGER,
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
        current_level_id INTEGER,
        current_hearts INTEGER NOT NULL DEFAULT 5,
        total_score INTEGER NOT NULL DEFAULT 0,
        current_streak INTEGER NOT NULL DEFAULT 0,
        max_hearts INTEGER NOT NULL DEFAULT 5,
        last_activity_date DATE NULLABLE,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (current_level_id) REFERENCES levels (level_id) ON DELETE CASCADE
    );
    
    
CREATE TABLE 
    IF NOT EXISTS sections (
        section_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        level_id INTEGER,
        FOREIGN KEY (level_id) REFERENCES levels (level_id) ON DELETE CASCADE
    );
    
CREATE TABLE
    IF NOT EXISTS units (
        unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id INTEGER,
        title VARCHAR(100) NOT NULL,
        theme_color varchar(50) NOT NULL,
        FOREIGN KEY (section_id) REFERENCES sections (section_id) ON DELETE CASCADE
    );
    
CREATE TABLE
    IF NOT EXISTS nodes (
        node_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        unit_id INTEGER,
        position INTEGER NOT NULL,
        FOREIGN KEY (unit_id) REFeRENCES units (unit_id) ON DELETE CASCADE
    );
    
CREATE TABLE
    IF NOT EXISTS lessons (
        lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id INTEGER,
        required_exp INTEGER NOT NULL,
        FOREIGN KEY (node_id) REFERENCES nodes (node_id) ON DELETE CASCADE
    );
    
CREATE TABLE 
    IF NOT EXISTS exercise_types (
    exercise_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_type_name VARCHAR(100) NOT NULL
);

INSERT INTO 
exercise_types (exercise_type_name) 
VALUES
    ('DEMO'),
    ('QUIZ_MULTIPLE'),
    ('REVERSE_QUIZ'),
    ('MATCHING'),
    ('CAM_VERIFY'),
    ('FREE_PRACTICE');
    
CREATE TABLE
    IF NOT EXISTS exercises (
        exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER,
        exercise_type_id INTEGER,
        question VARCHAR(100) NOT NULL,
        sign_id INTEGER,
        FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id) ON DELETE CASCADE,
        FOREIGN KEY (exercise_type_id) REFERENCES exercise_types (exercise_type_id) ON DELETE CASCADE,
        FOREIGN KEY (sign_id) REFERENCES signs (sign_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS signs (
        sign_id INTEGER PRIMARY KEY AUTOINCREMENT,
        meaning VARCHAR(100) NOT NULL,
        category_id INTEGER,
        resource_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (category_id) ON DELETE CASCADE,
        FOREIGN KEY (resource_id) REFERENCES resources (resource_id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(100)
    );
    
CREATE TABLE
    IF NOT EXISTS media_types (
        media_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        media_type_name VARCHAR(100) NOT NULL
    );
    
INSERT INTO 
    media_types (media_type_name)
VALUES
    ('VIDEO'),
    ('STATIC_IMAGE'),
    ('3D');

CREATE TABLE 
    IF NOT EXISTS resources (
        resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_type_id INTEGER,
        resource_content BLOB NOT NULL,
        FOREIGN KEY (resource_type_id) REFERENCES media_types (media_type_id) ON DELETE CASCADE 
    );
    
    

