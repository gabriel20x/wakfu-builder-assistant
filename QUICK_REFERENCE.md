# Quick Reference Card

## 🚀 Essential Commands

### First Time Setup
```bash
# 1. Create environment file
cat > .env << 'EOF'
POSTGRES_USER=wakfu
POSTGRES_PASSWORD=wakfu123
POSTGRES_DB=wakfu_builder
GAMEDATA_VERSION=1.90.1.43
CORS_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

# 2. Build and start
make build
make up

# 3. Load data (wait 30s first!)
sleep 30
docker compose restart worker

# 4. Monitor loading
docker compose logs -f worker
# Press Ctrl+C when you see "✅ Game data loading complete!"

# 5. Open app
open http://localhost:3000
```

### Daily Use
```bash
make up     # Start
make logs   # View logs
make down   # Stop
```

## 📍 URLs

- 🎨 **Frontend**: http://localhost:3000
- 🔧 **API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- ❤️ **Health**: http://localhost:8000/health

## 🛠️ Makefile Commands

```bash
make build      # Build all Docker images
make up         # Start all services
make down       # Stop all services
make logs       # View all logs
make test       # Run tests
make clean      # Remove everything
make help       # Show all commands
```

## 🐳 Docker Commands

```bash
# Service management
docker compose ps                    # List services
docker compose restart api           # Restart API
docker compose logs -f frontend      # Follow frontend logs
docker compose exec api bash         # Shell into API

# Database
docker compose exec db psql -U wakfu -d wakfu_builder

# Clean restart
docker compose down -v
docker compose up -d
```

## 📊 Database Queries

```bash
# Connect to database
docker compose exec db psql -U wakfu -d wakfu_builder

# Useful queries
SELECT COUNT(*) FROM items;
SELECT COUNT(*) FROM items WHERE source_type = 'drop';
SELECT name, level, difficulty FROM items WHERE is_epic = true LIMIT 10;
SELECT * FROM items WHERE slot = 'HEAD' ORDER BY difficulty DESC LIMIT 5;
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test
docker compose exec api pytest tests/test_solver.py -v

# Run with coverage
docker compose exec api pytest --cov=app tests/
```

## 🔍 Debugging

### Check if services are running
```bash
docker compose ps
```

### Check API health
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### Check data loaded
```bash
curl http://localhost:8000/gamedata/status
# Expected: {"status":"completed","loaded_items":5000+}
```

### View recent logs
```bash
docker compose logs --tail=50 api
docker compose logs --tail=50 worker
docker compose logs --tail=50 frontend
```

### Test build generation
```bash
curl -X POST http://localhost:8000/build/solve \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 200,
    "stat_weights": {
      "HP": 1.0,
      "AP": 2.5,
      "MP": 2.0
    }
  }'
```

## 🐛 Common Issues

### Port already in use
```bash
# Find what's using port 3000
lsof -i :3000
# Kill it or change port in docker-compose.yml
```

### Database won't start
```bash
# Remove volume and restart
docker compose down -v
docker compose up -d
```

### Worker fails
```bash
# Check logs
docker compose logs worker

# Common fixes:
# 1. Wait longer for DB to be ready
sleep 60 && docker compose restart worker

# 2. Check game data path exists
ls -la wakfu_data/gamedata_1.90.1.43/
```

### Frontend won't connect to API
```bash
# Check CORS settings
docker compose exec api env | grep CORS

# Check API is responding
curl http://localhost:8000/health

# Check browser console for errors
```

### Empty builds
```bash
# Check items loaded
curl http://localhost:8000/items?limit=1

# Try higher level
curl -X POST http://localhost:8000/build/solve \
  -H "Content-Type: application/json" \
  -d '{"level_max": 230, "stat_weights": {"HP": 1.0}}'
```

## 📝 File Locations

### Configuration
- `.env` - Environment variables
- `api/app/core/config.py` - Solver settings
- `docker-compose.yml` - Service config

