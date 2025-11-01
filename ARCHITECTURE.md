# Architecture Documentation

## System Overview

Wakfu Builder Crafter is a full-stack application for generating optimal equipment builds in the MMORPG Wakfu. It uses linear programming to find equipment combinations that maximize desired stats while considering item acquisition difficulty.

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│                     (Next.js Frontend)                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Routers    │  │   Services   │  │   Database   │      │
│  │  (Endpoints) │─▶│   (Logic)    │─▶│   (Models)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                       │
│        Items | Recipes | Harvests | Builds                   │
└────────────────────────┬────────────────────────────────────┘
                         ▲
                         │ SQL
┌────────────────────────┴────────────────────────────────────┐
│                      Worker Service                          │
│         (Data Extraction & Normalization)                    │
└────────────────────────┬────────────────────────────────────┘
                         │ File I/O
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Game Data JSON Files                       │
│  items.json | recipes.json | harvestLoots.json | ...        │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Next.js 14)

**Technology Stack:**
- Next.js 14 with App Router
- React 18 (functional components only)
- TypeScript
- Tailwind CSS
- Axios for API calls

**Key Components:**

1. **FormStats** (`src/components/FormStats.tsx`)
   - Collects user input for build generation
   - Level slider (1-230)
   - Stat weight sliders (0-5) for 12 different stats
   - Validates inputs before submission

2. **BuildResult** (`src/components/BuildResult.tsx`)
   - Displays generated builds
   - Shows total stats aggregation
   - Lists all equipped items with details
   - Color-coded by difficulty (easy/medium/hard)

3. **ManualDropEditor** (`src/components/ManualDropEditor.tsx`)
   - Lists all drop-type items
   - Allows manual difficulty assignment
   - Real-time search/filter
   - Persists changes to database

**State Management:**
- React hooks (useState, useEffect)
- No external state management library needed
- Local state for forms, global state via API

### Backend (FastAPI)

**Technology Stack:**
- FastAPI (Python 3.11)
- SQLAlchemy 2.0 (ORM)
- Pydantic v2 (validation)
- PuLP (linear programming solver)
- PostgreSQL (via psycopg2)

**Architecture Pattern:**
- **Router → Service → Database** (3-tier)
- Dependency injection for database sessions
- Async-ready (though currently sync)

**Key Modules:**

1. **Routers** (`app/routers/`)
   - `solver.py`: Build generation endpoints
   - `items.py`: Item CRUD operations
   - `gamedata.py`: Data management endpoints

2. **Services** (`app/services/`)
   - `solver.py`: Linear programming optimization
   - `difficulty.py`: Difficulty calculation algorithms
   - `normalizer.py`: JSON parsing and data loading

3. **Database Models** (`app/db/models.py`)
   - `Item`: Equipment items
   - `Recipe`: Crafting recipes
   - `HarvestResource`: Collection resources
   - `Build`: Saved builds history
   - `GameDataVersion`: Data versioning

### Difficulty Calculation System

The difficulty score (0-100) is calculated using a weighted formula:

```
difficulty = 0.3 × harvest_cost +
             0.3 × recipe_cost +
             0.2 × drop_cost +
             0.1 × flag_score +
             0.1 × rarity_score +
             0.1 × level_score
```

**Component Calculations:**

1. **Harvest Cost** (for collectible items):
   ```
   harvest_cost = (collection_time × visibility + consumption) / (drop_rate × quantity)
   Normalized to 0-100 using 95th percentile
   ```

2. **Recipe Cost** (for craftable items):
   ```
   recipe_cost = Σ(difficulty(ingredient) × quantity) + craft_cost
   Recursive calculation through ingredient tree
   ```

3. **Drop Cost** (for mob drops):
   ```
   drop_cost = manual_drop_difficulty (default: 70.0)
   User-assigned via frontend
   ```

4. **Flag Score**:
   - Epic: +20
   - Relic: +30
   - Gem slot: +10

5. **Rarity Score**:
   - Common: 10
   - Unusual: 15
   - Rare: 20
   - Mythical: 30
   - Legendary: 40
   - Relic: 35
   - Epic: 35

6. **Level Score**:
   ```
   level_score = (item_level / 230) × 100
   ```

### Solver System (Linear Programming)

**Problem Formulation:**

**Variables:**
- Binary variable `x_i` for each item (selected = 1, not selected = 0)

**Objective Function:**
```
maximize: Σ(stat_score_i - λ × difficulty_i) × x_i

where:
  stat_score_i = Σ(stat_value × stat_weight)
  λ = difficulty penalty (varies by build type)
```

**Constraints:**
1. **Slot constraint**: `Σ(x_i for i in slot) ≤ 1` for each equipment slot
2. **Epic constraint**: `Σ(x_i for i in epics) ≤ 1`
3. **Relic constraint**: `Σ(x_i for i in relics) ≤ 1`
4. **Level constraint**: `level_i ≤ level_max` for all selected items
5. **Difficulty constraint** (easy/medium only): `Σ(difficulty_i × x_i) ≤ threshold × num_slots`

**Lambda Values:**
- Easy: λ = 2.0 (high difficulty penalty)
- Medium: λ = 1.0 (balanced)
- Hard: λ = 0.1 (low difficulty penalty)

**Solver:**
- PuLP library (wrapper for COIN-OR CBC)
- Mixed Integer Linear Programming (MILP)
- Optimal solution guaranteed

### Worker Service

