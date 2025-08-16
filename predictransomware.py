import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import tkinter as tk
from tkinter import messagebox
import webbrowser
import psutil
from flask import Flask, request

app = Flask(__name__)

# Function to extract features from a file
def extract_features(file_path):
    # Extract file size
    file_size = os.path.getsize(file_path)
    
    # Extract file extension
    file_extension = os.path.splitext(file_path)[1]
    
    # Extract file modification time (in seconds since epoch)
    modification_time = os.path.getmtime(file_path)
    
    # Check if the file extension has changed
    original_extension = file_extension[1:] if file_extension else None
    new_extension = file_extension[1:] if file_extension else None
    extension_changed = 1 if original_extension != new_extension else 0
    
    # Check if the file has .encrypted extension
    is_encrypted = 1 if file_extension == '.encrypted' else 0
    
    # Calculate file entropy
    entropy = calculate_entropy(file_path)
    
    return [file_size, modification_time, extension_changed, is_encrypted, entropy]

# Function to calculate file entropy
def calculate_entropy(file_path):
    # Initialize variables
    entropy = 0
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        byte_freq = [0] * 256
        for byte in f.read():
            byte_freq[byte] += 1
    # Calculate entropy
    for freq in byte_freq:
        if freq != 0:
            p = freq / file_size
            entropy -= p * np.log2(p)
    return entropy

# Function to block ransomware files using IPS rule
def block_ransomware_files(file_paths):
    for file_path in file_paths:
        try:
            # Get the process accessing the file
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Get the list of files opened by the process
                    files_opened = proc.open_files()
                    # Check if the process is accessing the ransomware file
                    for opened_file in files_opened:
                        opened_file_path = os.path.normpath(opened_file.path)
                        if os.path.normpath(file_path) == opened_file_path:
                            process = psutil.Process(proc.pid)
                            process.terminate()
                            print(f"Terminated process accessing file: {file_path}")
                            show_notification(f"Ransomware Blocked", f"Process accessing file {file_path} terminated.")
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            print(f"Failed to terminate process accessing file: {file_path}")
            print(e)

# Function to show GUI notification
def show_notification(title, message, file_paths=None):
    root = tk.Tk()
    root.withdraw()
    if file_paths:
        if messagebox.askyesno("Ransomware Detected", f"{message}\nWould you like to check the files?"):
            webbrowser.open("http://127.0.0.1:5000/")
    else:
        root.after(100, lambda: messagebox.showinfo(title, message))
        root.mainloop()

@app.route("/block_files", methods=["POST"])
def block_files():
    # Load the ransomware samples
    ransomware_samples_dir = 'detected_ransomware'
    ransomware_samples = [os.path.join(ransomware_samples_dir, file) for file in os.listdir(ransomware_samples_dir)]
    
    # Block ransomware files using IPS rule
    block_ransomware_files(ransomware_samples)
    show_notification("Ransomware Blocked", "Ransomware files blocked successfully!", ransomware_samples)
    
    # Move ransomware files to quarantine
    quarantine_dir = 'quarantine'
    if not os.path.exists(quarantine_dir):
        os.makedirs(quarantine_dir)
    for file_path in ransomware_samples:
        file_name = os.path.basename(file_path)
        os.rename(file_path, os.path.join(quarantine_dir, file_name))
    
    return "Ransomware files blocked and quarantined successfully!"

@app.route("/")
def index():
    # Load the ransomware samples
    ransomware_samples_dir = 'detected_ransomware'
    ransomware_samples = [os.path.join(ransomware_samples_dir, file) for file in os.listdir(ransomware_samples_dir)]
    
    # Generate HTML content to display ransomware files
    html_content = "<html><head><title>Detected Ransomware Files</title></head><body>"
    html_content += "<h1>Detected Ransomware Files</h1>"
    html_content += "<ul>"
    for file_path in ransomware_samples:
        html_content += f"<li>{file_path}</li>"
    html_content += "</ul>"
    
    # Add block files button
    html_content += """
    <form action="/block_files" method="post">
        <input type="submit" value="Block Files">
    </form>
    </body></html>"""
    
    # Save HTML content to a file
    with open("templates/detected_ransomware.html", "w") as html_file:
        html_file.write(html_content)
    
    return html_content

if __name__ == "__main__":
    app.run(debug=True)
