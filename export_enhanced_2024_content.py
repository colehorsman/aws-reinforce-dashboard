#!/usr/bin/env python3
"""
Export enhanced 2024 session content for production database deployment
"""
import psycopg2
import json
import csv
from datetime import datetime

# Local database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'reinforce_summaries',
    'user': 'colehorsman',
    'port': 5432
}

def export_enhanced_2024_content():
    """Export all enhanced 2024 content to multiple formats for production deployment."""
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get all 2024 sessions with enhanced content
        cursor.execute("""
            SELECT 
                id, title, session_code, domain, year,
                key_points, technical_details,
                author, summary
            FROM summaries 
            WHERE year = 2024 
            AND key_points IS NOT NULL 
            AND technical_details IS NOT NULL
            AND array_length(key_points, 1) > 0
            AND array_length(technical_details, 1) > 0
            ORDER BY domain, title
        """)
        
        results = cursor.fetchall()
        
        print(f"📊 Found {len(results)} enhanced 2024 sessions to export")
        
        # Export as SQL UPDATE statements
        export_sql_updates(results)
        
        # Export as JSON for backup
        export_json_backup(results)
        
        # Export as CSV for review
        export_csv_summary(results)
        
        conn.close()
        
        print("✅ Export completed successfully!")
        print("\nFiles created:")
        print("• enhanced_2024_updates.sql - SQL UPDATE statements for production")
        print("• enhanced_2024_backup.json - JSON backup of all enhanced content")
        print("• enhanced_2024_summary.csv - CSV summary for review")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")

def export_sql_updates(results):
    """Create SQL UPDATE statements for production deployment."""
    
    with open('/Users/colehorsman/reinforce-2025-summaries/enhanced_2024_updates.sql', 'w') as f:
        f.write("-- Enhanced 2024 Session Content Updates\n")
        f.write(f"-- Generated: {datetime.now().isoformat()}\n")
        f.write(f"-- Total records: {len(results)}\n\n")
        f.write("BEGIN;\n\n")
        
        for row in results:
            id, title, session_code, domain, year, key_points, technical_details, author, summary = row
            
            # Escape single quotes for SQL
            def escape_sql(text):
                if text is None:
                    return None
                return text.replace("'", "''")
            
            # Convert arrays to PostgreSQL array format
            def array_to_sql(arr):
                if not arr:
                    return 'NULL'
                escaped_items = [f"'{escape_sql(item)}'" for item in arr]
                return f"ARRAY[{', '.join(escaped_items)}]"
            
            key_points_sql = array_to_sql(key_points)
            technical_details_sql = array_to_sql(technical_details)
            
            f.write(f"""-- Update session: {escape_sql(title)}
UPDATE summaries 
SET 
    key_points = {key_points_sql},
    technical_details = {technical_details_sql}
WHERE id = {id} AND year = 2024;

""")
        
        f.write("COMMIT;\n")
        f.write(f"\n-- Verification query:\n")
        f.write("SELECT COUNT(*) as enhanced_sessions FROM summaries WHERE year = 2024 AND key_points IS NOT NULL AND technical_details IS NOT NULL;\n")

def export_json_backup(results):
    """Create JSON backup of all enhanced content."""
    
    backup_data = {
        "export_date": datetime.now().isoformat(),
        "total_records": len(results),
        "sessions": []
    }
    
    for row in results:
        id, title, session_code, domain, year, key_points, technical_details, author, summary = row
        
        session_data = {
            "id": id,
            "title": title,
            "session_code": session_code,
            "domain": domain,
            "year": year,
            "author": author,
            "summary": summary,
            "key_points": key_points,
            "technical_details": technical_details
        }
        
        backup_data["sessions"].append(session_data)
    
    with open('/Users/colehorsman/reinforce-2025-summaries/enhanced_2024_backup.json', 'w') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)

def export_csv_summary(results):
    """Create CSV summary for review."""
    
    with open('/Users/colehorsman/reinforce-2025-summaries/enhanced_2024_summary.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'ID', 'Title', 'Session Code', 'Domain', 'Author',
            'Key Points Count', 'Technical Details Count',
            'First Key Point Preview', 'First Technical Detail Preview'
        ])
        
        # Data rows
        for row in results:
            id, title, session_code, domain, year, key_points, technical_details, author, summary = row
            
            key_points_count = len(key_points) if key_points else 0
            tech_details_count = len(technical_details) if technical_details else 0
            
            first_key_point = key_points[0][:100] + "..." if key_points and len(key_points[0]) > 100 else (key_points[0] if key_points else "")
            first_tech_detail = technical_details[0][:100] + "..." if technical_details and len(technical_details[0]) > 100 else (technical_details[0] if technical_details else "")
            
            writer.writerow([
                id, title, session_code, domain, author,
                key_points_count, tech_details_count,
                first_key_point, first_tech_detail
            ])

if __name__ == "__main__":
    export_enhanced_2024_content()