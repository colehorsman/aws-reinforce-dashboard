#!/usr/bin/env python3
"""
Debug the exact chatbot query that's failing
"""

import psycopg2
import openai

# Supabase connection
SUPABASE_CONFIG = {
    'host': 'aws-0-us-east-1.pooler.supabase.com',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres.tpjpvthtomffzafgzynk',
    'password': 'thisisthedatabasepassword'
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def test_database_queries():
    """Test the exact queries used by the chatbot."""
    
    print("🔍 Testing database queries...")
    
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        cur = conn.cursor()
        
        # Test 1: Basic schema check
        print("\n1️⃣ Checking table schema...")
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'summaries' 
            ORDER BY ordinal_position
        """)
        
        columns = cur.fetchall()
        for col, dtype, nullable in columns:
            print(f"  {col}: {dtype} ({'NULL' if nullable == 'YES' else 'NOT NULL'})")
        
        # Test 2: Count by year (this is what "compare 2024 to 2025" uses)
        print("\n2️⃣ Testing year comparison query...")
        cur.execute("""
            SELECT year, COUNT(*) as total_talks,
                   COUNT(CASE WHEN summary IS NOT NULL AND summary != '' THEN 1 END) as with_summary
            FROM summaries 
            GROUP BY year 
            ORDER BY year
        """)
        
        year_stats = cur.fetchall()
        for year, total, with_summary in year_stats:
            print(f"  {year}: {total} talks, {with_summary} with summaries")
        
        # Test 3: Sample data check
        print("\n3️⃣ Testing sample data access...")
        cur.execute("""
            SELECT id, year, domain, title, 
                   CASE WHEN summary IS NULL THEN 'NULL' 
                        WHEN summary = '' THEN 'EMPTY' 
                        ELSE 'HAS_DATA' END as summary_status,
                   CASE WHEN key_points IS NULL THEN 'NULL'
                        WHEN key_points = '' THEN 'EMPTY'
                        ELSE 'HAS_DATA' END as key_points_status
            FROM summaries 
            ORDER BY id
            LIMIT 5
        """)
        
        samples = cur.fetchall()
        for row in samples:
            print(f"  ID {row[0]} ({row[1]} {row[2]}): summary={row[4]}, key_points={row[5]}")
        
        # Test 4: The exact query that might be failing
        print("\n4️⃣ Testing chatbot-style query...")
        try:
            cur.execute("""
                SELECT 
                    year,
                    COUNT(*) as total_talks,
                    COUNT(DISTINCT domain) as domains,
                    array_agg(DISTINCT domain) as domain_list,
                    COUNT(CASE WHEN summary IS NOT NULL AND summary != '' THEN 1 END) as talks_with_summary
                FROM summaries
                GROUP BY year
                ORDER BY year
            """)
            
            results = cur.fetchall()
            print("✅ Query successful!")
            for row in results:
                print(f"  Year {row[0]}: {row[1]} talks, {row[2]} domains, {row[4]} with summaries")
                print(f"    Domains: {row[3]}")
        
        except Exception as e:
            print(f"❌ Chatbot query failed: {e}")
        
        # Test 5: Check if the issue is in the Python code's column access
        print("\n5️⃣ Testing Python dictionary access...")
        cur.execute("SELECT * FROM summaries LIMIT 1")
        row = cur.fetchone()
        
        # Get column names
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'summaries' 
            ORDER BY ordinal_position
        """)
        column_names = [col[0] for col in cur.fetchall()]
        
        print(f"  Column names: {column_names}")
        
        # Create a dict like pandas would
        if row:
            row_dict = dict(zip(column_names, row))
            print(f"  Sample row keys: {list(row_dict.keys())}")
            
            # Test the specific access that might be failing
            try:
                summary_val = row_dict['summary']
                print(f"  ✅ Can access 'summary': {type(summary_val)} - {len(str(summary_val)) if summary_val else 'None'} chars")
            except KeyError as e:
                print(f"  ❌ KeyError accessing 'summary': {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

def test_openai_connection():
    """Test OpenAI API connection."""
    
    print("\n🤖 Testing OpenAI connection...")
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI test successful'"}],
            max_tokens=10
        )
        print(f"✅ OpenAI test successful: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Debugging Chatbot Issues")
    print("=" * 50)
    
    db_ok = test_database_queries()
    ai_ok = test_openai_connection()
    
    if db_ok and ai_ok:
        print("\n✅ Both database and OpenAI are working!")
        print("The issue might be in the Streamlit code logic.")
    else:
        print(f"\n❌ Issues found: DB={'❌' if not db_ok else '✅'} AI={'❌' if not ai_ok else '✅'}")