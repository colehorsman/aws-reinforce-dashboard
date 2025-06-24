#!/usr/bin/env python3
"""
Setup Supabase using individual connection parameters
"""

import psycopg2
import sys

# Supabase connection parameters
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "thisisthedatabasepassword"
SUPABASE_HOST = "aws-0-us-west-1.pooler.supabase.com"  # This is likely the host
SUPABASE_PORT = "6543"  # Pooler port (might be 5432 for direct connection)
SUPABASE_DBNAME = "postgres"

def setup_supabase():
    """Setup Supabase with individual parameters."""
    
    print("🚀 Starting Supabase setup...")
    print(f"🔗 Connecting to: {SUPABASE_HOST}:{SUPABASE_PORT}")
    
    # Step 1: Connect and create schema
    print("\n📊 Creating database schema...")
    try:
        # Try connection with pooler first
        conn = psycopg2.connect(
            user=f"postgres.tpjpvthtomffzafgzynk",  # Pooler requires project ref
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            dbname=SUPABASE_DBNAME
        )
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
        print(f"❌ Failed with pooler connection: {e}")
        print("\n🔄 Trying direct connection...")
        
        # Try direct connection
        try:
            conn = psycopg2.connect(
                user=SUPABASE_USER,
                password=SUPABASE_PASSWORD,
                host=f"db.tpjpvthtomffzafgzynk.supabase.co",
                port="5432",
                dbname=SUPABASE_DBNAME
            )
            cur = conn.cursor()
            
            # Create table (same as above)
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
            
            conn.commit()
            print("✅ Schema created with direct connection!")
            
        except Exception as e2:
            print(f"❌ Both connections failed: {e2}")
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
    
    return True

if __name__ == "__main__":
    # First, let's find out which connection parameters work
    print("🔍 Testing connection parameters from Supabase dashboard...")
    print("\nPlease provide the connection parameters from your Supabase dashboard:")
    print("(Go to Settings → Database → Connection parameters)\n")
    
    host = input("Host (e.g., aws-0-us-west-1.pooler.supabase.com): ").strip()
    port = input("Port (e.g., 6543 or 5432): ").strip()
    database = input("Database name (usually 'postgres'): ").strip() or "postgres"
    user = input("User (for pooler use postgres.tpjpvthtomffzafgzynk, for direct use postgres): ").strip()
    
    # Update global variables
    SUPABASE_HOST = host
    SUPABASE_PORT = port
    SUPABASE_DBNAME = database
    SUPABASE_USER = user
    
    if setup_supabase():
        print("\n✅ All done! Your Supabase database is ready!")
        print("\n📋 Add these to your Streamlit secrets:")
        print(f"""
[postgres]
host = "{SUPABASE_HOST}"
port = {SUPABASE_PORT}
database = "{SUPABASE_DBNAME}"
user = "{SUPABASE_USER}"
password = "thisisthedatabasepassword"
""")
    else:
        print("\n❌ Setup failed. Please check the connection parameters.")