function iterator(max) {
  let min = 1;

  return {
    next() {
      let randNum = Math.round(Math.random() * (max - min + 1)) + min;
      return {
        value: randNum,
        done: false,
      };
    },
  };
}

function smth2(iterator, timeout) {
  const end = Date.now() + timeout;

  while (Date.now() < end) {
    const value = iterator.next();
    console.log(value);
  }
}

const numGen = iterator(100);
smth2(numGen, 25);
