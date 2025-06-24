#!/usr/bin/env python3
"""
Test the exact query that's failing
"""

import psycopg2
import pandas as pd

# Supabase connection
SUPABASE_CONFIG = {
    'host': 'aws-0-us-east-1.pooler.supabase.com',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres.tpjpvthtomffzafgzynk',
    'password': 'thisisthedatabasepassword'
}

def run_query(sql, params=None):
    """Execute SQL query exactly like Streamlit does."""
    try:
        conn = psycopg2.connect(**SUPABASE_CONFIG)
        df = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        print(f"Query failed: {e}")
        return None

def test_comparison_query():
    """Test the exact comparison query from the chatbot."""
    
    print("🧪 Testing exact comparison query...")
    
    # This is the exact query from line 1418-1424
    comparison_sql = """
    SELECT year, domain, COUNT(*) as talk_count
    FROM summaries 
    WHERE year IN (2024, 2025)
    GROUP BY year, domain
    ORDER BY year, domain
    """
    
    # Test with empty list (line 1426)
    print("1️⃣ Testing with empty list parameter...")
    try:
        comparison_data = run_query(comparison_sql, [])
        print(f"✅ Query successful! Shape: {comparison_data.shape}")
        print(f"Columns: {list(comparison_data.columns)}")
        print(f"First few rows:\n{comparison_data.head()}")
        
        # Test accessing the columns like the code does
        print("\n2️⃣ Testing column access...")
        domains = comparison_data['domain'].unique()
        print(f"✅ Domains: {domains}")
        
        # Test the specific operation that might be failing
        print("\n3️⃣ Testing domain iteration...")
        for domain in domains:
            domain_data = comparison_data[comparison_data['domain'] == domain]
            print(f"Domain {domain}: {len(domain_data)} rows")
            
            data_2024 = domain_data[domain_data['year'] == 2024]
            data_2025 = domain_data[domain_data['year'] == 2025]
            
            talks_2024 = data_2024['talk_count'].sum() if not data_2024.empty else 0
            talks_2025 = data_2025['talk_count'].sum() if not data_2025.empty else 0
            
            print(f"  2024: {talks_2024}, 2025: {talks_2025}")
        
        # Test the follow-up query that might be failing
        print("\n4️⃣ Testing themes query...")
        themes_2024_sql = "SELECT key_points FROM summaries WHERE year = 2024 AND domain = %s AND key_points IS NOT NULL LIMIT 1"
        themes_2024 = run_query(themes_2024_sql, ['AI'])
        
        if themes_2024 is not None and not themes_2024.empty:
            print("✅ Themes query successful!")
            print(f"Columns: {list(themes_2024.columns)}")
            
            # This might be where the error occurs
            try:
                sample_2024 = themes_2024.iloc[0]['key_points']
                print(f"✅ Can access key_points: {len(sample_2024)} chars")
            except KeyError as e:
                print(f"❌ KeyError accessing key_points: {e}")
        else:
            print("❌ Themes query failed")
            
    except Exception as e:
        print(f"❌ Query failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comparison_query()