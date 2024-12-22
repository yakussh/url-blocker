# URL Blocker Script
# Written by yakush

import ctypes
import sys
import os
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk  # Theme support

# Check for administrative privileges
def check_admin():
    system_platform = platform.system()
    if system_platform == 'Windows':
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to obtain administrative privileges: {e}")
            sys.exit()
    elif system_platform in ['Linux', 'Darwin']:
        if os.geteuid() != 0:
            messagebox.showerror("Error", "This application requires administrator (sudo) privileges.")
            sys.exit()

# Block URL function
def block_url():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Error", "Please enter a URL!")
        return

    system_platform = platform.system()
    hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts" if system_platform == 'Windows' else "/etc/hosts"
    redirect = "127.0.0.1"

    try:
        with open(hosts_path, "r+") as file:
            lines = file.readlines()
            if any(url in line for line in lines):
                messagebox.showinfo("Info", f"{url} is already blocked.")
                # MessageBox for Blocked URLs
                messagebox.showinfo("Blocked URLs", f"{url} is blocked successfully.")
                return

            file.write(f"\n{redirect} {url}")

        listbox.insert(tk.END, url)
        with open("blocked_urls.txt", "a") as f:
            f.write(f"{url}\n")
        messagebox.showinfo("Success", f"{url} has been successfully blocked.")
        # MessageBox for Allowed URLs
        messagebox.showinfo("Allowed URLs", f"{url} is now blocked and redirected.")
    except PermissionError:
        messagebox.showerror("Error", "You do not have write permissions. Administrative privileges may be required.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Unblock URL function
def unblock_url():
    try:
        selected_url = listbox.get(listbox.curselection()).strip()
    except tk.TclError:
        messagebox.showwarning("Error", "Please select a URL to remove!")
        return

    system_platform = platform.system()
    hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts" if system_platform == 'Windows' else "/etc/hosts"

    try:
        with open(hosts_path, "r") as file:
            lines = file.readlines()

        with open(hosts_path, "w") as file:
            for line in lines:
                if selected_url not in line:
                    file.write(line)

        listbox.delete(listbox.curselection())
        if os.path.exists("blocked_urls.txt"):
            with open("blocked_urls.txt", "r") as f:
                urls = f.readlines()
            with open("blocked_urls.txt", "w") as f:
                for line in urls:
                    if selected_url not in line.strip():
                        f.write(line)
        messagebox.showinfo("Success", f"{selected_url} has been successfully removed.")
        # MessageBox for Allowed URLs
        messagebox.showinfo("Allowed URLs", f"{selected_url} is now unblocked and allowed again.")
    except PermissionError:
        messagebox.showerror("Error", "You do not have write permissions. Administrative privileges may be required.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Load blocked URLs
def load_blocked_urls():
    if os.path.exists("blocked_urls.txt"):
        with open("blocked_urls.txt", "r") as file:
            for line in file:
                listbox.insert(tk.END, line.strip())

# Check for admin privileges
check_admin()

# GUI Design
root = ThemedTk(theme="arc")
root.title("URL Blocker")
root.geometry("600x450")  # Increased size

# Set dark background and light text color
root.tk_setPalette(background="#2C3E50", foreground="#ECF0F1")

frame = ttk.Frame(root, padding="15", style="TFrame")
frame.pack(fill=tk.BOTH, expand=True)

# Label with bold, black font
url_label = ttk.Label(frame, text="Enter the URL you want to block or unblock:", font=("Arial", 12, "bold"), foreground="black")
url_label.pack(pady=10, anchor="w")

# Entry box with bold, black text
url_entry = ttk.Entry(frame, width=50, font=("Arial", 12, "bold"), foreground="black", background="#ECF0F1")
url_entry.pack(pady=10)

button_frame = ttk.Frame(frame)
button_frame.pack(pady=20)

# Custom button styles
style = ttk.Style()
style.configure("TButton",
                background="#27AE60",
                foreground="black",  # Changed to black
                font=("Arial", 12, "bold"),
                padding=10)
style.map("TButton", background=[("active", "#2ECC71")])

# Block URL button with bold black text
block_button = ttk.Button(button_frame, text="Block URL", command=block_url, width=20, style="TButton")
block_button.pack(side=tk.LEFT, padx=10)

# Unblock URL button with bold black text
unblock_button = ttk.Button(button_frame, text="Unblock URL", command=unblock_url, width=20, style="TButton")
unblock_button.pack(side=tk.LEFT, padx=10)

# Listbox label with bold, black text
listbox_label = ttk.Label(frame, text="Blocked URLs:", font=("Arial", 12, "bold"), foreground="black")
listbox_label.pack(pady=10, anchor="w")

# Listbox with bold black text
listbox = tk.Listbox(frame, width=60, height=10, font=("Arial", 12, "bold"), bg="#2C3E50", fg="black", selectbackground="#1ABC9C", selectforeground="white")
listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Load blocked URLs
load_blocked_urls()

root.mainloop()

# Written by yakush
