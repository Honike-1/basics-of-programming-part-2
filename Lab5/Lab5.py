import asyncio

def map1(arr, fn, callback):
    async def _run():
        result = []
        
        for item in arr:
            res = await fn(item)
            result.append(res)
        
        return result
    
    def _execute():
        try:
            loop = asyncio.get_running_loop()
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