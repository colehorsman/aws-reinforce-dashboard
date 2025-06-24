#!/usr/bin/env python3
"""
Simple Supabase setup using direct connection string
"""

import psycopg2
import sys

def setup_supabase_simple(connection_string):
    """Setup Supabase with direct connection string."""
    
    print("🚀 Starting Supabase setup...")
    
    # Step 1: Connect and create schema
    print("\n📊 Creating database schema...")
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        
        # Create table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS summaries (
                id SERIAL PRIMARY KEY,
                year INTEGER,
                domain VARCHAR(100),
                title TEXT,
                session_code VARCHAR(50),
                author TEXT,
                duration VARCHAR(50),
                word_count INTEGER,
                publish_date DATE,
                video_id VARCHAR(50),
                video_url TEXT,
                summary TEXT,
                key_points TEXT,
                technical_details TEXT,
                full_transcript TEXT,
                file_path TEXT,
                speaker_name VARCHAR(255),
                speaker_company VARCHAR(255),
                speaker_linkedin_url VARCHAR(500)
            );
        """)
        
        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_summaries_year ON summaries(year);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_summaries_domain ON summaries(domain);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_summaries_session_code ON summaries(session_code);")
        
        conn.commit()
        print("✅ Schema created successfully!")
        
    except Exception as e:
        print(f"❌ Failed to create schema: {e}")
        return False
    
    # Step 2: Import data
    print("\n📤 Importing data from local database...")
    try:
        # Connect to local database
        local_conn = psycopg2.connect(
            host='localhost',
            database='reinforce_summaries',
            user='colehorsman',
            port=5432
        )
        local_cur = local_conn.cursor()
        
        # Fetch all data
        local_cur.execute("""
            SELECT year, domain, title, session_code, author, duration, 
                   word_count, publish_date, video_id, video_url, summary,
                   key_points, technical_details, full_transcript, file_path,
                   speaker_name, speaker_company, speaker_linkedin_url
            FROM summaries
        """)
        
        rows = local_cur.fetchall()
        print(f"📊 Found {len(rows)} records to import")
        
        # Clear existing data
        cur.execute("TRUNCATE TABLE summaries RESTART IDENTITY CASCADE")
        
        # Insert data in batches
        insert_query = """
            INSERT INTO summaries (
                year, domain, title, session_code, author, duration,
                word_count, publish_date, video_id, video_url, summary,
                key_points, technical_details, full_transcript, file_path,
                speaker_name, speaker_company, speaker_linkedin_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Insert in smaller batches
        batch_size = 50
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            cur.executemany(insert_query, batch)
            conn.commit()
            print(f"  Imported {min(i + batch_size, len(rows))}/{len(rows)} records...")
        
        # Verify
        cur.execute("SELECT COUNT(*) FROM summaries")
        count = cur.fetchone()[0]
        print(f"✅ Successfully imported {count} records!")
        
        local_conn.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Failed to import data: {e}")
        if conn:
            conn.close()
        return False
    
    print("\n🎉 Setup complete!")
    print("\n📋 Connection details for Streamlit secrets.toml:")
    print("""
[postgres]
host = "db.tpjpvthtomffzafgzynk.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "thisisthedatabasepassword"
""")
    
    return True

if __name__ == "__main__":
    # Replace [YOUR-PASSWORD] with the actual password
    connection_string = "postgresql://postgres:thisisthedatabasepassword@db.tpjpvthtomffzafgzynk.supabase.co:5432/postgres"
    
    print("Using connection string (password hidden):")
    print("postgresql://postgres:***@db.tpjpvthtomffzafgzynk.supabase.co:5432/postgres")
    
    if setup_supabase_simple(connection_string):
        print("\n✅ All done! Your Supabase database is ready for Streamlit Cloud!")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")