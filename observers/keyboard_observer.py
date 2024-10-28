from pynput import keyboard
import threading
import time

# Define inactivity timeout in seconds (e.g., 60 seconds = 1 minute)
INACTIVITY_TIMEOUT = 2

# Track the last time of keyboard activity
last_activity_time = None


def on_key_press(callback,key):
    """Handles key press events."""
    global last_activity_time
    current_time = time.time()

    if last_activity_time == None:
        callback(f"Key Press {key}")
        last_activity_time = current_time


    ellips_time = current_time - last_activity_time
    if ellips_time > INACTIVITY_TIMEOUT:
        callback(f"Key Press {key}")
    
    last_activity_time = current_time


def start_keyboard_observer(callback):
    """Start listening for keyboard events."""
    print("Keyboard Activity Observer Started")

    def run_on_key_press(key):
        on_key_press(callback,key)
    

    with keyboard.Listener(on_press=run_on_key_press) as listener:
        listener.join()  # Keep the listener running


def callback(message):
    print(message)

if __name__ == "__main__":

    start_keyboard_observer(callback)
