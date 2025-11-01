# Wakfu Builder Crafter

A dockerized SPA for generating Wakfu equipment builds based on statistics and item acquisition difficulty.

## Features

- **Automatic Build Generation**: Creates three builds (Easy, Medium, Hard) based on stat priorities
- **Difficulty Calculation**: Automatically calculates item difficulty from:
  - Harvest items: Using collection time and drop rates
  - Recipe items: Recursive ingredient difficulty calculation
  - Drop items: Manual input from frontend
- **Smart Solver**: Uses linear programming (PuLP) to maximize stats while respecting constraints
- **Full Stack**: Next.js frontend + FastAPI backend + PostgreSQL database

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Frontend   │────▶│     API     │────▶│ PostgreSQL  │
│  (Next.js)  │     │  (FastAPI)  │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           │
                    ┌──────▼──────┐
                    │   Worker    │
                    │  (Python)   │
                    └─────────────┘
```

## Quick Start

1. **Create environment file**:

Create a `.env` file in the root directory:
```bash
POSTGRES_USER=wakfu
POSTGRES_PASSWORD=wakfu123
POSTGRES_DB=wakfu_builder
GAMEDATA_VERSION=1.90.1.43
CORS_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

2. **Build and start services**:
```bash
make build
make up
```

3. **Load game data**:
```bash
docker compose restart worker
```

4. **Access the application**:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Services

- **db**: PostgreSQL 16 database
- **api**: FastAPI backend with solver logic
- **worker**: Python service for data extraction and normalization
- **frontend**: Next.js 14 frontend with App Router

## API Endpoints

### Build Generation
- `POST /build/solve` - Generate three builds (easy, medium, hard)
  ```json
  {
    "level_max": 230,
    "stat_weights": {
      "HP": 1.0,
      "AP": 2.5,
      "MP": 2.0,
      "Critical_Hit": 1.5
    }
  }
  ```

### Item Management
- `GET /items/{id}` - Get item details with calculated difficulty
- `POST /items/{id}/difficulty` - Update manual drop difficulty
- `GET /items` - List all items with filters

### Data Management
- `POST /gamedata/update` - Reload game data from JSON files

## Difficulty Calculation

The system calculates difficulty using multiple factors:

1. **Harvest Items** (30%):
   - Collection time × value
   - Drop rate
   - Quantity per harvest

2. **Recipe Items** (30%):
   - Recursive ingredient difficulty
   - Crafting cost

3. **Flags** (20%):
   - Epic: +20 points
   - Relic: +30 points
   - Gem slots: +10 points

4. **Rarity** (10%): 10-40 points (Common to Legendary)

5. **Level** (10%): Scaled from item level

## Development

### Run tests:
```bash
make test
```

### View logs:
```bash
make logs
```

### Clean everything:
```bash
make clean
```

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11, PuLP (solver)
- **Database**: PostgreSQL 16
- **DevOps**: Docker, Docker Compose

## License

MIT

