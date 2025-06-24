#!/usr/bin/env python3
"""
Final Supabase setup using the working pooler connection
"""

import psycopg2

# Working connection parameters
SUPABASE_CONFIG = {
    'host': 'aws-0-us-east-1.pooler.supabase.com',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres.tpjpvthtomffzafgzynk',
    'password': 'thisisthedatabasepassword'
}

def setup_database():
    """Setup Supabase database with schema and data."""
    
    print("🚀 Starting Supabase setup with pooler connection...")
    
    # Connect to Supabase
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        cur = conn.cursor()
        print("✅ Connected to Supabase!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Step 1: Create schema
    print("\n📊 Creating database schema...")
    try:
        # Drop table if exists (for clean setup)
        cur.execute("DROP TABLE IF EXISTS summaries CASCADE;")
        
        # Create table matching local schema
        cur.execute("""
            CREATE TABLE summaries (
                id SERIAL PRIMARY KEY,
                year INTEGER NOT NULL,
                domain VARCHAR(50) NOT NULL,
                title TEXT NOT NULL,
                session_code VARCHAR(20),
                author VARCHAR(100),
                duration VARCHAR(20),
                word_count VARCHAR(20),
                publish_date VARCHAR(20),
                video_id VARCHAR(50),
                video_url TEXT,
                summary TEXT,
                key_points TEXT[],
                technical_details TEXT[],
                full_transcript TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                speaker_name VARCHAR(255),
                linkedin_url VARCHAR(500)
            );
        """)
        
        # Create indexes
        cur.execute("CREATE INDEX idx_summaries_year ON summaries(year);")
        cur.execute("CREATE INDEX idx_summaries_domain ON summaries(domain);")
        cur.execute("CREATE INDEX idx_summaries_session_code ON summaries(session_code);")
        
        conn.commit()
        print("✅ Schema created successfully!")
        
    except Exception as e:
        print(f"❌ Schema creation failed: {e}")
        conn.rollback()
        return False
    
    # Step 2: Import data from local database
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
                   speaker_name, linkedin_url
            FROM summaries
            ORDER BY id
        """)
        
        rows = local_cur.fetchall()
        print(f"📊 Found {len(rows)} records to import")
        
        # Insert data
        insert_query = """
            INSERT INTO summaries (
                year, domain, title, session_code, author, duration,
                word_count, publish_date, video_id, video_url, summary,
                key_points, technical_details, full_transcript, file_path,
                speaker_name, linkedin_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Insert in batches of 10 (pooler might have smaller limits)
        batch_size = 10
        total_imported = 0
        
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            try:
                cur.executemany(insert_query, batch)
                conn.commit()
                total_imported += len(batch)
                print(f"  Imported {total_imported}/{len(rows)} records...")
            except Exception as e:
                print(f"  ⚠️  Batch {i}-{i+batch_size} failed: {e}")
                conn.rollback()
        
        # Verify final count
        cur.execute("SELECT COUNT(*) FROM summaries")
        final_count = cur.fetchone()[0]
        print(f"\n✅ Successfully imported {final_count} records!")
        
        # Show sample data
        cur.execute("SELECT year, domain, COUNT(*) FROM summaries GROUP BY year, domain ORDER BY year, domain")
        stats = cur.fetchall()
        print("\n📊 Data summary:")
        for year, domain, count in stats:
            print(f"  {year} - {domain}: {count} talks")
        
        local_conn.close()
        
    except Exception as e:
        print(f"❌ Data import failed: {e}")
        conn.rollback()
        return False
    
    conn.close()
    print("\n🎉 Supabase setup complete!")
    
    # Print final instructions
    print("\n" + "="*60)
    print("📋 SAVE THESE CONNECTION DETAILS FOR STREAMLIT:")
    print("="*60)
    print("""
Copy this exactly into Streamlit Cloud secrets:

[postgres]
host = "aws-0-us-east-1.pooler.supabase.com"
port = 5432
database = "postgres"
user = "postgres.tpjpvthtomffzafgzynk"
password = "thisisthedatabasepassword"

OPENAI_API_KEY = "your-openai-api-key-here"
""")
    print("="*60)
    
    return True

if __name__ == "__main__":
    if setup_database():
        print("\n✅ Your Supabase database is ready for Streamlit deployment!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")