import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import json, os, datetime
from matplotlib import pyplot as plt

DATA_FILE = "data/ecotrack_data.json"

CATEGORIES = ["Travel", "Energy", "Food", "Shopping", "Home", "Work", "Other"]
IMPACTS = ["Low", "Medium", "High", "Neutral"]

# ---------- Data Handling ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Core App ----------
class EcoTrackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 EcoTrack – Daily Sustainability Logger")
        self.root.geometry("850x600")
        self.root.config(bg="#e8f5e9")

        self.data = load_data()
        self.edit_index = None

        # ---------- Style ----------
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Green.TButton", background="#43a047", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Green.TButton", background=[("active", "#2e7d32")])

        style.configure("Red.TButton", background="#e53935", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Red.TButton", background=[("active", "#b71c1c")])

        style.configure("Blue.TButton", background="#1e88e5", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Blue.TButton", background=[("active", "#1565c0")])

        style.configure("Brown.TButton", background="#6d4c41", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Brown.TButton", background=[("active", "#4e342e")])

        style.configure("Treeview", background="#ffffff", foreground="black", rowheight=28, fieldbackground="#f1f8e9", font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#66bb6a", foreground="black", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#a5d6a7")])

        # ---------- Title ----------
        title = tk.Label(root, text="🌱 EcoTrack – Daily Sustainability Logger",
                         font=("Segoe UI", 18, "bold"), bg="#43a047", fg="white", pady=10)
        title.pack(fill="x")

        # ---------- Input Frame ----------
        input_frame = tk.LabelFrame(root, text="Add / Update Activity", bg="#e8f5e9",
                                    font=("Segoe UI", 11, "bold"), fg="#2e7d32", padx=10, pady=10)
        input_frame.pack(pady=15, padx=20, fill="x")

        labels = [
            ("Date:", 0, 0),
            ("Activity:", 0, 2),
            ("Category:", 1, 0),
            ("Impact:", 1, 2),
            ("Notes:", 2, 0)
        ]
        for text, r, c in labels:
            tk.Label(input_frame, text=text, bg="#e8f5e9", font=("Segoe UI", 10, "bold")).grid(row=r, column=c, padx=5, pady=5)

        # Calendar widget for modern date selection
        self.date_entry = DateEntry(input_frame, width=23, background="white", date_pattern="yyyy-mm-dd")
        self.activity_entry = ttk.Entry(input_frame, width=25)
        self.category_entry = ttk.Combobox(input_frame, values=CATEGORIES, width=23, state="readonly")
        self.category_entry.set("Other")
        self.impact_entry = ttk.Combobox(input_frame, values=IMPACTS, width=23, state="readonly")
        self.impact_entry.set("Low")
        self.notes_entry = ttk.Entry(input_frame, width=25)

        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.activity_entry.grid(row=0, column=3, padx=5, pady=5)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)
        self.impact_entry.grid(row=1, column=3, padx=5, pady=5)
        self.notes_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="we")

        # Buttons
        self.add_btn = ttk.Button(input_frame, text="➕ Add Entry", command=self.add_or_save_entry, style="Green.TButton")
        self.add_btn.grid(row=3, column=0, columnspan=3, pady=10, sticky="w")

        self.cancel_btn = ttk.Button(input_frame, text="↩ Cancel Edit", command=self.cancel_edit, style="Red.TButton")
        self.cancel_btn.grid(row=3, column=3, pady=10, sticky="e")
        self.cancel_btn.state(["disabled"])

        # ---------- Table ----------
        table_frame = tk.Frame(root, bg="#e8f5e9")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("Date", "Activity", "Category", "Impact", "Notes"),
                                 show='headings')
        for col in ("Date", "Activity", "Category", "Impact", "Notes"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.tag_configure('oddrow', background="#f1f8e9")
        self.tree.tag_configure('evenrow', background="#ffffff")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # ---------- Buttons ----------
        btn_frame = tk.Frame(root, bg="#e8f5e9")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="✏ Update Selected", command=self.start_update_selected, style="Blue.TButton", width=18).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="🗑 Delete Entry", command=self.delete_entry, style="Red.TButton", width=18).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="📊 View Summary", command=self.view_summary_chart, style="Blue.TButton", width=18).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text="🚪 Exit", command=root.destroy, style="Brown.TButton", width=18).grid(row=0, column=3, padx=10)

        self.refresh_table()

    # ---------- Functions ----------
    def add_or_save_entry(self):
        date_str = self.date_entry.get().strip()
        activity = self.activity_entry.get().strip()
        category = self.category_entry.get().strip()
        impact = self.impact_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not activity or not category:
            messagebox.showerror("Error", "Activity and Category are required.")
            return

        if self.edit_index is None:
            entry = {"date": date_str, "activity": activity, "category": category,
                     "impact": impact, "notes": notes}
            self.data.append(entry)
            save_data(self.data)
            self.refresh_table()
            self.clear_entries()
            messagebox.showinfo("Success", "Entry added successfully!")
        else:
            entry = self.data[self.edit_index]
            entry.update({"date": date_str, "activity": activity, "category": category,
                          "impact": impact, "notes": notes})
            save_data(self.data)
            self.refresh_table()
            self.clear_entries()
            self.edit_index = None
            self.add_btn.config(text="➕ Add Entry", style="Green.TButton")
            self.cancel_btn.state(["disabled"])
            messagebox.showinfo("Success", "Entry updated successfully!")

    def start_update_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry to update.")
            return
        index = self.tree.index(selected[0])
        entry = self.data[index]

        self.date_entry.set_date(entry.get("date", str(datetime.date.today())))
        self.activity_entry.delete(0, tk.END)
        self.activity_entry.insert(0, entry.get("activity", ""))
        self.category_entry.set(entry.get("category", "Other"))
        self.impact_entry.set(entry.get("impact", "Low"))
        self.notes_entry.delete(0, tk.END)
        self.notes_entry.insert(0, entry.get("notes", ""))

        self.edit_index = index
        self.add_btn.config(text="💾 Save Changes", style="Blue.TButton")
        self.cancel_btn.state(["!disabled"])

    def cancel_edit(self):
        if self.edit_index is None:
            return
        self.edit_index = None
        self.clear_entries()
        self.add_btn.config(text="➕ Add Entry", style="Green.TButton")
        self.cancel_btn.state(["disabled"])
        messagebox.showinfo("Cancelled", "Edit cancelled.")

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry to delete.")
            return
        index = self.tree.index(selected[0])
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?"):
            del self.data[index]
            save_data(self.data)
            self.refresh_table()
            if self.edit_index is not None:
                self.edit_index = None
                self.add_btn.config(text="➕ Add Entry", style="Green.TButton")
                self.cancel_btn.state(["disabled"])
            messagebox.showinfo("Deleted", "Entry removed successfully.")

    def view_summary_chart(self):
        if not self.data:
            messagebox.showinfo("No Data", "No entries to show in summary.")
            return

        categories = {}
        for entry in self.data:
            cat = entry.get("category", "Uncategorized")
            categories[cat] = categories.get(cat, 0) + 1

        labels = list(categories.keys())
        sizes = list(categories.values())

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title("🌿 EcoTrack Category Summary", fontsize=14)
        plt.show()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, entry in enumerate(self.data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(
                entry.get("date", ""),
                entry.get("activity", ""),
                entry.get("category", ""),
                entry.get("impact", ""),
                entry.get("notes", "")
            ), tags=(tag,))

    def clear_entries(self):
        self.date_entry.set_date(datetime.date.today())
        self.activity_entry.delete(0, tk.END)
        self.category_entry.set("Other")
        self.impact_entry.set("Low")
        self.notes_entry.delete(0, tk.END)

# ---------- Run App ----------
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    root = tk.Tk()
    app = EcoTrackApp(root)
    root.mainloop()
