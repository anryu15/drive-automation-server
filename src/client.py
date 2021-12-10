from websocketClient import WebsocketClient 
import config

ws_client = WebsocketClient(config.RASP_ADDR)
ws_client.run_forever()