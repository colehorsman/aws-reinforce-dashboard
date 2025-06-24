#!/usr/bin/env python3
"""
Quick script to fix LinkedIn URLs for specific speakers
"""

import psycopg2

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'reinforce_summaries',
    'user': 'colehorsman',
    'port': 5432
}

def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(**DB_CONFIG)

def fix_linkedin_urls():
    """Fix specific LinkedIn URLs that need correction."""
    
    # Manual corrections for LinkedIn URLs
    corrections = {
        "Cole Horseman": "https://linkedin.com/in/cole-horsman",  # Fixed transcript error
        # Add more corrections here as needed:
        # "Speaker Name": "https://linkedin.com/in/correct-url",
    }
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("🔧 Fixing LinkedIn URLs...")
    
    for speaker_name, correct_url in corrections.items():
        cursor.execute("""
            UPDATE summaries 
            SET linkedin_url = %s 
            WHERE speaker_name = %s
        """, (correct_url, speaker_name))
        
        if cursor.rowcount > 0:
            print(f"✅ Fixed {speaker_name} -> {correct_url}")
        else:
            print(f"⚠️  No records found for {speaker_name}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n✅ Fixed {len(corrections)} LinkedIn URLs")

if __name__ == "__main__":
    fix_linkedin_urls()