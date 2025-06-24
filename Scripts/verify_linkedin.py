#!/usr/bin/env python3
"""
LinkedIn URL Verification Tool
Helps identify which LinkedIn URLs need manual correction
"""

import psycopg2
import requests
import time

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

def check_linkedin_url(url, timeout=5):
    """
    Check if a LinkedIn URL exists.
    Returns: 'valid', 'invalid', or 'unknown'
    """
    try:
        # Simple HTTP HEAD request to check if URL exists
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return 'valid'
        elif response.status_code == 404:
            return 'invalid'
        else:
            return 'unknown'
    except:
        return 'unknown'

def verify_linkedin_profiles(check_urls=False):
    """
    Verify LinkedIn profiles and identify potential issues.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT speaker_name, linkedin_url 
        FROM summaries 
        WHERE speaker_name IS NOT NULL AND linkedin_url IS NOT NULL
        ORDER BY speaker_name
    """)
    
    profiles = cursor.fetchall()
    
    print(f"🔍 Analyzing {len(profiles)} LinkedIn profiles...")
    print("=" * 60)
    
    # Categorize profiles
    likely_issues = []
    verified_manual = []
    auto_generated = []
    
    # Known manual corrections (these should work)
    manual_corrections = ['colep', 'cole-horsman']
    
    for speaker_name, linkedin_url in profiles:
        # Extract username from URL
        username = linkedin_url.split('/in/')[-1].split('?')[0]
        
        # Check if this is a manual correction
        if any(manual in linkedin_url for manual in manual_corrections):
            verified_manual.append((speaker_name, linkedin_url))
        # Check for potential issues
        elif (
            len(username) > 20 or  # Very long usernames are less likely
            username.count('-') > 2 or  # Too many hyphens
            any(char.isdigit() for char in username)  # Numbers in username
        ):
            likely_issues.append((speaker_name, linkedin_url))
        else:
            auto_generated.append((speaker_name, linkedin_url))
        
        # Optional: Actually check URLs (rate limited)
        if check_urls:
            status = check_linkedin_url(linkedin_url)
            if status == 'invalid':
                print(f"❌ BROKEN: {speaker_name} -> {linkedin_url}")
            elif status == 'valid':
                print(f"✅ WORKS: {speaker_name} -> {linkedin_url}")
            time.sleep(1)  # Rate limiting
    
    # Summary report
    print(f"\n📊 LinkedIn Profile Analysis:")
    print(f"   Total profiles: {len(profiles)}")
    print(f"   ✅ Verified manual: {len(verified_manual)}")
    print(f"   🤖 Auto-generated: {len(auto_generated)}")
    print(f"   ⚠️  Likely issues: {len(likely_issues)}")
    
    if verified_manual:
        print(f"\n✅ Manually Verified Profiles:")
        for speaker, url in verified_manual[:5]:
            print(f"   {speaker}: {url}")
    
    if likely_issues:
        print(f"\n⚠️  Profiles That May Need Manual Correction:")
        for speaker, url in likely_issues[:10]:
            username = url.split('/in/')[-1]
            print(f"   {speaker}: {username}")
    
    # Suggest next steps
    print(f"\n💡 Recommendations:")
    print(f"   • Test the 'Likely issues' profiles manually")
    print(f"   • Add working URLs to manual_linkedin_corrections()")
    print(f"   • Run with --check-urls to verify actual URL status")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    import sys
    check_urls = '--check-urls' in sys.argv
    
    print("🔍 LinkedIn Profile Verification Tool")
    print("=" * 50)
    
    verify_linkedin_profiles(check_urls=check_urls)
    
    if not check_urls:
        print(f"\n💡 To check actual URL status, run:")
        print(f"   python3 Scripts/verify_linkedin.py --check-urls")