### Logs
```bash
docker compose logs api      # API logs
docker compose logs worker   # Worker logs
docker compose logs frontend # Frontend logs
docker compose logs db       # Database logs
```

### Data
- `wakfu_data/gamedata_1.90.1.43/` - Game data JSON files
- PostgreSQL data: Docker volume `pgdata`

## 🎮 Usage Examples

### Generate Tank Build
```json
{
  "level_max": 230,
  "stat_weights": {
    "HP": 5.0,
    "Resistance": 3.0,
    "Lock": 2.0
  }
}
```

### Generate DPS Build
```json
{
  "level_max": 230,
  "stat_weights": {
    "AP": 5.0,
    "Critical_Hit": 3.0,
    "Damage_Inflicted": 2.5,
    "Mastery": 2.0
  }
}
```

### Generate Support Build
```json
{
  "level_max": 230,
  "stat_weights": {
    "MP": 4.0,
    "Initiative": 2.0,
    "Wisdom": 2.0,
    "Prospecting": 1.0
  }
}
```

## 📋 Stat Names

Available stat weights:
- `HP` - Health Points
- `AP` - Action Points
- `MP` - Movement Points
- `Critical_Hit` - Critical Hit chance
- `Damage_Inflicted` - Damage bonus
- `Resistance` - Damage reduction
- `Mastery` - Element mastery
- `Lock` - Lock (positioning)
- `Dodge` - Dodge (positioning)
- `Initiative` - Turn order
- `Wisdom` - Experience/drops
- `Prospecting` - Item find

## 🔄 Update Workflow

### Update Game Data
1. Download new JSON files
2. Place in `wakfu_data/gamedata_X.XX.X.XX/`
3. Update `.env`:
   ```bash
   GAMEDATA_VERSION=X.XX.X.XX
   ```
4. Update `api/app/core/config.py`:
   ```python
   GAMEDATA_PATH = "/wakfu_data/gamedata_X.XX.X.XX"
   ```
5. Restart worker:
   ```bash
   docker compose restart worker
   ```

### Update Code
```bash
# 1. Make changes
# 2. Rebuild service
docker compose build api
docker compose restart api

# Or rebuild everything
make build
make up
```

## 📊 Monitoring

### Check resource usage
```bash
docker stats
```

### Check disk usage
```bash
docker system df
```

### Check database size
```bash
docker compose exec db psql -U wakfu -d wakfu_builder -c "\dt+"
```

## 🔐 Security Notes

**Current setup is for LOCAL USE only**

For production:
- [ ] Change default passwords
- [ ] Add authentication
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Restrict CORS
- [ ] Use secrets management

## 📚 Documentation

- `README.md` - Overview
- `QUICKSTART.md` - 5-minute setup
- `SETUP.md` - Detailed guide
- `ARCHITECTURE.md` - Technical docs
- `PROJECT_OVERVIEW.md` - Features
- `COMPLETION_SUMMARY.md` - What was built
- `QUICK_REFERENCE.md` - This file

## 🎯 Performance Tips

**Faster builds:**
- Lower `level_max` (e.g., 200)
- Fewer stat weights (2-3 main stats)
- Use Medium builds (balanced)

**Better results:**
- Update drop difficulties
- Higher weights (4-5) on key stats
- Include complementary stats

## ✅ Health Check Checklist

```bash
# 1. Services running
docker compose ps
# All should be "Up" or "Up (healthy)"

# 2. API responding
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# 3. Data loaded
curl http://localhost:8000/gamedata/status
# Should return: {"status":"completed","loaded_items":...}

# 4. Items accessible
curl http://localhost:8000/items?limit=1
# Should return: [{...}]

# 5. Frontend accessible
curl http://localhost:3000
# Should return: HTML

# 6. Database accessible
docker compose exec db psql -U wakfu -d wakfu_builder -c "SELECT COUNT(*) FROM items;"
# Should return: count > 0
```

---

**Keep this reference handy!** 📌

Save this file for quick access to common commands and troubleshooting steps.