**Purpose:**
- One-time data loading on startup
- Parses JSON files from game data
- Normalizes into database schema
- Can be triggered via API for updates

**Processing Pipeline:**
1. Load all JSON files (~50MB total)
2. Build lookup maps for cross-references
3. Extract equipment items (filter non-equipment)
4. Determine source type (harvest/recipe/drop/special)
5. Extract stats from equipment effects
6. Process recipes and ingredients
7. Process harvest resources
8. Calculate initial difficulties
9. Insert into database with transactions

**Action ID Mapping:**
Converts Wakfu's internal effect IDs to stat names:
```python
{
    20: "HP",
    31: "AP",
    41: "MP",
    80: "Critical_Hit",
    120: "Damage_Inflicted",
    # ... 20+ mappings
}
```

### Database Schema

**Items Table:**
```sql
CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    level INTEGER NOT NULL,
    rarity INTEGER,
    slot VARCHAR,
    is_epic BOOLEAN,
    is_relic BOOLEAN,
    has_gem_slot BOOLEAN,
    source_type VARCHAR,
    difficulty FLOAT,
    manual_drop_difficulty FLOAT,
    stats JSONB,
    raw_data JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
-- Indexes on: level, slot, is_epic, is_relic, source_type, difficulty
```

**Recipes Table:**
```sql
CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY,
    result_item_id INTEGER,
    ingredients JSONB,  -- [{"item_id": 123, "quantity": 5}, ...]
    craft_cost FLOAT,
    created_at TIMESTAMP
);
```

**Harvest Resources Table:**
```sql
CREATE TABLE harvest_resources (
    resource_id INTEGER PRIMARY KEY,
    item_id INTEGER,
    collection_time FLOAT,
    visibility FLOAT,
    drop_rate FLOAT,
    quantity INTEGER,
    created_at TIMESTAMP
);
```

**Builds Table:**
```sql
CREATE TABLE builds (
    id SERIAL PRIMARY KEY,
    params JSONB,  -- Input parameters
    result JSONB,  -- Generated builds
    created_at TIMESTAMP
);
```

### API Endpoints

**Build Generation:**
- `POST /build/solve` - Generate three builds
- `GET /build/history` - View recent builds

**Item Management:**
- `GET /items` - List items (with filters)
- `GET /items/{id}` - Get item details
- `POST /items/{id}/difficulty` - Update drop difficulty

**Data Management:**
- `POST /gamedata/update` - Reload game data
- `GET /gamedata/status` - Check data status

**Health:**
- `GET /` - API info
- `GET /health` - Health check

### Security Considerations

**Current Implementation:**
- No authentication (single-user application)
- CORS enabled for localhost:3000
- SQL injection prevented by SQLAlchemy ORM
- Input validation via Pydantic

**Production Recommendations:**
- Add JWT authentication
- Rate limiting
- HTTPS only
- Environment-based CORS
- Database connection pooling
- API key for sensitive operations

### Performance Characteristics

**Solver Performance:**
- ~1000 items: <1 second
- ~5000 items: 1-3 seconds
- ~10000 items: 3-10 seconds
- Scales linearly with item count

**Database Performance:**
- Indexed queries: <10ms
- Full item scan: <100ms
- Build generation: 100ms - 5s (solver-dependent)

**Memory Usage:**
- Frontend: ~50MB
- API: ~200MB
- Worker: ~300MB (during loading)
- PostgreSQL: ~100MB + data size

**Storage:**
- JSON files: ~50MB
- PostgreSQL data: ~100-200MB
- Docker images: ~2GB total

### Scaling Considerations

**Horizontal Scaling:**
- Frontend: Stateless, easy to replicate
- API: Stateless, can run multiple instances
- Database: Use read replicas for queries
- Worker: Run on-demand, not persistent

**Vertical Scaling:**
- Solver benefits from more CPU cores
- Database benefits from more RAM
- JSON parsing benefits from faster I/O

**Optimization Opportunities:**
1. Cache solver results (same params = same builds)
2. Pre-calculate common builds
3. Use Redis for session storage
4. Implement GraphQL for flexible queries
5. Add WebSocket for real-time updates

## Technology Choices

**Why Next.js 14?**
- Modern React framework
- App Router for better SEO
- Server-side rendering capable
- Great developer experience

**Why FastAPI?**
- Fast and modern Python framework
- Automatic API documentation (OpenAPI)
- Native async support
- Excellent type checking with Pydantic

**Why PuLP?**
- Pure Python, easy to integrate
- Open-source (COIN-OR CBC solver)
- Handles complex constraints
- Optimal solutions guaranteed

**Why PostgreSQL?**
- Robust and reliable
- Excellent JSON support (JSONB)
- Great indexing capabilities
- Free and open-source

**Why Docker?**
- Consistent environments
- Easy deployment
- Service isolation
- Simple orchestration with compose

## Future Enhancements

1. **Multi-build comparison** - Compare different stat priorities side-by-side
2. **Build sharing** - Generate shareable URLs for builds
3. **Advanced filters** - Filter items by source, element, set bonuses
4. **Set bonus support** - Consider set bonuses in solver
5. **Export builds** - Export to CSV, JSON, or game-compatible format
6. **Historical tracking** - Track meta shifts over time
7. **Community difficulty** - Crowdsource difficulty ratings
8. **Mobile app** - Native mobile experience
9. **Real-time updates** - WebSocket for live data updates
10. **Machine learning** - Predict item difficulty based on similar items

