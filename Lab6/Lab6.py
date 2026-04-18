import asyncio
import random

class DataStream:
    
    def __init__(self, records = 1000000):
        self.records = records
        self.current = 0
        self.levels = ["INFO", "DEBUG", "ERROR", "WARNING"]
        
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.records:
            raise StopAsyncIteration
        
        if self.current % 1000 == 0:
            await asyncio.sleep(0.01)
            
        self.current += 1
        level = random.choice(self.levels)
        return {"id": self.current, "level": level}
    
async def process(data):
    errors = 0
    
    async for record in data:
        if record["level"] == "ERROR":
            errors += 1
            
            if errors % 10000 == 0:
                print(f"Found {errors} errors")
    return errors

async def main():
    data = DataStream(records=1000000)
    errors = await process(data)
    print(f"Total errors found: {errors}")
    
asyncio.run(main())