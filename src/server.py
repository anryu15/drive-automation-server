import asyncio
import websockets
import config

async def receiveImage(websocket, path):
    image = await websocket.recv()
    with open(config.IMAGE_PATH, "wb")  as f:
      f.write(image)
      print(config.IMAGE_PATH)

start_server = websockets.serve(receiveImage, config.HOST_IP_ADDR, config.HOST_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
