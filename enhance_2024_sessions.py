#!/usr/bin/env python3
"""
Batch processor to enhance 2024 sessions with same quality as 2025 sessions.
Adds formatted key_points and technical_details to match 2025 styling.
"""

import psycopg2
import openai
import os
import json
import time
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'reinforce_summaries',
    'user': 'colehorsman',
    'port': 5432
}

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def get_db_connection():
    """Get database connection."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def get_2024_sessions_needing_enhancement():
    """Get 2024 sessions that need key_points and technical_details enhancement."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        # Find 2024 sessions with poor or missing key_points/technical_details
        cursor.execute("""
            SELECT id, title, summary, author, domain, session_code, 
                   key_points, technical_details, full_transcript
            FROM summaries 
            WHERE year = 2024 
            AND (
                key_points IS NULL 
                OR technical_details IS NULL
                OR array_length(key_points, 1) < 3
                OR array_length(technical_details, 1) < 3
                OR key_points = '{}'::text[]
                OR technical_details = '{}'::text[]
            )
            ORDER BY domain, title
            LIMIT 10
        """)
        
        results = cursor.fetchall()
        sessions = []
        
        for row in results:
            sessions.append({
                'id': row[0],
                'title': row[1],
                'summary': row[2],
                'author': row[3],
                'domain': row[4],
                'session_code': row[5],
                'key_points': row[6],
                'technical_details': row[7],
                'full_transcript': row[8]
            })
        
        return sessions
        
    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return []
    finally:
        conn.close()

def enhance_session_with_ai(session):
    """Use AI to generate enhanced key_points and technical_details."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Create comprehensive prompt for enhancement
        prompt = f"""
Analyze this AWS re:Inforce 2024 security session and extract detailed key points and technical details.

**Session Details:**
Title: {session['title']}
Author: {session['author']}
Domain: {session['domain']}
Summary: {session['summary']}

**Current Transcript/Content:**
{session['full_transcript'][:3000] if session['full_transcript'] else 'No transcript available'}

**Task:** Extract 7-10 key strategic points and 7-15 technical implementation details that would be valuable for security professionals. Match the quality and formatting of re:Inforce 2025 sessions.

**Output Format:**
Return ONLY a JSON object with this exact structure:
{{
    "key_points": [
        "**Strategic Theme Title**: Detailed insight with specific value proposition and business impact",
        "**Security Relevance**: Comprehensive explanation of security implications with practical context",
        "**Implementation Impact**: Detailed guidance on practical application and deployment considerations",
        "**Future Direction**: Strategic implications for security teams and technology evolution",
        "**Business Value**: Quantifiable benefits and ROI considerations for security investments",
        "**Risk Mitigation**: Specific threat vectors addressed and security improvements achieved",
        "**Operational Excellence**: Process improvements and efficiency gains for security operations"
    ],
    "technical_details": [
        "**AWS Service Integration**: Specific service configurations and implementation patterns",
        "**Security Controls**: Detailed IAM policies, encryption settings, and access management",
        "**Architecture Patterns**: Infrastructure design recommendations and security architecture",
        "**Configuration Guidelines**: Step-by-step implementation with security best practices",
        "**Monitoring and Alerting**: Detection capabilities, logging configurations, and response procedures",
        "**Compliance Framework**: Regulatory alignment and audit trail requirements",
        "**Performance Optimization**: Security-performance balance and scalability considerations",
        "**Integration Patterns**: API security, data flow protection, and service mesh configurations"
    ]
}}

Focus on:
- Actionable insights for security teams
- Specific AWS services and features mentioned
- Implementation guidance and best practices
- Strategic security implications
- Technical architecture patterns
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AWS security expert analyzing re:Inforce session content. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content.strip()
        
        # Clean up any markdown formatting
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        enhancement_data = json.loads(content)
        
        return enhancement_data
        
    except Exception as e:
        print(f"Error enhancing session {session['id']}: {e}")
        return None

def update_session_in_database(session_id, enhancement_data):
    """Update session with enhanced key_points and technical_details."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Convert lists to PostgreSQL arrays
        key_points = enhancement_data['key_points']
        technical_details = enhancement_data['technical_details']
        
        cursor.execute("""
            UPDATE summaries 
            SET key_points = %s, 
                technical_details = %s
            WHERE id = %s
        """, (key_points, technical_details, session_id))
        
        conn.commit()
        print(f"✅ Updated session {session_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating session {session_id}: {e}")
        return False
    finally:
        conn.close()

def main():
    """Main batch processing function."""
    print("🚀 Starting 2024 Session Enhancement Batch Process")
    print("=" * 60)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        return
    
    # Get sessions needing enhancement
    sessions = get_2024_sessions_needing_enhancement()
    
    if not sessions:
        print("✅ No 2024 sessions need enhancement!")
        return
    
    print(f"📊 Found {len(sessions)} sessions needing enhancement")
    print()
    
    successful_updates = 0
    failed_updates = 0
    
    for i, session in enumerate(sessions, 1):
        print(f"🔄 Processing {i}/{len(sessions)}: {session['title'][:60]}...")
        
        # Enhance with AI
        enhancement_data = enhance_session_with_ai(session)
        
        if enhancement_data:
            # Update database
            if update_session_in_database(session['id'], enhancement_data):
                successful_updates += 1
                print(f"   ✅ Enhanced with {len(enhancement_data['key_points'])} key points and {len(enhancement_data['technical_details'])} technical details")
            else:
                failed_updates += 1
        else:
            failed_updates += 1
            print(f"   ❌ Failed to enhance")
        
        # Rate limiting - pause between requests
        if i < len(sessions):
            print("   ⏳ Waiting 2 seconds...")
            time.sleep(2)
        
        print()
    
    print("=" * 60)
    print("📈 Batch Processing Complete!")
    print(f"✅ Successfully enhanced: {successful_updates} sessions")
    print(f"❌ Failed to enhance: {failed_updates} sessions")
    print(f"📊 Total processed: {len(sessions)} sessions")

if __name__ == "__main__":
    main()