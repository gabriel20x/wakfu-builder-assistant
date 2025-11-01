# Setup Guide - Wakfu Builder Crafter

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of available RAM
- Game data files in `wakfu_data/gamedata_1.90.1.43/`

## Quick Start

### 1. Initial Setup

```bash
# Copy environment variables
cp .env.example .env

# Build all Docker images
make build
```

### 2. Start Services

```bash
# Start all services in the background
make up

# View logs
make logs
```

### 3. Load Game Data

Wait for all services to be healthy (about 30 seconds), then:

```bash
# Restart the worker to trigger data loading
docker compose restart worker

# Monitor the loading progress
docker compose logs -f worker
```

This process will:
- Parse ~10,000+ items from JSON files
- Extract equipment stats and metadata
- Calculate difficulty scores
- Insert everything into PostgreSQL

Expected time: 2-5 minutes depending on your system.

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Using the Application

### Generate Builds

1. Open http://localhost:3000
2. Adjust the "Maximum Level" slider (default: 230)
3. Set stat priorities using the sliders:
   - **AP/MP**: High priority for offensive builds
   - **HP/Resistance**: High priority for defensive builds
   - **Critical Hit/Mastery**: Damage dealers
   - **Lock/Dodge**: Positioning control
4. Click "Generate Builds"
5. Review three builds:
   - **🌱 Easy**: Low difficulty items, easier to obtain
   - **⚡ Medium**: Balanced stats and difficulty
   - **🔥 Hard**: Maximum stats, ignoring difficulty

### Edit Drop Difficulties

1. Switch to the "Drop Difficulty Editor" tab
2. Search for items by name
3. Click "Edit" next to any drop item
4. Enter a difficulty value (0-100)
5. Click "Save"

The updated difficulty will be used in future build calculations.

## API Usage

### Generate Builds

```bash
curl -X POST http://localhost:8000/build/solve \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 200,
    "stat_weights": {
      "HP": 1.0,
      "AP": 2.5,
      "MP": 2.0,
      "Critical_Hit": 1.5
    }
  }'
```

### Get Item Details

```bash
curl http://localhost:8000/items/12345
```

### Update Drop Difficulty

```bash
curl -X POST http://localhost:8000/items/12345/difficulty \
  -H "Content-Type: application/json" \
  -d '{"difficulty": 75.0}'
```

### Check Data Status

```bash
curl http://localhost:8000/gamedata/status
```

## Development

### Run Tests

```bash
# Run API tests
make test

# Or manually
docker compose exec api pytest tests/ -v
```

### View Database

```bash
# Connect to PostgreSQL
docker compose exec db psql -U wakfu -d wakfu_builder

# Example queries
SELECT COUNT(*) FROM items;
SELECT name, level, difficulty FROM items WHERE is_epic = true;
```

### Rebuild After Code Changes

```bash
# Rebuild specific service
docker compose build api

# Restart service
docker compose restart api
```

## Troubleshooting

### Worker Fails to Load Data

Check logs:
```bash
docker compose logs worker
```

Common issues:
- Game data files not found → Check `wakfu_data/` path
- Database connection failed → Wait for PostgreSQL to be ready
- JSON parsing errors → Verify JSON file integrity

### API Returns Empty Builds

Possible causes:
1. Data not loaded yet → Restart worker
2. Level too low → Increase `level_max`
3. Stat weights too restrictive → Adjust weights

Check item count:
```bash
curl http://localhost:8000/items?limit=10
```

### Frontend Can't Connect to API

1. Check API is running: `curl http://localhost:8000/health`
2. Verify CORS settings in `.env`
3. Check browser console for errors

### Database Issues

Reset database:
```bash
# Stop services
docker compose down

# Remove database volume
docker volume rm wakfu-builder-assistant_pgdata

# Start fresh
docker compose up -d
```

## Configuration

### Environment Variables

Edit `.env` to customize:

```bash
# Database
POSTGRES_USER=wakfu
POSTGRES_PASSWORD=wakfu123
POSTGRES_DB=wakfu_builder

# API
CORS_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Game Data
GAMEDATA_VERSION=1.90.1.43
```

### Solver Parameters

Edit `api/app/core/config.py`:

```python
# Max items per type
MAX_EPIC_ITEMS = 1
MAX_RELIC_ITEMS = 1

# Difficulty thresholds
EASY_DIFFICULTY_MAX = 40.0
MEDIUM_DIFFICULTY_MAX = 70.0
HARD_DIFFICULTY_MAX = 100.0

# Lambda weights (higher = more penalty for difficulty)
EASY_LAMBDA = 2.0
MEDIUM_LAMBDA = 1.0
HARD_LAMBDA = 0.1
```

## Project Structure

```
wakfu-builder-crafter/
├── api/                 # FastAPI backend
│   ├── app/
│   │   ├── core/       # Configuration
│   │   ├── db/         # Database models
│   │   ├── routers/    # API endpoints
│   │   └── services/   # Business logic
│   └── tests/          # Unit tests
├── frontend/           # Next.js frontend
│   └── src/
│       ├── app/        # Pages
│       └── components/ # React components
├── worker/             # Data loading service
├── wakfu_data/         # Game data JSON files
└── docker-compose.yml  # Docker orchestration
```

## Performance Tips

1. **Database Indexing**: Already optimized for common queries
2. **Solver Speed**: Reduce `level_max` for faster results
3. **Frontend Caching**: Results are cached in component state
4. **API Rate Limiting**: None implemented, suitable for single-user

## Updating Game Data

When new game data is released:

1. Download new JSON files
2. Place in `wakfu_data/gamedata_X.XX.X.XX/`
3. Update `GAMEDATA_VERSION` in `.env`
4. Update `GAMEDATA_PATH` in `api/app/core/config.py`
5. Restart worker: `docker compose restart worker`

## License

MIT License - Free to use and modify

