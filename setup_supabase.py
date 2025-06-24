#!/usr/bin/env python3
"""
Automated Supabase setup script
Sets up tables and imports data using Supabase API
"""

import requests
import psycopg2
import sys
import json

def setup_supabase(project_url, service_key, db_password):
    """
    Automate Supabase setup
    
    Args:
        project_url: Your Supabase project URL (e.g., https://xxxxx.supabase.co)
        service_key: Your Supabase service role key (from Settings > API)
        db_password: Your database password
    """
    
    # Extract project ref from URL
    project_ref = project_url.split('//')[1].split('.')[0]
    
    # Database connection string
    from urllib.parse import quote_plus
    # Supabase uses aws-0-us-west-1.pooler.supabase.com format for connection pooling
    db_host = f"aws-0-us-west-1.pooler.supabase.com"
    # URL encode the password to handle special characters
    encoded_password = quote_plus(db_password)
    # Try direct connection first
    connection_string = f"postgresql://postgres.{project_ref}:{encoded_password}@{db_host}:5432/postgres"
    
    # Fallback connection string
    fallback_host = f"db.{project_ref}.supabase.co"
    fallback_connection = f"postgresql://postgres:{encoded_password}@{fallback_host}:5432/postgres"
    
    print(f"🔧 Setting up Supabase project: {project_ref}")
    
    # Step 1: Create tables via direct database connection
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
        cur.execute("CREATE INDEX IF NOT EXISTS idx_summaries_speaker_name ON summaries(speaker_name);")
        
        conn.commit()
        print("✅ Database schema created successfully!")
        
    except Exception as e:
        print(f"❌ Failed to create schema: {e}")
        return False
    
    # Step 2: Import data from local PostgreSQL
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
        
        # Insert data
        insert_query = """
            INSERT INTO summaries (
                year, domain, title, session_code, author, duration,
                word_count, publish_date, video_id, video_url, summary,
                key_points, technical_details, full_transcript, file_path,
                speaker_name, speaker_company, speaker_linkedin_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Batch insert
        cur.executemany(insert_query, rows)
        conn.commit()
        
        # Verify
        cur.execute("SELECT COUNT(*) FROM summaries")
        count = cur.fetchone()[0]
        print(f"✅ Successfully imported {count} records!")
        
        local_conn.close()
        
    except Exception as e:
        print(f"❌ Failed to import data: {e}")
        return False
    
    # Step 3: Enable Row Level Security (optional but recommended)
    print("\n🔒 Configuring security...")
    try:
        # Enable RLS
        cur.execute("ALTER TABLE summaries ENABLE ROW LEVEL SECURITY;")
        
        # Create a policy for public read access
        cur.execute("""
            CREATE POLICY "Allow public read access" ON summaries
            FOR SELECT USING (true);
        """)
        
        conn.commit()
        print("✅ Security configured!")
        
    except Exception as e:
        print(f"⚠️  Security configuration skipped: {e}")
    
    conn.close()
    
    # Step 4: Test the API
    print("\n🧪 Testing Supabase API...")
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json"
    }
    
    # Test query
    response = requests.get(
        f"{project_url}/rest/v1/summaries?limit=1",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ API test successful!")
    else:
        print(f"⚠️  API test returned status {response.status_code}")
    
    # Print connection details for Streamlit
    print("\n🎉 Setup complete! Here are your connection details for Streamlit:")
    print(f"\nDatabase Host: {db_host}")
    print(f"Database Port: 5432")
    print(f"Database Name: postgres")
    print(f"Database User: postgres")
    print(f"Database Password: {db_password}")
    
    print("\n📋 Add these to your Streamlit secrets:")
    print(f"""
[postgres]
host = "{db_host}"
port = 5432
database = "postgres"
user = "postgres"
password = "{db_password}"
""")
    
    return True

if __name__ == "__main__":
    print("🚀 Supabase Automated Setup")
    print("=" * 50)
    print("\nYou'll need:")
    print("1. Your Supabase project URL (e.g., https://xxxxx.supabase.co)")
    print("2. Your service role key (Settings > API > service_role)")
    print("3. Your database password\n")
    
    if len(sys.argv) == 4:
        project_url = sys.argv[1]
        service_key = sys.argv[2]
        db_password = sys.argv[3]
    else:
        project_url = input("Enter your Supabase project URL: ").strip()
        service_key = input("Enter your service role key: ").strip()
        db_password = input("Enter your database password: ").strip()
    
    setup_supabase(project_url, service_key, db_password)