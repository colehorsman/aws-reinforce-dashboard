#!/bin/bash

echo "🆕 Creating a BRAND NEW repository (NOT modifying the original)"
echo "=================================================="
echo ""

# Create a completely new directory OUTSIDE the current repo
NEW_REPO_PATH="$HOME/Desktop/my-reinforce-analytics"

echo "📁 Creating new directory at: $NEW_REPO_PATH"
echo "(This is OUTSIDE the original repository)"
echo ""

# Remove if exists and create fresh
rm -rf "$NEW_REPO_PATH"
mkdir -p "$NEW_REPO_PATH"

# Copy only the files we need (no .git folder!)
echo "📋 Copying clean files (no git history)..."
cp -r Dashboards "$NEW_REPO_PATH/"
cp streamlit_app.py "$NEW_REPO_PATH/"
cp requirements.txt "$NEW_REPO_PATH/"
cp README.md "$NEW_REPO_PATH/"
cp .gitignore "$NEW_REPO_PATH/"

# Create .streamlit directory
mkdir -p "$NEW_REPO_PATH/.streamlit"

echo ""
echo "✅ Clean files copied to new location"
echo ""
echo "🔒 This is a FRESH directory with:"
echo "   - NO git history"
echo "   - NO connection to the original repo"
echo "   - Ready for YOUR GitHub account"
echo ""
echo "📝 Next steps to create YOUR OWN repository:"
echo ""
echo "1. cd $NEW_REPO_PATH"
echo "2. git init                          # Start fresh git repo"
echo "3. git add ."
echo "4. git commit -m 'Initial commit'"
echo ""
echo "5. Go to YOUR GitHub account and create a new repo"
echo "6. git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo "7. git push -u origin main"
echo ""
echo "This will push to YOUR repository only!"