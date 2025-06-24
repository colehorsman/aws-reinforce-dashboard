#!/usr/bin/env python3
"""
Verify enhanced 2024 content deployment to production
"""
import psycopg2
import os

def test_specific_sessions():
    """Test specific sessions that users reported as missing content."""
    
    test_sessions = [
        "5 ways generative AI can enhance cybersecurity",
        "Accelerating auditing and compliance for generative AI",
        "Build responsible AI applications with Guardrails"
    ]
    
    try:
        # Production database connection
        DB_CONFIG = {
            'host': os.getenv('PROD_DB_HOST', 'your-supabase-host.supabase.co'),
            'database': os.getenv('PROD_DB_NAME', 'postgres'),
            'user': os.getenv('PROD_DB_USER', 'postgres'),
            'password': os.getenv('PROD_DB_PASSWORD', 'your-password'),
            'port': int(os.getenv('PROD_DB_PORT', '5432'))
        }
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔍 Testing specific sessions in production database:")
        print("=" * 60)
        
        for session_partial in test_sessions:
            cursor.execute("""
                SELECT title, 
                       CASE WHEN key_points IS NOT NULL AND array_length(key_points, 1) > 0 
                            THEN array_length(key_points, 1) ELSE 0 END as key_points_count,
                       CASE WHEN technical_details IS NOT NULL AND array_length(technical_details, 1) > 0 
                            THEN array_length(technical_details, 1) ELSE 0 END as tech_details_count,
                       key_points[1] as first_key_point
                FROM summaries 
                WHERE title ILIKE %s AND year = 2024
                LIMIT 1
            """, [f'%{session_partial}%'])
            
            result = cursor.fetchone()
            
            if result:
                title, key_count, tech_count, first_key = result
                status = "✅" if key_count > 0 and tech_count > 0 else "❌"
                print(f"{status} {title}")
                print(f"   Key Points: {key_count}, Technical Details: {tech_count}")
                if first_key:
                    print(f"   Preview: {first_key[:80]}...")
                print()
            else:
                print(f"❌ Session not found: {session_partial}")
                print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Failed to verify production database: {e}")
        print("\n💡 Set environment variables for production database:")
        print("export PROD_DB_HOST=your-supabase-host.supabase.co")
        print("export PROD_DB_PASSWORD=your-password")

if __name__ == "__main__":
    test_specific_sessions()