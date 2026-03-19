function memoize(fn, options = {}) {
  const { maxSize = Infinity, policy = "LRU", time = null } = options;

  const cache = new Map();
  function makeKey(args) {
    return JSON.stringify(args);
  }

  function LRU() {
    const oldestKey = cache.keys().next().value;
    cache.delete(oldestKey);
  }

  function LFU() {
    let minFrequency = Infinity;
    let LFUKey = null;

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

// testing

function fib(n) {
  if (n <= 2) {
    return 1;
  }
  return fib(n - 2) + fib(n - 1);
}

const fibonacci1 = memoize(fib, { maxSize: 3, policy: "LRU" });

console.log(fibonacci1(40));
console.log(fibonacci1(41));
console.log(fibonacci1(42));
console.log(fibonacci1(42));
console.log(fibonacci1(43));
console.log(fibonacci1(40));

const fibonacci2 = memoize(fib, { maxSize: 3, policy: "LFU" });

console.log(fibonacci2(40));
console.log(fibonacci2(41));
console.log(fibonacci2(42));
console.log(fibonacci2(40));
console.log(fibonacci2(42));
console.log(fibonacci2(43));
console.log(fibonacci2(41));

const fibonacci3 = memoize(fib, { maxSize: 3, policy: "timeout", time: 5000 });

console.log(fibonacci3(40));
console.log(fibonacci3(41));
console.log(fibonacci3(42));
console.log(fibonacci3(42));
console.log(fibonacci3(43));
console.log(fibonacci3(44));
console.log(fibonacci3(41));
