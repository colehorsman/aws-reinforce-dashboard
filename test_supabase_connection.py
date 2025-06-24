#!/usr/bin/env python3
"""
Test Supabase connections to find which one works
"""

import psycopg2
import socket

print("🔍 Testing Supabase Connection Methods")
print("=" * 50)

# Connection details
PASSWORD = "thisisthedatabasepassword"

# Method 1: Direct connection
print("\n1️⃣ Testing DIRECT connection:")
print("   Host: db.tpjpvthtomffzafgzynk.supabase.co")
print("   Port: 5432")

# First check if we can resolve the hostname
try:
    ip = socket.gethostbyname("db.tpjpvthtomffzafgzynk.supabase.co")
    print(f"   ✅ DNS resolved to: {ip}")
except:
    print("   ❌ Cannot resolve hostname")

# Try to connect
try:
    conn1 = psycopg2.connect(
        host="db.tpjpvthtomffzafgzynk.supabase.co",
        port=5432,
        database="postgres",
        user="postgres",
        password=PASSWORD
    )
    print("   ✅ DIRECT CONNECTION WORKS!")
    
    # Test query
    cur = conn1.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"   Database version: {version[0][:50]}...")
    
    conn1.close()
    CONNECTION_WORKS = "DIRECT"
    
except Exception as e:
    print(f"   ❌ Direct connection failed: {str(e)[:100]}...")
    CONNECTION_WORKS = None

# Method 2: Session pooler
print("\n2️⃣ Testing SESSION POOLER connection:")
print("   Host: aws-0-us-east-1.pooler.supabase.com")
print("   Port: 5432")
print("   User: postgres.tpjpvthtomffzafgzynk")

# Check DNS
try:
    ip = socket.gethostbyname("aws-0-us-east-1.pooler.supabase.com")
    print(f"   ✅ DNS resolved to: {ip}")
except:
    print("   ❌ Cannot resolve hostname")

# Try to connect
try:
    conn2 = psycopg2.connect(
        host="aws-0-us-east-1.pooler.supabase.com",
        port=5432,
        database="postgres",
        user="postgres.tpjpvthtomffzafgzynk",
        password=PASSWORD
    )
    print("   ✅ POOLER CONNECTION WORKS!")
    
    # Test query
    cur = conn2.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"   Database version: {version[0][:50]}...")
    
    conn2.close()
    if not CONNECTION_WORKS:
        CONNECTION_WORKS = "POOLER"
    
except Exception as e:
    print(f"   ❌ Pooler connection failed: {str(e)[:100]}...")

# Method 3: Try alternative pooler port
print("\n3️⃣ Testing SESSION POOLER with port 6543:")
print("   Host: aws-0-us-east-1.pooler.supabase.com")
print("   Port: 6543")

try:
    conn3 = psycopg2.connect(
        host="aws-0-us-east-1.pooler.supabase.com",
        port=6543,
        database="postgres",
        user="postgres.tpjpvthtomffzafgzynk",
        password=PASSWORD
    )
    print("   ✅ POOLER (6543) CONNECTION WORKS!")
    conn3.close()
    if not CONNECTION_WORKS:
        CONNECTION_WORKS = "POOLER_6543"
    
except Exception as e:
    print(f"   ❌ Pooler (6543) connection failed: {str(e)[:100]}...")

print("\n" + "=" * 50)

if CONNECTION_WORKS:
    print(f"\n✅ SUCCESS! Use the {CONNECTION_WORKS} connection method.")
    
    if CONNECTION_WORKS == "DIRECT":
        print("\n📋 Connection string for your code:")
        print(f'postgresql://postgres:{PASSWORD}@db.tpjpvthtomffzafgzynk.supabase.co:5432/postgres')
        
        print("\n📋 For Streamlit secrets.toml:")
        print("""[postgres]
host = "db.tpjpvthtomffzafgzynk.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "thisisthedatabasepassword" """)
        
    elif CONNECTION_WORKS == "POOLER":
        print("\n📋 Connection string for your code:")
        print(f'postgresql://postgres.tpjpvthtomffzafgzynk:{PASSWORD}@aws-0-us-east-1.pooler.supabase.com:5432/postgres')
        
        print("\n📋 For Streamlit secrets.toml:")
        print("""[postgres]
host = "aws-0-us-east-1.pooler.supabase.com"
port = 5432
database = "postgres"
user = "postgres.tpjpvthtomffzafgzynk"
password = "thisisthedatabasepassword" """)
        
else:
    print("\n❌ No connection methods worked!")
    print("\n🔧 Troubleshooting steps:")
    print("1. Check if your Supabase project is paused (Settings → General)")
    print("2. Verify the password is correct")
    print("3. Check if your IP needs to be whitelisted")
    print("4. Try using a VPN if you're on a restricted network")
    print("5. Wait a few minutes - new projects sometimes take time to activate")