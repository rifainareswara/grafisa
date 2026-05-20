import sqlite3
import psycopg2
import os

PG_HOST = "34.50.103.155"
PG_USER = "postgres"
PG_PASSWORD = "grafisapassword"
PG_DB = "grafisa"

# Connect to postgres
pg_conn = psycopg2.connect(
    host=PG_HOST,
    user=PG_USER,
    password=PG_PASSWORD,
    dbname=PG_DB
)
pg_cursor = pg_conn.cursor()

# Connect to sqlite
sqlite_conn = sqlite3.connect("backend/grafisa.db")
sqlite_conn.row_factory = sqlite3.Row
sqlite_cursor = sqlite_conn.cursor()

# Get all tables from sqlite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table in tables:
    table_name = table['name']
    if table_name == 'sqlite_sequence':
        continue
        
    print(f"Migrating table: {table_name}")
    
    # Get rows
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    if not rows:
        continue
        
    # Get column names
    col_names = rows[0].keys()
    
    # Generate insert query
    placeholders = ",".join(["%s"] * len(col_names))
    columns = ",".join(col_names)
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    # Insert rows
    for row in rows:
        try:
            pg_cursor.execute(insert_query, tuple(row))
        except psycopg2.IntegrityError:
            pg_conn.rollback()
            continue
        except Exception as e:
            print(f"Error on row {dict(row)}: {e}")
            pg_conn.rollback()
            continue
        pg_conn.commit()

print("Migration completed.")
pg_conn.close()
sqlite_conn.close()
