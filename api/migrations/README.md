# Database Migrations

This directory contains SQL migration scripts for the Wakfu Builder Assistant database.

## Available Migrations

### add_blocks_second_weapon.sql
Adds the `blocks_second_weapon` column to track two-handed weapons.

### add_gfx_id.sql
Adds the `gfx_id` column to store the graphics ID for item images.

## How to Apply Migrations

### Option 1: Manual SQL Execution

Connect to your PostgreSQL database and run:

```bash
psql -U wakfu -d wakfu_builder -f add_gfx_id.sql
```

### Option 2: Using Docker

```bash
docker exec -i wakfu-builder-assistant-db-1 psql -U wakfu -d wakfu_builder < api/migrations/add_gfx_id.sql
```

### Option 3: Automatic (Recommended)

The worker will automatically create all columns when it runs. Simply set `FORCE_RELOAD=true` to reload all data:

```bash
docker-compose down
docker-compose up -d
# Wait for worker to complete
```

## Data Population

After adding the `gfx_id` column, you need to reload the data:

1. Set environment variable: `FORCE_RELOAD=true` in docker-compose.yml
2. Restart the worker container
3. The worker will extract `gfx_id` from `graphicParameters` in the item data

## Notes

- All migrations use `IF NOT EXISTS` clauses, so they're safe to run multiple times
- The worker creates tables and columns automatically using SQLAlchemy models
- Manual migrations are only needed if you want to update without reloading all data

