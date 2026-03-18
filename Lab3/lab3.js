function memoize(fn, options = {}) {
  const { maxSize = Infinity, policy = "LRU", time = null } = options;

  const cache = new Map();
  function makeKey(args) {
    JSON.stringify(args);
  }

  function LRU() {
    const oldestKey = cache.keys().next().value;
    cache.delete(oldestKey);
  }

  function LFU() {
    const minFrequency = Infinity;
    const LFUKey = null;

    for (const [key, entry] of cache) {
      if (entry.freq < minFrequency) {
        minFrequency = entry.freq; // потім пропишу freq
        LFUKey = key;
      }
    }
    cache.delete(LFUKey);
  }

  function timeout() {
    for (const [key, entry] of cache) {
      if (Date.now() - entry.addedAt > time) {
        // потім напишу addedAt
        cache.delete(key);
      }
    }
  }
}
