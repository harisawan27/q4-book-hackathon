-- migrations/005_user_personalization.sql
-- User Authentication, Personalization, and Urdu Translation feature

-- Enable UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Create users table (Better-Auth compatible)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified TIMESTAMPTZ,
    name VARCHAR(255),
    image TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create accounts table (Better-Auth compatible)
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    provider_account_id VARCHAR(255) NOT NULL,
    refresh_token TEXT,
    access_token TEXT,
    expires_at BIGINT,
    token_type VARCHAR(50),
    scope TEXT,
    id_token TEXT,
    session_state TEXT,
    UNIQUE(provider, provider_account_id)
);

-- 3. Create auth sessions table (Better-Auth compatible)
CREATE TABLE IF NOT EXISTS auth_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_token VARCHAR(255) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires TIMESTAMPTZ NOT NULL
);

-- 4. Create verification_tokens table (Better-Auth compatible)
CREATE TABLE IF NOT EXISTS verification_tokens (
    identifier VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires TIMESTAMPTZ NOT NULL,
    UNIQUE(identifier, token)
);

-- 5. Create user_backgrounds table (Custom)
CREATE TABLE IF NOT EXISTS user_backgrounds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    software_skills VARCHAR(20) NOT NULL DEFAULT 'none'
        CHECK (software_skills IN ('none', 'beginner', 'intermediate', 'advanced')),
    hardware_skills VARCHAR(20) NOT NULL DEFAULT 'none'
        CHECK (hardware_skills IN ('none', 'beginner', 'intermediate', 'advanced')),
    experience_level VARCHAR(20) NOT NULL DEFAULT 'student'
        CHECK (experience_level IN ('student', 'professional', 'hobbyist', 'researcher')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Create transformation_logs table (Custom)
CREATE TABLE IF NOT EXISTS transformation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    chapter_slug VARCHAR(255) NOT NULL,
    transformation_type VARCHAR(20) NOT NULL
        CHECK (transformation_type IN ('personalization', 'translation')),
    input_length INTEGER NOT NULL,
    output_length INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL,
    success BOOLEAN NOT NULL DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Extend existing sessions table (optional user linkage for RAG chatbot)
-- Only run if the sessions table exists and doesn't have user_id
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'sessions') THEN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'sessions' AND column_name = 'user_id') THEN
            ALTER TABLE sessions ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE SET NULL;
        END IF;
    END IF;
END $$;

-- 8. Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_user_id ON auth_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_auth_sessions_token ON auth_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_user_backgrounds_user_id ON user_backgrounds(user_id);
CREATE INDEX IF NOT EXISTS idx_transformation_logs_user_id ON transformation_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_transformation_logs_chapter ON transformation_logs(chapter_slug);
CREATE INDEX IF NOT EXISTS idx_transformation_logs_type ON transformation_logs(transformation_type);
CREATE INDEX IF NOT EXISTS idx_transformation_logs_created ON transformation_logs(created_at);
