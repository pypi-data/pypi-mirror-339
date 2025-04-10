import asyncio
import json
import socket
import websockets
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK
from rcom.rcom_registry import RcomRegistry

    
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


class RcomServer():
    def __init__(self, topic):
        pass

    def handle_command(self, method, args):
        pass
        

async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(message)
            response = try_handle_message(message)
            await websocket.send(json.dumps(response))
        except ConnectionClosedOK:
            break


def try_handle_message(message):
    method = None
    result = {}
    try:
        cmd = json.loads(message)
        if not 'method' in cmd:
            raise ValueError('Missing method')
        method = cmd['method']
        result = handle_command(method, cmd)
    except Exception as e:
        result = {'method': method, 'error': {'code': -1, 'message': repr(e)}}
    return result


def handle_command(method, args):
    return {'method': method}


async def main():
    my_ip = get_local_ip()
    my_port = 45678
    async with serve(handler, my_ip, my_port) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())


    
