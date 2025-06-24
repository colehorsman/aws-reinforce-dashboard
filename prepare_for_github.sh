#!/bin/bash

echo "🧹 Preparing clean repository for GitHub..."

# Create a temporary directory for clean export
TEMP_DIR="../reinforce-2025-clean"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR

# Copy only necessary files (excluding sensitive data)
echo "📁 Copying essential files..."

# Core application files
cp -r Dashboards $TEMP_DIR/
cp streamlit_app.py $TEMP_DIR/
cp requirements.txt $TEMP_DIR/
cp README.md $TEMP_DIR/

# Documentation
cp STREAMLIT_DEPLOYMENT.md $TEMP_DIR/
cp STREAMLIT_CLOUD_QUICKSTART.md $TEMP_DIR/

# Create directories for organization
mkdir -p $TEMP_DIR/2024
mkdir -p $TEMP_DIR/2025
mkdir -p $TEMP_DIR/Scripts
mkdir -p $TEMP_DIR/Docs

# Copy .gitignore
cp .gitignore $TEMP_DIR/

# Create a clean secrets example
cat > $TEMP_DIR/.streamlit/secrets.toml.example << 'EOF'
# Example secrets file for Streamlit Cloud
# Copy this content to Streamlit secrets (do not commit!)

[postgres]
host = "aws-0-us-east-1.pooler.supabase.com"
port = 5432
database = "postgres"
user = "postgres.tpjpvthtomffzafgzynk"
password = "your-database-password"

OPENAI_API_KEY = "your-openai-api-key"
EOF

# Create deployment instructions
cat > $TEMP_DIR/DEPLOY.md << 'EOF'
# Quick Deployment Guide

## Prerequisites
✅ Supabase database already set up with data
✅ OpenAI API key ready

## Deploy to Streamlit Cloud

1. Fork or clone this repository
2. Go to https://share.streamlit.io
3. Create new app with:
   - Repository: Your fork
   - Branch: main
   - Main file: streamlit_app.py

4. Add secrets in Advanced Settings:
```toml
[postgres]
host = "aws-0-us-east-1.pooler.supabase.com"
port = 5432
database = "postgres"
user = "postgres.tpjpvthtomffzafgzynk"
password = "thisisthedatabasepassword"

OPENAI_API_KEY = "your-actual-openai-key"
```

5. Deploy!

Your app will be live at:
https://[username]-reinforce-2025-summaries.streamlit.app
EOF

echo "✅ Clean repository prepared at: $TEMP_DIR"
echo ""
echo "📋 Next steps:"
echo "1. cd $TEMP_DIR"
echo "2. git init"
echo "3. git add ."
echo "4. git commit -m 'Initial commit - AWS re:Inforce Analytics Platform'"
echo "5. Create repo on GitHub"
echo "6. git remote add origin https://github.com/YOUR_USERNAME/reinforce-analytics.git"
echo "7. git push -u origin main"