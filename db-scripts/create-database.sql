-- 1. Create role (user)
CREATE ROLE daily_wisdom_user
WITH LOGIN
PASSWORD 'daily_wisdom_user'
NOSUPERUSER
NOCREATEDB
NOCREATEROLE
NOINHERIT;

-- 2. Create database (default tablespace)
CREATE DATABASE daily_wisdom
WITH OWNER = daily_wisdom_user
ENCODING = 'UTF8'
TABLESPACE = pg_default
LC_COLLATE = 'en_US.UTF-8'
LC_CTYPE = 'en_US.UTF-8'
TEMPLATE = template0;

-- 3. Restrict public access (important for rule #1)
REVOKE ALL ON DATABASE daily_wisdom FROM PUBLIC;

-- 4. Connect to the database
\c daily_wisdom;

-- 5. Create a dedicated schema (NOT public)
CREATE SCHEMA IF NOT EXISTS daily_wisdom
AUTHORIZATION daily_wisdom_user;

-- 6. Restrict access to public schema
REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM daily_wisdom_user;

-- 7. Set search path (so objects are created in proper schema)
ALTER ROLE daily_wisdom_user
SET search_path TO daily_wisdom;

-- 8. Grant privileges on schema
GRANT USAGE, CREATE ON SCHEMA daily_wisdom TO daily_wisdom_user;

-- 9. Create table in custom schema
CREATE TABLE daily_wisdom.DAILY_WISDOMS (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    wisdom_text TEXT NOT NULL,
    author VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Grant table access
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA daily_wisdom
TO daily_wisdom_user;

-- Future-proof: auto grants
ALTER DEFAULT PRIVILEGES IN SCHEMA daily_wisdom
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO daily_wisdom_user;