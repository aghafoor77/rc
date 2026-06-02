-- EU AI Act Compliance System - Database Initialization Script
-- PostgreSQL 15+

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS compliance;
CREATE SCHEMA IF NOT EXISTS audit;

-- Set search path
SET search_path TO compliance, public;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA compliance TO ai_compliance_user;
GRANT ALL PRIVILEGES ON SCHEMA audit TO ai_compliance_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA compliance TO ai_compliance_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA audit TO ai_compliance_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA compliance TO ai_compliance_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA audit TO ai_compliance_user;

-- Default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA compliance GRANT ALL ON TABLES TO ai_compliance_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA compliance GRANT ALL ON SEQUENCES TO ai_compliance_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT ALL ON TABLES TO ai_compliance_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT ALL ON SEQUENCES TO ai_compliance_user;

-- Create initial tables will be handled by Alembic migrations
-- This script only sets up the database structure and permissions

-- Made with Bob
