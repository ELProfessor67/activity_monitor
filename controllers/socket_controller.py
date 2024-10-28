from dotenv import load_dotenv
import socketio
import os
from utils.generate_key import check_or_create_key

load_dotenv()
messenger_url = os.getenv('MESSENGER_URL')

sio = socketio.Client()
room_id = check_or_create_key()

@sio.event
def connect():
    global room_id
    print('Connection established')
    sio.emit('join', {"room_id":room_id})

@sio.event
def disconnect():
    print('Disconnected from server')


@sio.on("on_order")
def on_order(data):
    print("order",data)


sio.connect(messenger_url)


def send_message(event):
    global room_id
    sio.emit('on_event', {"room_id":room_id,"event": event})