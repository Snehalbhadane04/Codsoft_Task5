import tkinter as tk
from tkinter import messagebox
import json
import os
import re

CONTACTS_FILE = 'contacts.json'

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_contacts():
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.match(pattern, email)

def show_validation_errors(name, phone, email):
    valid = True
    if not name:
        name_error.config(text="Name is required")
        valid = False
    else:
        name_error.config(text="")

    if not phone:
        phone_error.config(text="Phone is required")
        valid = False
    elif not validate_phone(phone):
        phone_error.config(text="Must be 10 digits")
        valid = False
    else:
        phone_error.config(text="")

    if email and not validate_email(email):
        email_error.config(text="Invalid email format")
        valid = False
    else:
        email_error.config(text="")

    return valid

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if not show_validation_errors(name, phone, email):
        return

    contacts[name] = {'Phone': phone, 'Email': email, 'Address': address}
    save_contacts()
    update_list()
    clear_fields()
    messagebox.showinfo("Success", f"Contact '{name}' added.")

def update_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("No selection", "Select a contact from the list to update.")
        return

    old_name = list(list(contacts.keys()))[selected[0]]
    new_name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if not show_validation_errors(new_name, phone, email):
        return

    if new_name != old_name:
        del contacts[old_name]

    contacts[new_name] = {'Phone': phone, 'Email': email, 'Address': address}
    save_contacts()
    update_list()
    clear_fields()
    messagebox.showinfo("Success", f"Contact '{new_name}' updated.")

def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("No selection", "Select a contact from the list to delete.")
        return

    name = list(list(contacts.keys()))[selected[0]]
    if messagebox.askyesno("Confirm Delete", f"Delete contact '{name}'?"):
        del contacts[name]
        save_contacts()
        update_list()
        clear_fields()

def search_contact():
    query = search_entry.get().lower().strip()
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        if query in name.lower() or query in info['Phone']:
            listbox.insert(tk.END, f"{name} - {info['Phone']}")

def update_list():
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        listbox.insert(tk.END, f"{name} - {info['Phone']}")

def on_select(event):
    if listbox.curselection():
        index = listbox.curselection()[0]
        name = list(list(contacts.keys()))[index]
        info = contacts[name]
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

        name_entry.insert(0, name)
        phone_entry.insert(0, info['Phone'])
        email_entry.insert(0, info['Email'])
        address_entry.insert(0, info['Address'])

        clear_errors()

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    listbox.selection_clear(0, tk.END)
    clear_errors()

def clear_errors():
    name_error.config(text="")
    phone_error.config(text="")
    email_error.config(text="")

contacts = load_contacts()

# GUI setup
root = tk.Tk()
root.title("Contact Book")
root.geometry("750x430")
root.configure(bg="#f0f9ff")
root.resizable(False, False)

label_style = {"bg": "#f0f9ff", "fg": "#01579b", "font": ("Arial", 10, "bold")}
entry_style = {"bg": "#ffffff", "fg": "#000000", "font": ("Arial", 10)}
error_style = {"bg": "#f0f9ff", "fg": "red", "font": ("Arial", 8)}

# Labels
tk.Label(root, text="Name", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky='w')
tk.Label(root, text="Phone", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky='w')
tk.Label(root, text="Email", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky='w')
tk.Label(root, text="Address", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky='w')

# Entry fields
name_entry = tk.Entry(root, width=30, **entry_style)
phone_entry = tk.Entry(root, width=30, **entry_style)
email_entry = tk.Entry(root, width=30, **entry_style)
address_entry = tk.Entry(root, width=30, **entry_style)

name_entry.grid(row=0, column=1, padx=5, pady=2)
phone_entry.grid(row=1, column=1, padx=5, pady=2)
email_entry.grid(row=2, column=1, padx=5, pady=2)
address_entry.grid(row=3, column=1, padx=5, pady=2)

# Error labels under fields
name_error = tk.Label(root, text="", **error_style)
phone_error = tk.Label(root, text="", **error_style)
email_error = tk.Label(root, text="", **error_style)

name_error.grid(row=0, column=2, sticky='w')
phone_error.grid(row=1, column=2, sticky='w')
email_error.grid(row=2, column=2, sticky='w')

# Buttons
btn_style = {"bg": "#0288d1", "fg": "white", "font": ("Arial", 10, "bold"), "width": 12}

tk.Button(root, text="Add", command=add_contact, **btn_style).grid(row=4, column=0, pady=10)
tk.Button(root, text="Update", command=update_contact, **btn_style).grid(row=4, column=1)
tk.Button(root, text="Delete", command=delete_contact, **btn_style).grid(row=5, column=0)
tk.Button(root, text="Clear", command=clear_fields, **btn_style).grid(row=5, column=1)

# Search
tk.Label(root, text="Search", **label_style).grid(row=6, column=0, padx=10, pady=5, sticky='w')
search_entry = tk.Entry(root, width=30, **entry_style)
search_entry.grid(row=6, column=1, padx=5, pady=5)
tk.Button(root, text="Search", command=search_contact, **btn_style).grid(row=6, column=2, padx=5)

# Contact list
listbox = tk.Listbox(root, width=40, height=17, bg="#ffffff", fg="#000000", font=("Arial", 10))
listbox.grid(row=0, column=3, rowspan=7, padx=15, pady=10)
listbox.bind('<<ListboxSelect>>', on_select)

update_list()
root.mainloop()
