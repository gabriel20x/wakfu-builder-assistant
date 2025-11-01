# 🚀 Quickstart Guide - Wakfu Builder Crafter

Get up and running in 5 minutes!

## Prerequisites

✅ Docker and Docker Compose installed  
✅ At least 4GB free RAM  
✅ Ports 3000, 8000, and 5432 available  

## Step-by-Step Setup

### 1️⃣ Copy Environment File (5 seconds)

```bash
cp .env.example .env
```

**Optional**: Edit `.env` if you want to change default passwords or ports.

### 2️⃣ Build Docker Images (2-3 minutes)

```bash
make build
```

Or without Make:
```bash
docker compose build
```

This builds:
- ✅ FastAPI backend
- ✅ Next.js frontend  
- ✅ Python worker

### 3️⃣ Start All Services (30 seconds)

```bash
make up
```

Or without Make:
```bash
docker compose up -d
```

**Services starting:**
- 🗄️ PostgreSQL database
- 🔧 FastAPI backend
- 🎨 Next.js frontend
- ⚙️ Data worker

### 4️⃣ Load Game Data (2-5 minutes)

Wait ~30 seconds for services to be ready, then:

```bash
docker compose restart worker
```

**Monitor progress:**
```bash
docker compose logs -f worker
```

You'll see:
```
worker  | Loading JSON files...
worker  | Loaded 50000+ items from JSON
worker  | Processing items...
worker  | Loaded 5000-10000 equipment items
worker  | Processing recipes...
worker  | Processing harvest resources...
worker  | ✅ Game data loading complete!
```

Press `Ctrl+C` to exit logs.

### 5️⃣ Open the Application 🎉

**Frontend**: http://localhost:3000  
**API Docs**: http://localhost:8000/docs  

## First Build

1. Go to http://localhost:3000
2. Adjust the "Maximum Level" slider (default: 230)
3. Set stat priorities (AP and MP for offensive builds)
4. Click **"Generate Builds"**
5. Wait 2-10 seconds
6. See three builds: 🌱 Easy, ⚡ Medium, 🔥 Hard

## Verify Everything Works

### Check API Health
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy"}`

### Check Data Status
```bash
curl http://localhost:8000/gamedata/status
```

Expected: `{"status":"completed","loaded_items":...}`

### Check Items Loaded
```bash
curl http://localhost:8000/items?limit=5
```

Expected: JSON array of 5 items

## Common Issues

### ❌ Port already in use

**Error**: "Bind for 0.0.0.0:3000 failed: port is already allocated"

**Solution**:
```bash
# Stop services using the ports
docker compose down

# Or change ports in docker-compose.yml
```

### ❌ Worker fails immediately

**Error**: "Database connection failed"

**Solution**: Wait longer for PostgreSQL to initialize (30-60 seconds), then:
```bash
docker compose restart worker
```

### ❌ Frontend shows "Failed to generate builds"

**Causes**:
1. Data not loaded yet → Check `docker compose logs worker`
2. API not responding → Check `curl http://localhost:8000/health`
3. No items match criteria → Lower max level or adjust stat weights

**Solution**:
```bash
# Check all services are running
docker compose ps

# View all logs
make logs
```

### ❌ Empty builds returned

**Solution**: Increase level max to 230 and make sure data loaded successfully:
```bash
curl http://localhost:8000/gamedata/status
```

## Useful Commands

```bash
# View all logs
make logs

# View specific service
docker compose logs -f api
docker compose logs -f frontend
docker compose logs -f worker

# Restart a service
docker compose restart api

# Stop all services
make down

# Clean everything (including database)
make clean

# Run tests
make test
```

## What to Try

### 1. Generate Different Builds
- **Tank build**: High HP, Resistance weights
- **DPS build**: High AP, Critical Hit, Damage Inflicted
- **Support build**: High MP, Initiative, Wisdom

### 2. Edit Drop Difficulties
1. Click "Drop Difficulty Editor" tab
2. Search for an item (e.g., "ring")
3. Click "Edit"
4. Enter difficulty (0-100)
5. Click "Save"
6. Generate new builds to see the effect

### 3. Explore the API
Visit http://localhost:8000/docs for interactive API documentation.

Try these endpoints:
- `GET /items` - Browse all items
- `GET /items/{id}` - Get specific item
- `POST /build/solve` - Generate builds
- `GET /build/history` - View past builds

## Next Steps

📖 Read **SETUP.md** for detailed configuration options  
🏗️ Read **ARCHITECTURE.md** to understand how it works  
📋 Read **PROJECT_OVERVIEW.md** for the complete feature list  

## Performance Tips

**Faster builds:**
- Lower the max level (e.g., 200 instead of 230)
- Reduce stat variety (focus on 2-3 main stats)

**Better results:**
- Update drop difficulties for items you know
- Higher weights (3-5) on your most important stats
- Use Medium build as a good balance

## Stopping the Application

```bash
# Stop services (keeps data)
make down

# Stop and remove everything (clean slate)
make clean
```

## Support

Having issues? Check:
1. ✅ All services running: `docker compose ps`
2. ✅ Logs for errors: `make logs`
3. ✅ Database has data: `curl http://localhost:8000/gamedata/status`
4. ✅ API responding: `curl http://localhost:8000/health`

---

**Ready to build?** 🎮

```bash
make build && make up
# Wait 30 seconds
docker compose restart worker
# Wait 2-5 minutes
# Open http://localhost:3000
```

Enjoy! ✨

