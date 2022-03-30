-- Reinitialize the database
DROP DATABASE IF EXISTS "database";
CREATE DATABASE "database";

\connect database

-- Create the 'nocase' collation rules, per Postgres collation docs
-- Ref: https://www.postgresql.org/docs/current/collation.html
CREATE COLLATION nocase (provider = icu, locale = 'und-u-ks-level2', deterministic = false);