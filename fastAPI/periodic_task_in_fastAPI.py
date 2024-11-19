from fastapi import FastAPI
import asyncio

app = FastAPI()
x = [1]           # a global variable x

@app.get('/x')
def hello():
    return {'x':x}

async def periodic():
    while True:
        # code to run periodically starts here
        x[0] += 1
        print(f"x is now {x}")
        # code to run periodically ends here
        # sleep for 2seconds after running above code
        await asyncio.sleep(2)

@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(periodic())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)