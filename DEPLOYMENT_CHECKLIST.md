# ✅ Deployment Checklist - Wakfu Builder

## 🎯 Pre-Deployment (Do This First)

### Local Development
- [ ] Application runs locally with `docker-compose up`
- [ ] All services start without errors
- [ ] Can access frontend at http://localhost:5173
- [ ] Can access API at http://localhost:8000/docs
- [ ] Database is populated with game data
- [ ] No errors in browser console
- [ ] Can generate builds successfully

### Code Quality
- [ ] All tests pass (if you have tests)
- [ ] No linter errors
- [ ] Code is committed to Git
- [ ] .gitignore is configured properly

### Git & GitHub
- [ ] Git repository initialized
- [ ] All changes committed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub (`git push`)
- [ ] Repository is public (or connect private repo on platform)

### Environment Variables Documented
- [ ] Know what `DATABASE_URL` should be
- [ ] Know what `CORS_ORIGINS` should be
- [ ] Know what `VITE_API_URL` should be
- [ ] `GAMEDATA_PATH` configured

---

## 🚀 Deployment Process

### Choose Your Platform
- [ ] Decided on platform (Render/Railway/Fly.io)
- [ ] Created account on chosen platform
- [ ] Verified email (if required)

### For Render.com
- [ ] Logged into Render.com
- [ ] Clicked "New +" → "Blueprint"
- [ ] Connected GitHub account
- [ ] Selected your repository
- [ ] Reviewed `render.yaml` configuration
- [ ] Clicked "Apply"
- [ ] Waiting for deployment (10-15 minutes)

### For Railway.app
- [ ] Installed Railway CLI: `npm i -g @railway/cli`
- [ ] Ran `railway login`
- [ ] Ran `railway init`
- [ ] Added database: `railway add --database postgres`
- [ ] Deployed: `railway up`
- [ ] Opened dashboard: `railway open`

### For Fly.io
- [ ] Installed Fly CLI
- [ ] Ran `fly auth login`
- [ ] Created database: `fly postgres create --name wakfu-db`
- [ ] Deployed API: `cd api && fly launch && fly deploy`
- [ ] Deployed Frontend: `cd frontend && fly launch && fly deploy`
- [ ] Deployed Worker: `cd worker && fly launch && fly deploy`

---

## ⚙️ Configuration

### Database
- [ ] Database created successfully
- [ ] Database is running (check health status)
- [ ] Database URL copied
- [ ] Database URL set in API environment
- [ ] Database URL set in Worker environment

### API Service
- [ ] API service created
- [ ] Environment variables set:
  - [ ] `DATABASE_URL`
  - [ ] `CORS_ORIGINS` (with frontend URL)
  - [ ] `GAMEDATA_PATH=/wakfu_data/gamedata_1.90.1.43`
