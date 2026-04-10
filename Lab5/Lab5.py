import asyncio
import re

def map1(arr, fn, callback):
    async def _run():
        result = []
        
        for item in arr:
            res = await fn(item)
            result.append(res)
        
        return result
    
    def _execute():
        try:
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(_run())
            callback(None, result)
        except Exception as error:
            callback(error, None)
            
    _execute()

async def map2(arr, fn, stop_event=None):
    result = []
    
    for item in arr:
        if stop_event is not None and stop_event.is_set():
            raise asyncio.CancelledError("Canceled")
        res = await fn(item)
        result.append(res)
    
    return result


# demo 1

arr1 = ["idk", "words", "something", "brainrot"]
async def fn1(item):
    await asyncio.sleep(1)
    return len(item)

def callback(error, result):
    if error:
        print("Error:", error)
    else:
        print("Words length:", result)
        
map1(arr1, fn1, callback)

# demo 2

arr2 = ["email@gmail.com", "smth", "another_email@ukr.net", "smth2"]
async def fn2(item):
    await asyncio.sleep(1)
    is_valid = bool(re.match(r"[^@]+@[^@]+\.[^@]+", item))
    return {"email": item, "valid": is_valid}

async def demo2():
    
    res = await map2(arr2, fn2)

    for item in res:
        if item["valid"] == True:
            print(f"{item["email"]}: is valid")
        else:
            print(f"{item["email"]}: is not valid")
            
asyncio.run(demo2())