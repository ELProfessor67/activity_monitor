import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileOpenedEvent, FileSystemEventHandler
import socket
import psutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from plyer import notification

# Path to the root directory to monitor (use "/" for Linux and "C:\\" for Windows)
WATCH_DIRECTORY = "/"
# Path to the log file
LOG_FILE = "activity_log.txt"

# Keep track of the logged changes
logged_changes = set()

class ChangeHandler(FileSystemEventHandler):
    def __init__(self,callback) -> None:
        self.callback = callback

    def on_opened(self, event) -> None:
        if not event.is_directory:
            if LOG_FILE in event.src_path:
                return
            ip, user = self.get_current_ip_and_user()
            self.log_event(f"File Opened: {event.src_path}", event.src_path, ip, "Opened", user)

    def on_created(self, event):
        if not event.is_directory:
            if LOG_FILE in event.src_path:
                return
            ip, user = self.get_current_ip_and_user()
            self.log_event(f"File created: {event.src_path}", event.src_path, ip, "Created", user)

    def on_modified(self, event):
        if not event.is_directory:
            if LOG_FILE in event.src_path:
                return
            ip, user = self.get_current_ip_and_user()
            self.log_event(f"File modified: {event.src_path}", event.src_path, ip, "Modified", user)

    def log_event(self, message, file_path, ip, event_type, user):
        if LOG_FILE in message:
            return
        if message not in logged_changes:
            # Add to logged changes to prevent duplicate entries
            logged_changes.add(message)
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"{time.ctime()} | {event_type} | {message} | IP: {ip} | User: {user}\n")
                # log_file.write(f"{time.ctime()}: {message} | IP: {ip} | User: {user}\n")
            # print(message, f" | IP: {ip} | User: {user}")
            self.callback(f"{time.ctime()} | {event_type} | {message} | IP: {ip} | User: {user}\n")
            

            # Show pop-up for file creation events
            self.show_notification(message,file_path);

    def get_current_ip_and_user(self):
        """Retrieve the current IP address and determine if the user is local or remote."""
        try:
            # Check active network connections to identify remote users
            active_connections = self.get_active_connections()
            if active_connections:
                # If remote connections are detected, treat it as a remote user (attacker)
                remote_ip = active_connections[0]['remote_ip']
                connection_type = self.check_connection_ip(remote_ip)
                if connection_type == "Remote":
                    return remote_ip, "Attacker"
                else:
                    return remote_ip, "You"
            else:
                # No remote connections, this is a local user
                local_ip = self.get_local_ip()
                return local_ip, "You"
        except Exception as e:
            print(f"Error determining IP and user: {e}")
            return "Unknown IP", "Unknown"

    def get_active_connections(self):
        """Check for active remote connections using psutil."""
        connections = psutil.net_connections()
        active_connections = []
        for conn in connections:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                remote_ip, remote_port = conn.raddr
                active_connections.append({
                    'remote_ip': remote_ip,
                    'remote_port': remote_port
                })
        return active_connections

    def get_local_ip(self):
        """Retrieve the local machine's IP address."""
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    def check_connection_ip(self, ip):
        try:
            # Get local machine's IP addresses
            local_ips = [ip_info[4][0] for ip_info in psutil.net_if_addrs().values()]
            print(f"Local IPs: {local_ips}")

            # Check if the IP is in the local IP range or is a link-local address
            if ip.startswith("fe80::"):  # Link-local address
                return "Local (Link-local address)"
            elif ip in local_ips:  # Check against the system's local IPs
                return "Local"
            else:
                return "Remote"
        except Exception as e:
            print(f"Error: {e}")
            return "Unknown"

    def show_notification(self, message,file_path):
        notification.notify(
            title='File System Change Detected',
            message=message,
            app_name='File Monitor',
            timeout=10  # Duration for which the notification will be visible
        )


def monitor_directory(callback):
    path = WATCH_DIRECTORY
    event_handler = ChangeHandler(callback)
    observer = Observer()
    # Recursive=True to monitor all subdirectories
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring directory: {path}")

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def callback(message):
    print(message)

if __name__ == "__main__":
    monitor_directory(callback)