- [ ] Service is building
- [ ] Service deployed successfully
- [ ] API URL copied (e.g., https://wakfu-api.onrender.com)

### Frontend Service
- [ ] Frontend service created
- [ ] Environment variables set:
  - [ ] `VITE_API_URL` (with API URL)
- [ ] Service is building
- [ ] Service deployed successfully
- [ ] Frontend URL copied (e.g., https://wakfu-frontend.onrender.com)

### Worker Service
- [ ] Worker service created
- [ ] Environment variables set:
  - [ ] `DATABASE_URL`
  - [ ] `GAMEDATA_PATH=/wakfu_data/gamedata_1.90.1.43`
- [ ] Service is building
- [ ] Service deployed successfully
- [ ] Worker has run successfully

---

## 🧪 Testing & Verification

### API Testing
- [ ] Can access API URL in browser
- [ ] `/health` endpoint returns `{"status":"healthy"}`
- [ ] `/docs` shows FastAPI documentation
- [ ] Can see available endpoints
- [ ] No 500 errors in API logs

### Database Testing
- [ ] Worker logs show data loading completed
- [ ] Database has tables created
- [ ] Database has data (items, equipment, etc.)
- [ ] API can query database successfully

### Frontend Testing
- [ ] Frontend loads in browser
- [ ] No white screen of death
- [ ] No errors in browser console
- [ ] Can see the UI
- [ ] All assets load (images, CSS, fonts)

### Integration Testing
- [ ] Frontend can reach API
- [ ] No CORS errors in console
- [ ] Can select equipment slots
- [ ] Can set preferences
- [ ] Can generate builds
- [ ] Build results display correctly
- [ ] All features work as expected

---

## 🔧 Post-Deployment Setup

### Monitoring (Recommended)
- [ ] Set up UptimeRobot (for Render.com)
  - [ ] Created UptimeRobot account
  - [ ] Added API monitor (https://your-api.com/health)
  - [ ] Set interval to 5 minutes
  - [ ] Added Frontend monitor
- [ ] Set up error tracking (optional)
  - [ ] Sentry, LogRocket, or similar
- [ ] Set up analytics (optional)
  - [ ] Google Analytics, Plausible, etc.

### Custom Domain (Optional)
- [ ] Purchased domain (or using free subdomain)
- [ ] Added domain to platform
- [ ] Updated DNS records
- [ ] SSL certificate issued
- [ ] Domain works with HTTPS

### CORS & Security
- [ ] Updated `CORS_ORIGINS` with all frontend URLs
- [ ] Added custom domain to CORS (if applicable)
- [ ] Tested CORS from frontend
- [ ] Security headers configured (nginx.conf)

### Performance
- [ ] Tested cold start time (Render.com)
- [ ] Verified services wake up properly
- [ ] Tested API response times
- [ ] Tested frontend load time
- [ ] Optimized if needed

---

## 📊 Final Verification

### Services Status
- [ ] ✅ Database: Running
- [ ] ✅ API: Running & Healthy
- [ ] ✅ Frontend: Running & Accessible
- [ ] ✅ Worker: Completed Successfully

### URLs Saved
- [ ] Frontend URL: ___________________________
- [ ] API URL: ___________________________
- [ ] API Docs URL: ___________________________
- [ ] Database URL: ___________________________ (keep secret!)

### Functionality Check
- [ ] ✅ Home page loads
- [ ] ✅ Can navigate UI
- [ ] ✅ API responds
- [ ] ✅ Can generate builds
- [ ] ✅ Results display correctly
- [ ] ✅ No console errors
- [ ] ✅ Mobile responsive (check on phone)

---

## 🎉 Success Criteria

Your deployment is successful when:

✅ All services show "Running" or "Healthy" status
✅ Frontend loads without errors
✅ API docs accessible at `/docs`
✅ Can generate builds end-to-end
✅ No CORS errors
✅ Database populated with game data
✅ Services stay online (or wake up properly)

---

## 📝 Post-Launch Tasks

### Documentation
- [ ] Updated README with deployment URLs
- [ ] Documented environment variables
- [ ] Created troubleshooting guide (if needed)

### Sharing
- [ ] Shared with friends/testers
- [ ] Posted on Wakfu community forums
- [ ] Added to portfolio (if applicable)

### Maintenance
- [ ] Set calendar reminder to renew DB (Render, 90 days)
- [ ] Monitor usage/credits (Railway)
- [ ] Check logs weekly
- [ ] Plan for backups

---

## 🆘 If Something Goes Wrong

### Deployment Failed?
1. Check build logs for errors
2. Verify Dockerfile syntax
3. Ensure all dependencies listed
4. Check platform status page

### Services Won't Start?
1. Check environment variables are set correctly
2. Verify database is running
3. Check service logs for error messages
4. Ensure ports are correct

### Can't Access Services?
1. Wait 10-15 minutes (first deploy takes time)
2. Check service status (should be "Running")
3. Verify URL is correct
4. Try incognito/private browsing

### Database Issues?
1. Verify `DATABASE_URL` is set
2. Check database is created and running
3. Look at worker logs for errors
4. Try restarting worker service

### CORS Errors?
1. Add frontend URL to `CORS_ORIGINS`
2. Include `https://` protocol
3. Restart API service
4. Clear browser cache

---

## 💡 Pro Tips

- ✨ Deploy early, deploy often
- ✨ Test in production-like environment first
- ✨ Keep environment variables in a secure note
- ✨ Set up monitoring from day one
- ✨ Document everything you do
- ✨ Take screenshots of working setup
- ✨ Backup your database regularly
- ✨ Monitor your costs (even free tier)

---

## 🎯 Quick Reference

### Render.com URLs
- Dashboard: https://dashboard.render.com
- Docs: https://render.com/docs

### Railway URLs
- Dashboard: https://railway.app/dashboard
- Docs: https://docs.railway.app

### Fly.io URLs
- Dashboard: https://fly.io/dashboard
- Docs: https://fly.io/docs

### Monitoring
- UptimeRobot: https://uptimerobot.com
- Sentry: https://sentry.io

---

## ✅ Completion

When you can check ALL boxes above, your deployment is complete! 🎉

**Congratulations on deploying your Wakfu Builder!** 🚀

---

**Print this checklist and check off items as you go!**

📋 Total Items: 100+
⏱️ Estimated Time: 30-60 minutes (first time)
🎯 Success Rate: 95%+ (if you follow all steps)

**You got this!** 💪

