# Wakfu Builder - Quick Deployment Script (PowerShell)
# This script helps you deploy to different platforms on Windows

Write-Host "🚀 Wakfu Builder Deployment Helper" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-Not (Test-Path .git)) {
    Write-Host "❌ Git not initialized. Initializing..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for deployment"
    Write-Host "✅ Git initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Select your deployment platform:"
Write-Host "1) Render.com (Recommended - Easiest & Free)"
Write-Host "2) Railway.app (Better Performance - `$5 free credits)"
Write-Host "3) Fly.io (Most Free Resources)"
Write-Host "4) Exit"
Write-Host ""
$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "📦 Deploying to Render.com..." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Steps:"
        Write-Host "1. Push your code to GitHub (if not already)"
        Write-Host "2. Go to https://render.com"
        Write-Host "3. Click 'New +' → 'Blueprint'"
        Write-Host "4. Connect your GitHub repo"
        Write-Host "5. Render will detect render.yaml automatically"
        Write-Host ""
        $pushGit = Read-Host "Do you want to push to GitHub now? (y/n)"
        if ($pushGit -eq "y") {
            $repoUrl = Read-Host "Enter your GitHub repository URL"
            try {
                git remote add origin $repoUrl 2>$null
            } catch {
                git remote set-url origin $repoUrl
            }
            git branch -M main
            git push -u origin main
            Write-Host "✅ Pushed to GitHub!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Now go to https://render.com and follow the steps above"
        }
    }
    "2" {
        Write-Host ""
        Write-Host "🚂 Deploying to Railway.app..." -ForegroundColor Cyan
        Write-Host ""
        
        # Check if Railway CLI is installed
        if (-Not (Get-Command railway -ErrorAction SilentlyContinue)) {
            Write-Host "Railway CLI not found. Installing..." -ForegroundColor Yellow
            npm install -g @railway/cli
        }
        
        Write-Host "Logging in to Railway..."
        railway login
        
        Write-Host "Initializing project..."
        railway init
        
        Write-Host "Adding PostgreSQL database..."
        railway add --database postgres
        
        Write-Host "Deploying services..."
        railway up
        
        Write-Host "✅ Deployed to Railway!" -ForegroundColor Green
        Write-Host "Opening dashboard..."
        railway open
    }
    "3" {
        Write-Host ""
        Write-Host "🪰 Deploying to Fly.io..." -ForegroundColor Cyan
        Write-Host ""
        
        # Check if Fly CLI is installed
        if (-Not (Get-Command fly -ErrorAction SilentlyContinue)) {
            Write-Host "❌ Fly CLI not found." -ForegroundColor Red
            Write-Host "Installing Fly CLI..."
            iwr https://fly.io/install.ps1 -useb | iex
            Write-Host "Please restart PowerShell and run this script again."
            exit 1
        }
        
        Write-Host "Logging in to Fly.io..."
        fly auth login
        
        Write-Host ""
        Write-Host "Creating PostgreSQL database..."
        $dbName = Read-Host "Enter database name (default: wakfu-db)"
        if ([string]::IsNullOrWhiteSpace($dbName)) {
            $dbName = "wakfu-db"
        }
        fly postgres create --name $dbName --region iad
        
        Write-Host ""
        Write-Host "Deploying API..."
        Set-Location api
        fly launch --name wakfu-api --region iad --no-deploy
        fly deploy
        Set-Location ..
        
        Write-Host ""
        Write-Host "Deploying Frontend..."
        Set-Location frontend
        fly launch --name wakfu-frontend --region iad --no-deploy
        fly deploy
        Set-Location ..
        
        Write-Host ""
        Write-Host "Deploying Worker..."
        Set-Location worker
        fly launch --name wakfu-worker --region iad --no-deploy
        fly deploy
        Set-Location ..
        
        Write-Host "✅ Deployed to Fly.io!" -ForegroundColor Green
    }
    "4" {
        Write-Host "Goodbye! 👋" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host "Invalid choice. Exiting." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Deployment process completed!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:"
Write-Host "1. Check your platform dashboard for service URLs"
Write-Host "2. Update environment variables if needed"
Write-Host "3. Test your application"
Write-Host "4. Set up monitoring (UptimeRobot for Render)"
Write-Host ""
Write-Host "📖 For detailed instructions, see:"
Write-Host "  - QUICK_DEPLOY.md (quick start)"
Write-Host "  - DEPLOYMENT_GUIDE.md (detailed guide)"

