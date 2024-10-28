from pynput import mouse
import time


# Define inactivity timeout in seconds (e.g., 60 seconds = 1 minute)
INACTIVITY_TIMEOUT = 30

# Track the last time of mouse activity
last_activity_time = None

def on_move(callback):
    """Handles mouse movement events."""

    global last_activity_time
    current_time = time.time()

    if last_activity_time == None:
        callback(f"Mouse Move {current_time}")
        last_activity_time = current_time


    ellips_time = current_time - last_activity_time
    if ellips_time > INACTIVITY_TIMEOUT:
        callback(f"Mouse Move {current_time}")
    
    last_activity_time = current_time
    

def start_mouse_observer(callback):
    """Start listening for mouse events."""
    print("Mouse Activity Observer Started")

    def on_move_run(x,y):
        on_move(callback)
    
    def on_click_run(x, y, button, pressed):
        on_move(callback)

    with mouse.Listener(on_move=on_move_run, on_click=on_click_run) as listener:
        listener.join()  # Keep the listener running

def callback(message):
    print(message,"from callback")

if __name__ == "__main__":
    # Start the mouse event listener
    start_mouse_observer(callback)
