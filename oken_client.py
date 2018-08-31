import websockets
import asyncio


async def hello():
    #35.236.186.12
    async with websockets.connect('ws://35.236.186.12:8765') as websocket:
        name = input("what's your name?")
        await websocket.send(name)
        print(f"send server:{name}")
        greeting = await websocket.recv()
        print(f"receive from server:{greeting}")


asyncio.get_event_loop().run_until_complete(hello())