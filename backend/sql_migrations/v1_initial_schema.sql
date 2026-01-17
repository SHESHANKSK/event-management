-- v1_initial_schema.sql

-- t_users
CREATE TABLE IF NOT EXISTS t_users (
    uid CHAR(36) PRIMARY KEY,
    username VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    country_code VARCHAR,
    roles JSON DEFAULT '[]',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_t_users_username ON t_users (username);
CREATE INDEX IF NOT EXISTS ix_t_users_email ON t_users (email);

-- t_events
CREATE TABLE IF NOT EXISTS t_events (
    event_id CHAR(36) PRIMARY KEY,
    event_name VARCHAR NOT NULL,
    event_description TEXT,
    event_date DATE NOT NULL,
    event_status VARCHAR(20) NOT NULL DEFAULT 'TODO', -- TODO, IN_PROGRESS, DONE, CANCELLED
    organizing_team VARCHAR NOT NULL,
    participants_count INTEGER,
    average_duration FLOAT,
    created_by CHAR(36) NOT NULL,
    updated_by CHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(created_by) REFERENCES t_users(uid),
    FOREIGN KEY(updated_by) REFERENCES t_users(uid)
);

-- t_attendance
CREATE TABLE IF NOT EXISTS t_attendance (
    attendance_id CHAR(36) PRIMARY KEY,
    event_id CHAR(36) NOT NULL,
    email VARCHAR NOT NULL, -- Participant ID
    duration INTEGER NOT NULL, -- Minutes
    role VARCHAR NOT NULL,
    full_name VARCHAR,
    join_time DATETIME,
    leave_time DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(event_id) REFERENCES t_events(event_id)
);

-- t_role_permissions (RBAC)
CREATE TABLE IF NOT EXISTS t_role_permissions (
    role VARCHAR NOT NULL,
    permission VARCHAR NOT NULL,
    PRIMARY KEY (role, permission)
);

-- t_migrations (To track applied SQL)
CREATE TABLE IF NOT EXISTS t_migrations (
    id CHAR(36) PRIMARY KEY,
    filename VARCHAR NOT NULL UNIQUE,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
