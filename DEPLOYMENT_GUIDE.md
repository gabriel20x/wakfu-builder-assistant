# Wakfu Builder - Free Deployment Guide

## 🎯 Best Free Options

### Option 1: Render.com (Recommended - Easiest)
- ✅ Free PostgreSQL database
- ✅ Multiple services
- ✅ Auto-deploy from GitHub
- ⚠️ Database expires after 90 days (can recreate)
- ⚠️ Services sleep after 15 min of inactivity

### Option 2: Railway.app
- ✅ $5/month free credits
- ✅ Better database persistence
- ⚠️ Credits can run out quickly

### Option 3: Fly.io
- ✅ Most generous free tier
- ✅ Better performance
- ⚠️ More complex setup

---

## 🚀 Deployment Instructions

## A) Deploy to Render.com (Easiest)

### Prerequisites
1. GitHub account
2. Render.com account (free)

### Steps

#### 1. Push your code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/wakfu-builder-assistant.git
git push -u origin main
```

#### 2. Update Dockerfiles for Production

**Update `frontend/Dockerfile`:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Create `frontend/nginx.conf`:**
```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass ${VITE_API_URL};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Update `api/Dockerfile` for production:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

COPY . .

EXPOSE 8000

# Production command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

#### 3. Deploy on Render.com

**Option A: Using Blueprint (render.yaml)**
1. Go to [render.com](https://render.com)
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect `render.yaml` and create all services
5. Review and create

**Option B: Manual Setup**
1. Create PostgreSQL database first
2. Create 3 Web Services (API, Frontend)
3. Create 1 Background Worker
4. Set environment variables for each

---

## B) Deploy to Railway.app

### Steps

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and initialize:
```bash
railway login
railway init
```

3. Create services:
```bash
# Create database
railway add --database postgres

# Deploy services
railway up
```

4. Link services in Railway dashboard and set environment variables

---

## C) Deploy to Fly.io

### Steps

1. Install Fly CLI:
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

2. Login:
```bash
fly auth login
```

3. Create apps:
```bash
# Create database
fly postgres create --name wakfu-db --region iad

# Create and deploy API
cd api
fly launch --name wakfu-api --region iad
fly deploy

# Create and deploy Frontend
cd ../frontend
fly launch --name wakfu-frontend --region iad
fly deploy

# Create and deploy Worker
cd ../worker
fly launch --name wakfu-worker --region iad
fly deploy
```

---

## 📝 Important Notes

### For Render.com:
- ⚠️ Free services sleep after 15 minutes of inactivity (50-second cold start)
- ⚠️ Free PostgreSQL expires after 90 days (backup and recreate)
- ⚠️ Limited to 750 hours/month per service
- 💡 Keep services awake: use UptimeRobot or Cron-job.org to ping every 10 minutes

### For Railway:
- ⚠️ $5 free credits can run out quickly with all services
- 💡 Monitor usage in dashboard
- 💡 Stop services when not needed

### For Fly.io:
- ✅ Most generous free tier
- 💡 3 shared-cpu-1x 256MB VMs free
- 💡 160GB outbound transfer free

---

## 🔧 Environment Variables Setup

### API Service
```
DATABASE_URL=postgresql://user:password@host:port/database
CORS_ORIGINS=https://your-frontend.onrender.com
GAMEDATA_PATH=/wakfu_data/gamedata_1.90.1.43
```

### Frontend Service
```
VITE_API_URL=https://your-api.onrender.com
```

### Worker Service
```
DATABASE_URL=postgresql://user:password@host:port/database
GAMEDATA_PATH=/wakfu_data/gamedata_1.90.1.43
```

---

## 📦 Handling wakfu_data Folder

The `wakfu_data` folder contains game data. For deployment:

**Option 1**: Include in Git (if < 100MB)
**Option 2**: Download during build (recommended)
**Option 3**: Use cloud storage (S3, Cloudflare R2)

---

## ✅ Verification

After deployment:
1. Check API: `https://your-api.onrender.com/docs`
2. Check Frontend: `https://your-frontend.onrender.com`
3. Check logs for errors
4. Test database connection

---

## 🆘 Troubleshooting

### Services won't start:
- Check logs in Render/Railway/Fly dashboard
- Verify environment variables
- Check Docker build logs

### Database connection failed:
- Verify DATABASE_URL
- Check database is created and running
- Ensure worker/API depend on database

### Frontend can't reach API:
- Update CORS_ORIGINS in API
- Update VITE_API_URL in frontend
- Check network/firewall settings

---

## 💰 Cost Comparison

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| Render.com | Unlimited services (with limits) | Hobby projects |
| Railway.app | $5/month credits | Small apps |
| Fly.io | 3 VMs + DB | Production-ready apps |
| Vercel + Supabase | Frontend + DB free | JAMstack apps |

---

## 🎓 Recommendation

**For learning/hobby**: Use **Render.com** (easiest setup)
**For serious project**: Use **Fly.io** (better performance)
**For budget-conscious**: Use **Railway.app** (good balance)

---

## Need Help?

Feel free to ask if you encounter any issues during deployment!

