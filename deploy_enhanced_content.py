#!/usr/bin/env python3
"""
Deploy enhanced 2024 content to production database
"""
import psycopg2
import json
import os
from datetime import datetime

def get_database_connection(use_production=False):
    """Get database connection - local or production."""
    
    if use_production:
        # For production deployment - you'll need to set these environment variables
        # or modify this to use your production database credentials
        DB_CONFIG = {
            'host': os.getenv('PROD_DB_HOST', 'your-supabase-host.supabase.co'),
            'database': os.getenv('PROD_DB_NAME', 'postgres'),
            'user': os.getenv('PROD_DB_USER', 'postgres'),
            'password': os.getenv('PROD_DB_PASSWORD', 'your-password'),
            'port': int(os.getenv('PROD_DB_PORT', '5432'))
        }
    else:
        # Local development
        DB_CONFIG = {
            'host': 'localhost',
            'database': 'reinforce_summaries',
            'user': 'colehorsman',
            'port': 5432
        }
    
    return psycopg2.connect(**DB_CONFIG)

def check_production_database_status():
    """Check the current state of 2024 sessions in production."""
    
    print("🔍 Checking production database status...")
    
    try:
        conn = get_database_connection(use_production=True)
        cursor = conn.cursor()
        
        # Check total 2024 sessions
        cursor.execute("""
            SELECT 
                COUNT(*) as total_2024,
                COUNT(CASE WHEN key_points IS NOT NULL AND array_length(key_points, 1) > 0 THEN 1 END) as with_key_points,
                COUNT(CASE WHEN technical_details IS NOT NULL AND array_length(technical_details, 1) > 0 THEN 1 END) as with_tech_details
            FROM summaries 
            WHERE year = 2024
        """)
        
        total, with_key_points, with_tech_details = cursor.fetchone()
        
        print(f"📊 Production Database Status:")
        print(f"• Total 2024 sessions: {total}")
        print(f"• Sessions with key_points: {with_key_points} ({with_key_points/total*100:.1f}% if total > 0 else 0%)")
        print(f"• Sessions with technical_details: {with_tech_details} ({with_tech_details/total*100:.1f}% if total > 0 else 0%)")
        
        # Check specific session mentioned by user
        cursor.execute("""
            SELECT title, key_points, technical_details
            FROM summaries 
            WHERE title ILIKE '%5 ways generative AI can enhance cybersecurity%'
            AND year = 2024
        """)
        
        specific_result = cursor.fetchone()
        if specific_result:
            title, key_points, tech_details = specific_result
            print(f"\n🎯 Specific session check:")
            print(f"• '{title[:50]}...'")
            print(f"• Has key_points: {'✅' if key_points and len(key_points) > 0 else '❌'}")
            print(f"• Has technical_details: {'✅' if tech_details and len(tech_details) > 0 else '❌'}")
        else:
            print("\n❌ Specific session not found in production")
        
        conn.close()
        return total, with_key_points, with_tech_details
        
    except Exception as e:
        print(f"❌ Failed to check production database: {e}")
        print("💡 Make sure to set production database environment variables:")
        print("   export PROD_DB_HOST=your-supabase-host.supabase.co")
        print("   export PROD_DB_PASSWORD=your-password")
        return None, None, None

def deploy_enhanced_content_to_production():
    """Deploy the enhanced content to production database."""
    
    print("🚀 Starting deployment of enhanced 2024 content...")
    
    # Load the enhanced content
    try:
        with open('/Users/colehorsman/reinforce-2025-summaries/enhanced_2024_backup.json', 'r') as f:
            backup_data = json.load(f)
        
        sessions = backup_data['sessions']
        print(f"📦 Loaded {len(sessions)} enhanced sessions from backup")
        
    except Exception as e:
        print(f"❌ Failed to load enhanced content backup: {e}")
        return False
    
    # Connect to production database
    try:
        conn = get_database_connection(use_production=True)
        cursor = conn.cursor()
        print("✅ Connected to production database")
        
    except Exception as e:
        print(f"❌ Failed to connect to production database: {e}")
        return False
    
    # Deploy the updates
    successful_updates = 0
    failed_updates = 0
    
    try:
        for session in sessions:
            try:
                # Convert Python lists to PostgreSQL arrays
                key_points_array = session['key_points']
                tech_details_array = session['technical_details']
                
                cursor.execute("""
                    UPDATE summaries 
                    SET 
                        key_points = %s,
                        technical_details = %s
                    WHERE id = %s AND year = 2024
                """, (key_points_array, tech_details_array, session['id']))
                
                if cursor.rowcount > 0:
                    successful_updates += 1
                else:
                    print(f"⚠️ No rows updated for session ID {session['id']}: {session['title'][:50]}...")
                    failed_updates += 1
                
            except Exception as e:
                print(f"❌ Failed to update session {session['id']}: {e}")
                failed_updates += 1
        
        # Commit all updates
        conn.commit()
        print(f"✅ Successfully updated {successful_updates} sessions")
        if failed_updates > 0:
            print(f"❌ Failed to update {failed_updates} sessions")
        
        conn.close()
        return successful_updates > 0
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        conn.rollback()
        conn.close()
        return False

def main():
    """Main deployment function."""
    
    print("🔄 Enhanced 2024 Content Deployment")
    print("=" * 50)
    
    # Step 1: Check current production status
    total, with_key_points, with_tech_details = check_production_database_status()
    
    if total is None:
        print("\n❌ Cannot proceed without production database access")
        print("\n💡 To set up production database access:")
        print("1. Get your Supabase database credentials from Streamlit Cloud secrets")
        print("2. Set environment variables:")
        print("   export PROD_DB_HOST=your-supabase-host.supabase.co")
        print("   export PROD_DB_PASSWORD=your-password")
        print("3. Run this script again")
        return
    
    # Step 2: Determine if deployment is needed
    if with_key_points >= total * 0.9:  # 90% or more already enhanced
        print(f"\n✅ Production database already has {with_key_points}/{total} enhanced sessions")
        response = input("Do you want to proceed with deployment anyway? (y/N): ")
        if response.lower() != 'y':
            print("Deployment cancelled")
            return
    else:
        print(f"\n🚨 Production database needs enhancement: {with_key_points}/{total} sessions have enhanced content")
        response = input("Proceed with deployment? (Y/n): ")
        if response.lower() == 'n':
            print("Deployment cancelled")
            return
    
    # Step 3: Deploy the enhanced content
    if deploy_enhanced_content_to_production():
        print("\n🎉 Deployment completed successfully!")
        print("📊 Run status check again to verify deployment...")
        check_production_database_status()
    else:
        print("\n❌ Deployment failed")

if __name__ == "__main__":
    main()