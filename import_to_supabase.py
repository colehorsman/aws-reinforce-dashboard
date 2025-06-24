#!/usr/bin/env python3
"""
Import data from local PostgreSQL to Supabase
"""

import psycopg2
import sys

# Configuration
LOCAL_DB = {
    'host': 'localhost',
    'database': 'reinforce_summaries',
    'user': 'colehorsman',
    'port': 5432
}

def import_data(supabase_connection_string):
    """Import data from local PostgreSQL to Supabase."""
    
    print("🔄 Connecting to local database...")
    try:
        local_conn = psycopg2.connect(**LOCAL_DB)
        local_cur = local_conn.cursor()
    except Exception as e:
        print(f"❌ Failed to connect to local database: {e}")
        return
    
    print("🔄 Connecting to Supabase...")
    try:
        supabase_conn = psycopg2.connect(supabase_connection_string)
        supabase_cur = supabase_conn.cursor()
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return
    
    print("📊 Fetching data from local database...")
    local_cur.execute("""
        SELECT year, domain, title, session_code, author, duration, 
               word_count, publish_date, video_id, video_url, summary,
               key_points, technical_details, full_transcript, file_path,
               speaker_name, speaker_company, speaker_linkedin_url
        FROM summaries
    """)
    
    rows = local_cur.fetchall()
    print(f"✅ Found {len(rows)} records to import")
    
    print("📤 Importing to Supabase...")
    insert_query = """
        INSERT INTO summaries (
            year, domain, title, session_code, author, duration,
            word_count, publish_date, video_id, video_url, summary,
            key_points, technical_details, full_transcript, file_path,
            speaker_name, speaker_company, speaker_linkedin_url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        # Clear existing data first (optional)
        supabase_cur.execute("TRUNCATE TABLE summaries RESTART IDENTITY CASCADE")
        
        # Insert all rows
        supabase_cur.executemany(insert_query, rows)
        supabase_conn.commit()
        
        # Verify import
        supabase_cur.execute("SELECT COUNT(*) FROM summaries")
        count = supabase_cur.fetchone()[0]
        
        print(f"✅ Successfully imported {count} records to Supabase!")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        supabase_conn.rollback()
    finally:
        local_conn.close()
        supabase_conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_to_supabase.py 'postgresql://postgres:password@db.xxxx.supabase.co:5432/postgres'")
        sys.exit(1)
    
    import_data(sys.argv[1])