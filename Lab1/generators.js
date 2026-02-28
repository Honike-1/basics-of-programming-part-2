function* numGenerator(max) {
    min = 1;
    while (true) {
        let randNum = Math.round(Math.random() * (max - min + 1)) + min;
        yield randNum;
    }
}

function smth(iterator, timeout) {
    const end = Date.now() + timeout;
    
    while (Date.now() < end) {
        const {value} = iterator.next();
        console.log(value);
    }
}

const numGen = numGenerator(100);
smth(numGen, 25);