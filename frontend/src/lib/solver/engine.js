/**
 * HiGHS engine wrapper.
 *
 * Keeps the highs-js (HiGHS compiled to WASM) instance creation behind a small
 * indirection so the browser / web worker integration can inject its own
 * loader (e.g. with a custom `locateFile` for the .wasm asset), while in Node
 * a plain dynamic import of the 'highs' package just works.
 */

let customLoader = null;
let instancePromise = null;

/**
 * Inject a custom loader that returns (a promise of) a ready HiGHS instance.
 * Must be called before the first solve. Typical browser usage:
 *
 *   import highsLoader from 'highs';
 *   import highsWasmUrl from 'highs/build/highs.wasm?url';
 *   setHighsLoader(() => highsLoader({
 *     locateFile: (file) => (file.endsWith('.wasm') ? highsWasmUrl : file),
 *   }));
 *
 * @param {() => Promise<object>|object} loader
 */
export function setHighsLoader(loader) {
  customLoader = loader;
  instancePromise = null;
}

/**
 * Get (and cache) the HiGHS instance.
 * @returns {Promise<object>} HiGHS instance with a `solve(lpText)` method.
 */
export async function getHighs() {
  if (!instancePromise) {
    instancePromise = (async () => {
      if (customLoader) {
        return customLoader();
      }
      // Default: Node / bundler resolution of the 'highs' package.
      const mod = await import('highs');
      const factory = mod.default || mod;
      return factory();
    })();
  }
  return instancePromise;
}

/**
 * Solve a model given in CPLEX LP format text.
 * @param {string} lpText
 * @returns {Promise<{Status: string, Columns: object, ObjectiveValue: number}>}
 */
export async function solveLp(lpText) {
  const highs = await getHighs();
  return highs.solve(lpText);
}
