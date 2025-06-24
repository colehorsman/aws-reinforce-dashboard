#!/usr/bin/env python3
"""
Create production-compatible SQL updates for TEXT columns instead of ARRAY columns
"""
import psycopg2
import json

# Local database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'reinforce_summaries',
    'user': 'colehorsman',
    'port': 5432
}

def create_text_based_deployment():
    """Create SQL updates that work with TEXT columns instead of ARRAY columns."""
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get enhanced 2024 sessions
        cursor.execute("""
            SELECT 
                id, title, session_code, domain, year,
                key_points, technical_details
            FROM summaries 
            WHERE year = 2024 
            AND key_points IS NOT NULL 
            AND technical_details IS NOT NULL
            AND array_length(key_points, 1) > 0
            AND array_length(technical_details, 1) > 0
            ORDER BY domain, title
        """)
        
        results = cursor.fetchall()
        print(f"📊 Creating TEXT-based updates for {len(results)} enhanced sessions")
        
        with open('/Users/colehorsman/reinforce-2025-summaries/text_based_updates.sql', 'w') as f:
            f.write("-- Production TEXT-Based Enhanced 2024 Content Updates\n")
            f.write(f"-- Generated for TEXT columns (not ARRAY)\n")
            f.write(f"-- Total records: {len(results)}\n\n")
            f.write("BEGIN;\n\n")
            
            for row in results:
                id, title, session_code, domain, year, key_points, technical_details = row
                
                # Convert arrays to formatted text
                def array_to_text(arr):
                    if not arr:
                        return ''
                    # Join with double newlines for clear separation
                    return '\\n\\n'.join(arr)
                
                # Escape single quotes for SQL
                def escape_sql(text):
                    if text is None:
                        return ''
                    return text.replace("'", "''")
                
                key_points_text = escape_sql(array_to_text(key_points))
                tech_details_text = escape_sql(array_to_text(technical_details))
                title_escaped = escape_sql(title)
                
                f.write(f"-- Update: {title_escaped}\n")
                f.write(f"UPDATE summaries \n")
                f.write(f"SET \n")
                f.write(f"    key_points = '{key_points_text}',\n")
                f.write(f"    technical_details = '{tech_details_text}'\n")
                f.write(f"WHERE id = {id} AND year = 2024;\n\n")
            
            f.write("COMMIT;\n\n")
            f.write("-- Verification query for TEXT columns:\n")
            f.write("SELECT COUNT(*) as enhanced_sessions FROM summaries WHERE year = 2024 AND key_points IS NOT NULL AND length(key_points) > 10;\n")
        
        # Also create a specific test for the problematic session
        with open('/Users/colehorsman/reinforce-2025-summaries/test_specific_session.sql', 'w') as f:
            f.write("-- Test the specific session that user reported\n")
            f.write("SELECT \n")
            f.write("    title,\n") 
            f.write("    CASE WHEN key_points IS NOT NULL AND length(key_points) > 10 \n")
            f.write("         THEN 'Has Enhanced Content' \n")
            f.write("         ELSE 'Missing Content' END as key_points_status,\n")
            f.write("    CASE WHEN technical_details IS NOT NULL AND length(technical_details) > 10 \n")
            f.write("         THEN 'Has Enhanced Content' \n")
            f.write("         ELSE 'Missing Content' END as tech_details_status,\n")
            f.write("    substring(key_points, 1, 100) as key_points_preview\n")
            f.write("FROM summaries \n")
            f.write("WHERE title ILIKE '%5 ways generative AI can enhance cybersecurity%' \n")
            f.write("AND year = 2024;\n")
        
        conn.close()
        
        print("✅ Created TEXT-based deployment files:")
        print("• text_based_updates.sql - Main deployment script")
        print("• test_specific_session.sql - Test the reported session")
        
    except Exception as e:
        print(f"❌ Error creating TEXT-based updates: {e}")

if __name__ == "__main__":
    create_text_based_deployment()