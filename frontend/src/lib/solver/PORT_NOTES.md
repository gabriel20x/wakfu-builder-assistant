# Solver Port Notes (Python/PuLP -> JavaScript/HiGHS)

Port of `api/app/services/solver.py` + `api/app/services/element_resolver.py`
+ the `/solve` contract of `api/app/routers/solver.py` to plain ES modules,
running fully client-side on HiGHS (WASM, npm package `highs` 1.15.x).

## Modules

- `elementResolver.js` — faithful port of `element_resolver.py`
  (`inferElementPreferencesFromWeights`, `resolveElementStats`, `resolveBuildStats`).
- `solverModel.js` — global eligibility filter (the old SQLAlchemy query),
  per-tier rarity filter, objective scoring, item power / alternatives, and the
  MILP model emitted as CPLEX LP format text. Constants copied from
  `api/app/core/config.py` (`SETTINGS`) and the normalization table from `solver.py`.
- `engine.js` — thin wrapper around the HiGHS WASM instance
  (`getHighs`, `solveLp`, `setHighsLoader` for browser injection).
- `solver.js` — public API: `async solveBuild(items, params) -> SolveResponse`.
  `items` is the array from `public/data/items.json`; `params` uses the exact
  snake_case request fields of the old POST `/solve`
  (`level_max, stat_weights, include_pet, include_accessory, only_droppable,
  damage_preferences, resistance_preferences, ignored_item_ids, monster_types`),
  with the same defaults. Response: `{easy, medium, hard_epic, hard_relic, full}`,
  each `{items, total_stats, total_difficulty, build_type}` with the same
  per-item serialization (incl. `metadata`, `drop_sources`, `alternatives`
  with `item_power` / `power_difference`).

## Fidelity verification

Beyond the unit/integration tests (`frontend/tests/solver.test.mjs`), the port
was cross-checked against the *real* `solver.py` executed with PuLP/CBC
(SQLAlchemy stubbed out, same eligible item pool from `items.json`,
level_max=230, realistic weights): **all five tiers selected the exact same
item sets, with identical objective values** (diff 0.0 on every tier).

## Data-source changes (no database)

- Items come from a static JSON array instead of `Item` rows.
- `item.metadata` is embedded per item (Python read `METADATA_PATH`
  / `item_metadata.json` at solve time; missing metadata serializes as `{}`
  in both versions).
- `item.drop_sources` is embedded (Python queried
  `MonsterDrop`/`Monster`/`MonsterFamily` at solve time). Consequently:
  - `only_droppable` = "has at least one entry in `drop_sources`" (equivalent to
    Python's "has at least one `MonsterDrop` row", since `drop_sources` was
    generated from that table).
  - `monster_types` filtering checks `drop_sources[].monster_type` (equivalent
    to the old `MonsterDrop JOIN Monster` query).

## Behavioral deviations (and why)

1. **Response keys**: `_solve_single_build` in Python also returned `status` and
   `num_items`, but FastAPI's `BuildResponse` model stripped them before they
   reached the frontend. The JS port returns exactly the four contract keys, so
   the browser-visible response is unchanged.
2. **Binary extraction threshold**: Python used `value(var) == 1`; the JS port
   uses `Primal > 0.5` because HiGHS can report values like `0.99999999` for
   binaries. Same semantics, more robust.
3. **Empty candidate pool**: PuLP happily "solves" a zero-variable problem as
   Optimal; the HiGHS LP-file parser needs at least one variable, so the port
   short-circuits to an empty build when the tier's item list is empty.
   Identical output (empty `items`, `{}` stats, 0 difficulty).
4. **Degenerate optima**: MILP solutions are not unique; CBC and HiGHS may
   break ties between equally-optimal builds differently. In the cross-check
   above they happened to coincide, but exact item identity is not guaranteed
   for every input — only objective-value equality is.
5. **Constraint names**: PuLP silently tolerated duplicate constraint names
   (e.g. `no_duplicate_ring_*` collisions); the LP text uses unique generated
   names. No semantic difference.
6. **Dead code preserved**: the rarity bonus block only triggers for
   `build_type == "hard"`, which never matches the current tier names
   (`hard_epic`/`hard_relic`/`full`) — it was dead code in Python and is
   intentionally kept dead here (do not "fix" without changing Python parity).
7. **Not ported** (backend-only concerns): build history persistence
   (`Build` table write in the router), `/history`, `/refresh-items`.

Everything else — filtering (level window `[level_max-10, level_max]`,
+10 for rarity 5/6/7, PET exemption, rarity-2 and "Recuerdo" exclusions),
adaptive tier rarity rules at level 80, ring duplicate/no-2H-with-off-hand
pair constraints, the `difficulty_max * 14` aggregate difficulty cap, scoring
(normalization factors, negative-stat penalties, missing AP/MP slot penalties
with compensation, 30%/10% bonuses, slot-fill bonus 5/2, lambda weights 2.0 /
0.5 / 0.0), alternatives (top 3 lower-power same-slot items over the same
tier-filtered pool) — is replicated 1:1.

## Performance (Node 22, Windows, level_max 230, 7920-item items.json)

- Eligible pool after global filter: ~712 items.
- HiGHS WASM instantiation (one-time): ~70-100 ms in Node.
- All five tiers solved (incl. model build, alternatives, serialization):
  **~200 ms total** (~40 ms/tier). Python/CBC took roughly 0.4 s per tier on
  the same pool.
- Full test suite (`node frontend/tests/solver.test.mjs`): ~0.5 s.

## Browser integration

- The `highs` package loads `highs.wasm` next to its JS glue. Bundlers (Vite)
  won't resolve that automatically; inject a loader before the first solve:

  ```js
  import highsLoader from 'highs';
  import highsWasmUrl from 'highs/build/highs.wasm?url';
  import { setHighsLoader } from '@/lib/solver/engine.js';

  setHighsLoader(() => highsLoader({
    locateFile: (file) => (file.endsWith('.wasm') ? highsWasmUrl : file),
  }));
  ```

  In Node (tests), no setup is needed — `engine.js` falls back to
  `import('highs')`.
- `highs.solve()` is synchronous and CPU-bound once the instance is ready;
  run `solveBuild` inside a Web Worker to keep the UI responsive, and load
  `items.json` (~9.8 MB) once, then reuse the array across solves.
- The HiGHS instance is created once and cached (`getHighs`); repeated solves
  are cheap.
