# SQL to create schema, meta table. Use command line to create
SQL = """
    CREATE SCHEMA IF NOT EXISTS raw; 
    CREATE SCHEMA IF NOT EXISTS staging; 
    CREATE SCHEMA IF NOT EXISTS marts; 
    CREATE SCHEMA IF NOT EXISTS meta; 

    CREATE TABLE IF NOT EXISTS meta.elt_run(
        run_id TEXT PRIMARY KEY,
        pipeline TEXT NOT NULL,
        status TEXT NOT NULL,
        row_count BIGINT,
        started_at TIMESTAMPTZ,
        finished_at TIMESTAMPTZ,
        note TEXT
        );
    """

# command line creating schema
# docker compose exec postgres psql -d weather_elt -U weather -c "CREATE SCHEMA IF NOT EXISTS raw; 
# CREATE SCHEMA IF NOT EXISTS staging; 
# CREATE SCHEMA IF NOT EXISTS marts; 
# CREATE SCHEMA IF NOT EXISTS meta;"     

# command line creating table
# docker compose exec postgres psql -d weather_elt -U weather -c "CREATE TABLE IF NOT EXISTS meta.elt_run(                                                                     
#         run_id TEXT PRIMARY KEY,
#         pipeline TEXT NOT NULL,
#         status TEXT NOT NULL,
#         row_count BIGINT,
#         started_at TIMESTAMPTZ,
#         finished_at TIMESTAMPTZ,
#         note TEXT
#        );
#     "