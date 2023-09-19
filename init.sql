CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS apps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    secret TEXT NOT NULL,
    host TEXT NOT NULL,
    name TEXT NOT NULL,
    owner_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS apps_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    encrypted_password BYTEA NOT NULL,
    app_id UUID NOT NULL,
    FOREIGN KEY (app_id) REFERENCES apps (id) ON DELETE CASCADE,
    CONSTRAINT uq_username_app_id UNIQUE (username, app_id)
);
