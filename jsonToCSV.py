import tkinter as tk
from tkinter import filedialog, messagebox
import json
import csv

def flatten_json(nested_json):
    """Flattens nested JSON objects."""
    flat_dict = {}

    def flatten(d, parent_key=''):
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                flatten(v, new_key)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    flatten(item, f"{new_key}_{i}")
            else:
                flat_dict[new_key] = v

    flatten(nested_json)
    return flat_dict

def convert_json_to_csv(json_path, csv_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            raise ValueError("JSON must be a list of dictionaries.")

        # Flatten all JSON objects
        flattened_data = [flatten_json(item) for item in data]

        # Write to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=flattened_data[0].keys())
            writer.writeheader()
            writer.writerows(flattened_data)

    except Exception as e:
        raise e

def browse_json_file():
    filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if filepath:
        json_path_var.set(filepath)

def save_csv_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv")])
    if filepath:
        csv_path_var.set(filepath)

def start_conversion():
    json_path = json_path_var.get()
    csv_path = csv_path_var.get()

    if not json_path or not csv_path:
        messagebox.showwarning("Missing Paths", "Please select both JSON input and CSV output paths.")
        return

    try:
        convert_json_to_csv(json_path, csv_path)
        messagebox.showinfo("Success", "Conversion completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert file:\n{e}")

# GUI setup
root = tk.Tk()
root.title("JSON to CSV Converter")
root.geometry("400x150")

json_path_var = tk.StringVar()
csv_path_var = tk.StringVar()

tk.Label(root, text="JSON File:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
tk.Entry(root, textvariable=json_path_var, width=40).grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_json_file).grid(row=0, column=2, padx=5)

tk.Label(root, text="CSV Output:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
tk.Entry(root, textvariable=csv_path_var, width=40).grid(row=1, column=1)
tk.Button(root, text="Save As", command=save_csv_file).grid(row=1, column=2, padx=5)

tk.Button(root, text="Convert", command=start_conversion, width=20).grid(row=2, column=1, pady=20)

root.mainloop()
