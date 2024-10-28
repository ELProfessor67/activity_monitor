import tkinter as tk
from tkinter import ttk
import time

LOG_FILE = "activity_log.txt"

class FileMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File System Monitor")
        self.root.geometry("700x400")

        self.tree = ttk.Treeview(root, columns=("Path", "IP", "Date", "Type", "User"), show="headings")
        self.tree.heading("Path", text="File Path")
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Type", text="Event Type")
        self.tree.heading("User", text="User")

        self.tree.column("Path", width=200)
        self.tree.column("IP", width=100)
        self.tree.column("Date", width=150)
        self.tree.column("Type", width=80)
        self.tree.column("User", width=100)

        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        self.update_table()

    def update_table(self):
        with open(LOG_FILE, "r") as log_file:
            lines = log_file.readlines()
            self.tree.delete(*self.tree.get_children())  # Clear previous entries
            for line in lines:
                date, event_type, message, ip_info, user_info = line.split(" | ")
                file_path = message.split(": ")[-1]
                ip = ip_info.split(": ")[-1].strip()
                user = user_info.split(": ")[-1].strip()
                self.tree.insert("", tk.END, values=(file_path, ip, date, event_type, user))
        self.root.after(5000, self.update_table)  # Refresh every 5 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMonitorApp(root)
    root.mainloop()
