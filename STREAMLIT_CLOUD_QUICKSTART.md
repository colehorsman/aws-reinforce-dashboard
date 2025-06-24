# Streamlit Cloud Quick Start Guide

## 1. Database Setup (Choose One)

### Option A: Supabase (Recommended - Free)
1. Go to https://supabase.com and create account
2. Create new project (remember your password!)
3. Go to Settings > Database
4. Copy connection string (looks like: postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres)
5. In SQL Editor, create the summaries table:

```sql
CREATE TABLE summaries (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    domain VARCHAR(100),
    title TEXT,
    session_code VARCHAR(50),
    author TEXT,
    duration VARCHAR(50),
    word_count INTEGER,
    publish_date DATE,
    video_id VARCHAR(50),
    video_url TEXT,
    summary TEXT,
    key_points TEXT,
    technical_details TEXT,
    full_transcript TEXT,
    file_path TEXT,
    speaker_name VARCHAR(255),
    speaker_company VARCHAR(255),
    speaker_linkedin_url VARCHAR(500)
);
```

6. Import data using the CSV file (summaries_export.csv)

### Option B: Neon (Alternative - Free)
1. Go to https://neon.tech and create account
2. Create new project
3. Get connection string from Dashboard
4. Create table and import data similarly

## 2. Streamlit Cloud Deployment

1. **Fork or push this repository to your GitHub**

2. **Go to https://share.streamlit.io**
   - Sign in with GitHub
   - Click "New app"

3. **Deploy your app:**
   - Repository: Your GitHub repo
   - Branch: main
   - Main file path: streamlit_app.py

4. **Add Secrets (Important!):**
   - Click "Advanced settings"
   - Add secrets in TOML format:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"

[postgres]
host = "db.xxxxx.supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = "your-password-here"
```

5. **Click Deploy!**

## 3. Post-Deployment Checklist

- [ ] Test AI search functionality
- [ ] Verify all charts load correctly
- [ ] Check speaker profiles work
- [ ] Test data export features
- [ ] Share your app URL!

## 4. Troubleshooting

### Common Issues:

**Database connection fails:**
- Double-check your connection string
- Ensure database is publicly accessible
- Verify credentials in secrets

**OpenAI API errors:**
- Verify API key is correct
- Check OpenAI account has credits
- Ensure key has proper permissions

**App crashes or restarts:**
- Check Streamlit Cloud logs
- Reduce memory usage if needed
- Ensure all dependencies in requirements.txt

## 5. Your App URL

Once deployed, your app will be available at:
`https://[your-github-username]-[repo-name]-[branch].streamlit.app`

Share this URL with stakeholders!