import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from datetime import datetime
import sqlite3
import tkinter.messagebox

# Initialize main window
root = tk.Tk()
root.title("Treeview Example")

# Initialize frame
f2 = tk.Frame(root)
f2.pack()

# Initialize Treeview
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack()

# Define headings
tv.heading(1, text="ID")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# Define select_record function
def select_record(event):
    selected = tv.focus()
    values = tv.item(selected, 'values')
    item_name_entry.delete(0, tk.END)
    item_price_entry.delete(0, tk.END)
    purchase_date_entry.delete(0, tk.END)
    item_name_entry.insert(0, values[1])
    item_price_entry.insert(0, values[2])
    purchase_date_entry.insert(0, values[3])

# Bind Treeview
tv.bind("<ButtonRelease-1>", select_record)

# Style for Treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# Database functions
def init_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY,
            item_name TEXT,
            item_price TEXT,
            purchase_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_records():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM records')
    rows = cursor.fetchall()
    for row in rows:
        tv.insert('', 'end', values=row)
    conn.close()

def save_record(id, item_name, item_price, purchase_date):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (id, item_name, item_price, purchase_date)
        VALUES (?, ?, ?, ?)
    ''', (id, item_name, item_price, purchase_date))
    conn.commit()
    conn.close()

def delete_record_from_db(id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM records WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_record_in_db(id, item_name, item_price, purchase_date):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE records
        SET item_name = ?, item_price = ?, purchase_date = ?
        WHERE id = ?
    ''', (item_name, item_price, purchase_date, id))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Call fetch_records function
fetch_records()

# Input fields and button
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Item Name").grid(row=0, column=0)
item_name_entry = tk.Entry(input_frame)
item_name_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Item Price").grid(row=1, column=0)
item_price_entry = tk.Entry(input_frame)
item_price_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Purchase Date").grid(row=2, column=0)
purchase_date_entry = tk.Entry(input_frame)
purchase_date_entry.grid(row=2, column=1)

def add_record():
    item_name = item_name_entry.get()
    item_price = item_price_entry.get()
    purchase_date = purchase_date_entry.get()
    new_id = len(tv.get_children()) + 1
    tv.insert('', 'end', values=(new_id, item_name, item_price, purchase_date))
    save_record(new_id, item_name, item_price, purchase_date)

add_button = tk.Button(input_frame, text="Add Item", command=add_record, bg="lightgreen")
add_button.grid(row=3, column=0, pady=10, padx=5)

# Define delete_record function
def delete_record():
    selected_item = tv.selection()[0]
    item_id = tv.item(selected_item, 'values')[0]
    tv.delete(selected_item)
    delete_record_from_db(item_id)

delete_button = tk.Button(input_frame, text="Delete Item", command=delete_record, bg="lightcoral")
delete_button.grid(row=3, column=1, pady=10, padx=5)

# Define update_record function
def update_record():
    selected = tv.focus()
    item_id = tv.item(selected, 'values')[0]
    tv.item(selected, values=(item_id, item_name_entry.get(), item_price_entry.get(), purchase_date_entry.get()))
    update_record_in_db(item_id, item_name_entry.get(), item_price_entry.get(), purchase_date_entry.get())

update_button = tk.Button(input_frame, text="Update Item", command=update_record, bg="lightblue")
update_button.grid(row=3, column=2, pady=10, padx=5)

# Define set_current_date function
def set_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    purchase_date_entry.delete(0, tk.END)
    purchase_date_entry.insert(0, current_date)

current_date_button = tk.Button(input_frame, text="Set Current Date", command=set_current_date, bg="lightyellow")
current_date_button.grid(row=3, column=3, pady=10, padx=5)

# Define calculate_total_balance function
def calculate_total_balance():
    total_balance = 0
    for row_id in tv.get_children():
        row = tv.item(row_id, 'values')
        total_balance += float(row[2].replace('$', ''))
    tk.messagebox.showinfo("Total Balance", f"Total Balance: ${total_balance:.2f}")

total_balance_button = tk.Button(input_frame, text="Total Balance", command=calculate_total_balance, bg="lightpink")
total_balance_button.grid(row=3, column=4, pady=10, padx=5)

# Start main loop
root.mainloop()