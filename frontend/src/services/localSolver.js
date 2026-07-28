/**
 * Main-thread client for the solver Web Worker.
 * Falls back to running the solver inline if Workers are unavailable.
 */

let worker = null
let nextId = 1
const pending = new Map()

function getWorker() {
  if (!worker) {
    worker = new Worker(new URL('../workers/solver.worker.js', import.meta.url), {
      type: 'module',
    })
    worker.onmessage = (event) => {
      const { id, result, error } = event.data
      const entry = pending.get(id)
      if (!entry) return
      pending.delete(id)
      if (error) entry.reject(new Error(error))
      else entry.resolve(result)
    }
    worker.onerror = (err) => {
      for (const entry of pending.values()) {
        entry.reject(err)
      }
      pending.clear()
      worker.terminate()
      worker = null
    }
  }
  return worker
}

export function solveBuildInWorker(params) {
  if (typeof Worker === 'undefined') {
    // Environments without Worker support: run inline (blocks UI while solving)
    return Promise.all([
      import('../lib/solver/solver.js'),
      import('./dataStore.js').then((m) => m.loadItems()),
    ]).then(([solverModule, items]) => solverModule.solveBuild(items, params))
  }
  const id = nextId++
  // Vue refs hand out reactive Proxies, which structured clone (postMessage)
  // rejects with DataCloneError — deep-copy to plain data first.
  const plainParams = JSON.parse(JSON.stringify(params))
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject })
    getWorker().postMessage({ id, params: plainParams })
  })
}
