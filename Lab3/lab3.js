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
        minFrequency = entry.freq;
        LFUKey = key;
      }
    }
    cache.delete(LFUKey);
  }

  function timeout() {
    for (const [key, entry] of cache) {
      if (Date.now() - entry.addedAt > time) {
        cache.delete(key);
      }
    }
  }

  function eviction() {
    if (cache.size <= maxSize) {
      return;
    }

    if (policy === "LRU") {
      LRU();
    } else if (policy === "LFU") {
      LFU();
    } else if (policy === "timeout") {
      timeout();
    }
  }

  return function (...args) {
    const key = makeKey(args);

    if (policy === "timeout" && cache.has(key)) {
      const entry = cache.get(key);
      if (Date.now() - entry.addedAt > time) {
        cache.delete(key);
      }
    }

    if (cache.has(key)) {
      const entry = cache.get(key);
      entry.freq = (entry.freq || 0) + 1;
      if (policy === "LRU") {
        cache.delete(key);
        cache.set(key, entry);
      }

      return entry.value;
    }

    const result = fn.apply(this, args);

    cache.set(key, {
      value: result,
      freq: 1,
      addedAt: Date.now(),
    });

    eviction();
    return result;
  };
}

export { memoize };
