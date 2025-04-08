import socketio

# Create client
sio = socketio.Client(ssl_verify=False)
sio_server = 'https://django:9500'

def emit_socket_event(event, data):
    if sio.connected is False:
        sio.connect(sio_server)

    sio.emit(event, data)

def send_socket_response(event, data):
    emit_socket_event(event, data)