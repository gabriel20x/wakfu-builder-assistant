/**
 * Web Worker that runs the MILP build solver off the main thread.
 * Loads the static item data once and solves requests sequentially.
 */
import highsLoader from 'highs'
// Direct file path: the highs package's exports map doesn't expose the wasm
import highsWasmUrl from '../../node_modules/highs/build/highs.wasm?url'
import { setHighsLoader } from '../lib/solver/engine.js'
import { solveBuild } from '../lib/solver/solver.js'

// Vite can't resolve the wasm next to the highs glue automatically —
// inject a loader that points at the bundled asset URL.
setHighsLoader(() =>
  highsLoader({
    locateFile: (file) => (file.endsWith('.wasm') ? highsWasmUrl : file),
  })
)

let itemsPromise = null

function loadItems() {
  if (!itemsPromise) {
    itemsPromise = fetch('/data/items.json').then((res) => {
      if (!res.ok) throw new Error(`Failed to load items.json: ${res.status}`)
      return res.json()
    })
  }
  return itemsPromise
}

self.onmessage = async (event) => {
  const { id, params } = event.data
  try {
    const items = await loadItems()
    const result = await solveBuild(items, params)
    self.postMessage({ id, result })
  } catch (err) {
    self.postMessage({ id, error: err?.message || String(err) })
  }
}
