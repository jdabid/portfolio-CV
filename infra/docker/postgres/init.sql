-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Verify
SELECT extname FROM pg_extension WHERE extname IN ('uuid-ossp', 'pg_trgm');
