from tornado_websockets.websocket import WebSocket

'''
    Test application for WebSocket tests.
'''


def get_ws():
    ws = WebSocket('/test')

    @ws.on
    def hello(socket, data):
        ws.emit('hello', {
            'message': 'Hello, I am %s.' % ws,
        })

    return ws
