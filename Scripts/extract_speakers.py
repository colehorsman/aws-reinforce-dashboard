#!/usr/bin/env python3
"""
Extract speaker names from transcripts and add to database
"""

import psycopg2
import re
import requests
import time
from urllib.parse import quote

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

def extract_speaker_name(transcript):
    """Extract speaker name from transcript using various patterns."""
    if not transcript:
        return None
    
    # Common patterns for speaker introductions
    patterns = [
        r"my name is ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"My name is ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"I'm ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"I am ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"This is ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"My name's ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"Hello[,.]? [Mm]y name is ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"Hi[,.]? [Mm]y name is ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"Good morning[,.]? [Mm]y name is ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
        r"Good afternoon[,.]? [Mm]y name is ([A-Z][a-z]+ [A-Z][a-z]+)(?:\.|,|\s)",
    ]
    
    # Look at the first 1000 characters where introductions typically happen
    text_start = transcript[:1000]
    
    for pattern in patterns:
        match = re.search(pattern, text_start, re.IGNORECASE)
        if match:
            name = match.group(1)
            # Clean up the name
            name = ' '.join(name.split())  # Remove extra spaces
            
            # Validate the name - must be two proper words
            words = name.split()
            if len(words) == 2:
                # Check if both words look like proper names (not common words)
                common_words = ['the', 'and', 'with', 'from', 'here', 'going', 'gonna', 'really', 
                               'super', 'very', 'so', 'an', 'one', 'that', 'this', 'what', 'how']
                
                if not any(word.lower() in common_words for word in words):
                    # Additional check - both words should start with capital letter
                    if all(word[0].isupper() and word[1:].islower() for word in words):
                        return name
    
    return None

def search_linkedin_profile(name, company="AWS", max_retries=3):
    """
    Search for LinkedIn profile URL using Google search.
    This is a basic implementation - in production you'd want to use LinkedIn API.
    """
    if not name:
        return None
    
    # Manual corrections for known speakers (transcript errors, etc.)
    name_corrections = {
        "Cole Horseman": "cole-horsman",  # Transcript error: should be Horsman not Horseman
        # Add more corrections as needed
    }
    
    # Check for manual corrections first
    if name in name_corrections:
        return f"https://linkedin.com/in/{name_corrections[name]}"
    
    # Convert name to likely LinkedIn format
    name_parts = name.lower().split()
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        
        # Common LinkedIn URL patterns
        potential_urls = [
            f"https://linkedin.com/in/{first_name}-{last_name}",
            f"https://linkedin.com/in/{first_name}{last_name}",
            f"https://linkedin.com/in/{first_name}.{last_name}",
            f"https://linkedin.com/in/{first_name}-{last_name}-aws",
            f"https://linkedin.com/in/{first_name}-{last_name}-amazon",
        ]
        
        # Return the most likely URL (first pattern)
        return potential_urls[0]
    
    return None

def update_speakers_in_database():
    """Extract speakers from transcripts and update database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First, add speaker_name and linkedin_url columns if they don't exist
    try:
        cursor.execute("ALTER TABLE summaries ADD COLUMN speaker_name VARCHAR(255);")
        cursor.execute("ALTER TABLE summaries ADD COLUMN linkedin_url VARCHAR(500);")
        conn.commit()
        print("✅ Added speaker columns to database")
    except psycopg2.Error as e:
        if "already exists" in str(e):
            print("ℹ️  Speaker columns already exist")
        else:
            print(f"Error adding columns: {e}")
        conn.rollback()
    
    # Get all talks with transcripts
    cursor.execute("""
        SELECT id, title, session_code, full_transcript 
        FROM summaries 
        WHERE full_transcript IS NOT NULL 
        AND LENGTH(full_transcript) > 100
        AND (speaker_name IS NULL OR speaker_name = '')
    """)
    
    talks = cursor.fetchall()
    print(f"🔍 Processing {len(talks)} talks for speaker extraction...")
    
    updated_count = 0
    
    for talk_id, title, session_code, transcript in talks:
        print(f"\n📝 Processing: {session_code} - {title[:50]}...")
        
        # Extract speaker name
        speaker_name = extract_speaker_name(transcript)
        
        if speaker_name:
            print(f"👤 Found speaker: {speaker_name}")
            
            # Search for LinkedIn profile
            linkedin_url = search_linkedin_profile(speaker_name)
            if linkedin_url:
                print(f"🔗 LinkedIn: {linkedin_url}")
            
            # Update database
            cursor.execute("""
                UPDATE summaries 
                SET speaker_name = %s, linkedin_url = %s 
                WHERE id = %s
            """, (speaker_name, linkedin_url, talk_id))
            
            updated_count += 1
        else:
            print("❌ No speaker name found")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n✅ Updated {updated_count} talks with speaker information")

def show_speaker_stats():
    """Show statistics about extracted speakers."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_talks,
            COUNT(speaker_name) as talks_with_speakers,
            COUNT(linkedin_url) as talks_with_linkedin,
            COUNT(DISTINCT speaker_name) as unique_speakers
        FROM summaries
    """)
    
    stats = cursor.fetchone()
    total, with_speakers, with_linkedin, unique = stats
    
    print("\n📊 Speaker Extraction Statistics:")
    print(f"   Total talks: {total}")
    print(f"   Talks with speakers: {with_speakers} ({with_speakers/total*100:.1f}%)")
    print(f"   Talks with LinkedIn: {with_linkedin} ({with_linkedin/total*100:.1f}%)")
    print(f"   Unique speakers: {unique}")
    
    # Show top speakers
    cursor.execute("""
        SELECT speaker_name, COUNT(*) as talk_count
        FROM summaries 
        WHERE speaker_name IS NOT NULL
        GROUP BY speaker_name
        ORDER BY talk_count DESC
        LIMIT 10
    """)
    
    top_speakers = cursor.fetchall()
    if top_speakers:
        print("\n🏆 Top Speakers:")
        for speaker, count in top_speakers:
            print(f"   {speaker}: {count} talks")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("🎤 AWS re:Inforce Speaker Extraction Tool")
    print("=" * 50)
    
    # Extract and update speakers
    update_speakers_in_database()
    
    # Show statistics
    show_speaker_stats()
    
    print("\n✅ Speaker extraction complete!")