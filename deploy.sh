#!/bin/bash

# Wakfu Builder - Quick Deployment Script
# This script helps you deploy to different platforms

set -e

echo "🚀 Wakfu Builder Deployment Helper"
echo "===================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Initializing..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
    echo "✅ Git initialized"
fi

echo ""
echo "Select your deployment platform:"
echo "1) Render.com (Recommended - Easiest & Free)"
echo "2) Railway.app (Better Performance - $5 free credits)"
echo "3) Fly.io (Most Free Resources)"
echo "4) Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📦 Deploying to Render.com..."
        echo ""
        echo "Steps:"
        echo "1. Push your code to GitHub (if not already)"
        echo "2. Go to https://render.com"
        echo "3. Click 'New +' → 'Blueprint'"
        echo "4. Connect your GitHub repo"
        echo "5. Render will detect render.yaml automatically"
        echo ""
        read -p "Do you want to push to GitHub now? (y/n): " push_git
        if [ "$push_git" = "y" ]; then
            read -p "Enter your GitHub repository URL: " repo_url
            git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"
            git branch -M main
            git push -u origin main
            echo "✅ Pushed to GitHub!"
            echo ""
            echo "Now go to https://render.com and follow the steps above"
        fi
        ;;
    2)
        echo ""
        echo "🚂 Deploying to Railway.app..."
        echo ""
        
        # Check if Railway CLI is installed
        if ! command -v railway &> /dev/null; then
            echo "Railway CLI not found. Installing..."
            npm install -g @railway/cli
        fi
        
        echo "Logging in to Railway..."
        railway login
        
        echo "Initializing project..."
        railway init
        
        echo "Adding PostgreSQL database..."
        railway add --database postgres
        
        echo "Deploying services..."
        railway up
        
        echo "✅ Deployed to Railway!"
        echo "Open dashboard to configure environment variables:"
        railway open
        ;;
    3)
        echo ""
        echo "🪰 Deploying to Fly.io..."
        echo ""
        
        # Check if Fly CLI is installed
        if ! command -v fly &> /dev/null; then
            echo "❌ Fly CLI not found."
            echo "Install it from: https://fly.io/docs/hands-on/install-flyctl/"
            echo ""
            echo "For Windows (PowerShell):"
            echo "  iwr https://fly.io/install.ps1 -useb | iex"
            echo ""
            echo "For Mac/Linux:"
            echo "  curl -L https://fly.io/install.sh | sh"
            exit 1
        fi
        
        echo "Logging in to Fly.io..."
        fly auth login
        
        echo ""
        echo "Creating PostgreSQL database..."
        read -p "Enter database name (default: wakfu-db): " db_name
        db_name=${db_name:-wakfu-db}
        fly postgres create --name "$db_name" --region iad
        
        echo ""
        echo "Deploying API..."
        cd api
        fly launch --name wakfu-api --region iad --no-deploy
        fly deploy
        cd ..
        
        echo ""
        echo "Deploying Frontend..."
        cd frontend
        fly launch --name wakfu-frontend --region iad --no-deploy
        fly deploy
        cd ..
        
        echo ""
        echo "Deploying Worker..."
        cd worker
        fly launch --name wakfu-worker --region iad --no-deploy
        fly deploy
        cd ..
        
        echo "✅ Deployed to Fly.io!"
        ;;
    4)
        echo "Goodbye! 👋"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process completed!"
echo ""
echo "📝 Next steps:"
echo "1. Check your platform dashboard for service URLs"
echo "2. Update environment variables if needed"
echo "3. Test your application"
echo "4. Set up monitoring (UptimeRobot for Render)"
echo ""
echo "📖 For detailed instructions, see:"
echo "  - QUICK_DEPLOY.md (quick start)"
echo "  - DEPLOYMENT_GUIDE.md (detailed guide)"

