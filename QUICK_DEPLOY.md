# ⚡ Quick Deploy Guide - Wakfu Builder

## 🚀 FASTEST Way to Deploy (5 minutes)

### Option 1: Render.com (Recommended for Beginners)

#### Step 1: Push to GitHub
```bash
# If not already initialized
git init
git add .
git commit -m "Ready for deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/wakfu-builder-assistant.git
git push -u origin main
```

#### Step 2: Deploy on Render
1. Go to https://render.com and sign up
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click **"Apply"** and wait 5-10 minutes

**That's it!** ✅

Your services will be at:
- Frontend: `https://wakfu-frontend.onrender.com`
- API: `https://wakfu-api.onrender.com`

---

### Option 2: Railway.app (Better Performance)

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Step 2: Deploy
```bash
# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add --database postgres

# Deploy
railway up

# Open dashboard
railway open
```

#### Step 3: Configure Services (in Railway Dashboard)
1. Add environment variables for each service
2. Link database to API and Worker
3. Deploy all services

---

### Option 3: Fly.io (Most Free Resources)

#### Step 1: Install Fly CLI (Windows)
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

#### Step 2: Create fly.toml files

Create `api/fly.toml`:
```toml
app = "wakfu-api"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

Create `frontend/fly.toml`:
```toml
app = "wakfu-frontend"

[build]
  dockerfile = "Dockerfile.prod"

[[services]]
  internal_port = 80
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

#### Step 3: Deploy
```bash
# Login
fly auth login

# Create and deploy database
fly postgres create --name wakfu-db

# Deploy API
cd api
fly launch --name wakfu-api
fly deploy

# Deploy Frontend
cd ../frontend
fly launch --name wakfu-frontend
fly deploy

# Deploy Worker
cd ../worker
fly launch --name wakfu-worker
fly deploy
```

---

## 🔑 Important Environment Variables

### For Production API
```env
DATABASE_URL=<from_render_or_railway>
CORS_ORIGINS=https://your-frontend-url.onrender.com,https://your-custom-domain.com
GAMEDATA_PATH=/wakfu_data/gamedata_1.90.1.43
```

### For Production Frontend
```env
VITE_API_URL=https://your-api-url.onrender.com
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: Services sleeping (Render.com)
**Solution**: Use [UptimeRobot](https://uptimerobot.com/) (free) to ping your app every 5 minutes

### Issue 2: Database connection timeout
**Solution**: Increase health check timeout in docker-compose.yml

### Issue 3: CORS errors
**Solution**: Add your frontend URL to CORS_ORIGINS in API env vars

### Issue 4: Build fails - not enough memory
**Solution**: 
- Reduce Docker image size
- Use multi-stage builds (already configured)
- Remove unused dependencies

### Issue 5: wakfu_data folder too large
**Solution**: 
```bash
# Option A: Don't commit large files
echo "wakfu_data/" >> .gitignore

# Option B: Use Git LFS
git lfs install
git lfs track "wakfu_data/**/*.json"
```

---

## 📊 Free Tier Limits Comparison

| Platform | Services | Database | Sleep? | Deploy Time |
|----------|----------|----------|--------|-------------|
| Render | Unlimited* | 90 days | After 15min | ~5 min |
| Railway | All | Permanent | No | ~3 min |
| Fly.io | 3 VMs | Paid** | No | ~10 min |

\* With limitations  
\** $0.15/GB/month (usually ~$1-2/month for small DB)

---

## 🎯 My Recommendation

**Just starting?** → **Render.com** (easiest, truly free)
**Need performance?** → **Railway.app** ($5 credits should last 1-2 months)
**Production app?** → **Fly.io** (best performance, small DB cost)

---

## 🆘 Need Help?

If something doesn't work:
1. Check the logs in the platform dashboard
2. Verify all environment variables are set
3. Make sure your wakfu_data folder is accessible
4. Check CORS settings

---

## ✨ Post-Deployment Checklist

- [ ] All services are running
- [ ] Database is connected
- [ ] Frontend loads correctly
- [ ] API responds to requests
- [ ] Worker has loaded game data
- [ ] CORS is configured correctly
- [ ] Set up UptimeRobot (for Render)
- [ ] Configure custom domain (optional)

---

**Ready to deploy?** Pick your platform and follow the steps above! 🚀

