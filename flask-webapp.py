from flask_socketio import SocketIO, emit
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

... # Server functionality for receiving and storing data from elsewhere, not related to the websocket

# Handle the webapp connecting to the websocket
@socketio.on('connect')
def test_connect():
    print('someone connected to websocket')
    emit('responseMessage', {'data': 'Connected! ayy'})


# Handle the webapp connecting to the websocket, including namespace for testing
@socketio.on('connect', namespace='/devices')
def test_connect2():
    print('someone connected to websocket!')
    emit('responseMessage', {'data': 'Connected! ayy'})


# Handle the webapp sending a message to the websocket
@socketio.on('message')
def handle_message():
    print('someone sent to the websocket')


# Handle the webapp sending a message to the websocket, including namespace for testing
@socketio.on('message', namespace='/devices')
def handle_message2():
    print('someone sent to the websocket!')


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')