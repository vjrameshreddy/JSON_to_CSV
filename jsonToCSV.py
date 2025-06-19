import json, csv
import tkinter as tk
from tkinter import filedialog, messagebox

class Json2CsvApp:
    def __init__(self, master):
        self.master = master
        master.title("JSON → CSV Converter")
        master.geometry("400x150")
        
        # Input file
        tk.Label(master, text="JSON file:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.json_path = tk.Entry(master, width=40)
        self.json_path.grid(row=0, column=1, pady=5)
        tk.Button(master, text="Browse…", command=self.browse_json).grid(row=0, column=2, padx=5)

        # Output file
        tk.Label(master, text="CSV file:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.csv_path = tk.Entry(master, width=40)
        self.csv_path.grid(row=1, column=1, pady=5)
        tk.Button(master, text="Save As…", command=self.save_csv).grid(row=1, column=2, padx=5)

        # Convert button
        tk.Button(master, text="Convert", command=self.convert).grid(row=2, column=1, pady=15)

    def browse_json(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON files","*.json"),("All files","*.*")]
        )
        if path: self.json_path.delete(0, tk.END); self.json_path.insert(0, path)

    def save_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files","*.csv"),("All files","*.*")]
        )
        if path: self.csv_path.delete(0, tk.END); self.csv_path.insert(0, path)

    def convert(self):
        jpath, cpath = self.json_path.get(), self.csv_path.get()
        if not jpath or not cpath:
            messagebox.showwarning("Missing info", "Choose both JSON input and CSV output.")
            return

        try:
            with open(jpath, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            if not isinstance(data, list) or not data:
                raise ValueError("JSON must be a non-empty list of objects.")

            # Collect all keys (header row)
            headers = set().union(*(item.keys() for item in data))

            with open(cpath, "w", newline="", encoding="utf-8") as cf:
                writer = csv.DictWriter(cf, fieldnames=list(headers))
                writer.writeheader()
                for entry in data:
                    writer.writerow(entry)

            messagebox.showinfo("Success", f"Converted {len(data)} records.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = Json2CsvApp(root)
    root.mainloop()