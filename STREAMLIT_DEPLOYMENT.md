# Streamlit Cloud Deployment Guide

## Overview
This guide will help you deploy the AWS re:Inforce Analytics Platform to Streamlit Cloud.

## Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)
- PostgreSQL database (we'll use Supabase or Neon for free hosting)

## Step 1: Database Migration
Since Streamlit Cloud doesn't support local PostgreSQL, we need to migrate to a cloud database.

### Option A: Supabase (Recommended - Free Tier)
1. Create account at https://supabase.com
2. Create new project
3. Get connection string from Settings > Database

### Option B: Neon (Alternative - Free Tier)
1. Create account at https://neon.tech
2. Create new project
3. Get connection string

## Step 2: Export Current Data
```bash
# Export current PostgreSQL data
pg_dump -h localhost -U colehorsman -d reinforce_summaries > reinforce_backup.sql

# Or export as CSV
psql -h localhost -U colehorsman -d reinforce_summaries -c "\COPY summaries TO 'summaries.csv' WITH CSV HEADER"
```

## Step 3: Prepare Repository for Streamlit Cloud

### Required Files Structure:
```
reinforce-2025-summaries/
├── streamlit_app.py          # Main app file (required)
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── secrets.toml         # Secret configuration (local only)
└── Dashboards/
    └── ciso_dashboard.py    # Your existing dashboard
```

## Step 4: Environment Variables
Create `.streamlit/secrets.toml` for local testing (DO NOT commit this file):

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-openai-api-key"

[postgres]
host = "your-cloud-db-host"
port = 5432
database = "postgres"
user = "postgres"
password = "your-password"
```

## Step 5: Update Database Connection
Update the database connection in your dashboard to use Streamlit secrets:

```python
import streamlit as st

def get_db_connection():
    if 'postgres' in st.secrets:
        # Production (Streamlit Cloud)
        return psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"]
        )
    else:
        # Local development
        return psycopg2.connect(
            host='localhost',
            database='reinforce_summaries',
            user='colehorsman',
            port=5432
        )
```

## Step 6: Create Main App File
Create `streamlit_app.py` in the root directory:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run your dashboard
from Dashboards.ciso_dashboard import main

if __name__ == "__main__":
    main()
```

## Step 7: Deploy to Streamlit Cloud

1. Push your code to GitHub (without secrets.toml)
2. Go to https://share.streamlit.io
3. Click "New app"
4. Connect your GitHub repository
5. Select branch, and set main file path to `streamlit_app.py`
6. Click "Advanced settings"
7. Add your secrets (OPENAI_API_KEY and postgres credentials)
8. Deploy!

## Step 8: Post-Deployment

1. Test all features
2. Share the public URL
3. Monitor usage in Streamlit Cloud dashboard

## Security Notes
- Never commit `.streamlit/secrets.toml` to GitHub
- Use `.gitignore` to exclude sensitive files
- Rotate API keys regularly
- Use read-only database user if possible

## Limitations of Streamlit Cloud
- 1GB memory limit
- No persistent storage
- Restarts after inactivity
- Limited compute resources

## Cost Comparison
- Streamlit Cloud: FREE
- Supabase/Neon: FREE (with limits)
- Total: $0/month for basic usage