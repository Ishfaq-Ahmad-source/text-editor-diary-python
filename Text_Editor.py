import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

# Main Window
root = tk.Tk()
root.title("Text Editor Diary")
root.geometry("800x600")
root.minsize(600, 400)

current_file = None
auto_save_interval = 30000  # 30 seconds
dark_mode = False

# Functions

def new_file(event=None):
    global current_file
    if text.edit_modified():
        if not ask_save_changes():
            return
    text.delete("1.0", tk.END)
    current_file = None
    root.title("Text Editor Diary")
    text.edit_modified(False)

def open_file(event=None):
    global current_file
    if text.edit_modified():
        if not ask_save_changes():
            return
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text.delete("1.0", tk.END)
            text.insert(tk.END, file.read())
        current_file = file_path
        root.title(f"Text Editor Diary - {os.path.basename(file_path)}")
        text.edit_modified(False)

def save_file(event=None):
    global current_file
    if current_file:
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(text.get("1.0", tk.END))
        text.edit_modified(False)
        status_bar.config(text="Saved")
    else:
        save_as_file()

def save_as_file(event=None):
    global current_file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        current_file = file_path
        save_file()
        root.title(f"Text Editor Diary - {os.path.basename(file_path)}")

def exit_app(event=None):
    if text.edit_modified():
        if not ask_save_changes():
            return
    root.quit()

def ask_save_changes():
    response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes?")
    if response is None:  # Cancel
        return False
    if response:  # Yes
        save_file()
    return True

def update_status(event=None):
    words = len(text.get("1.0", tk.END).split())
    chars = len(text.get("1.0", tk.END)) - 1  # remove trailing newline
    status_bar.config(text=f"Words: {words} | Characters: {chars} | {'Saved' if not text.edit_modified() else 'Unsaved'}")

def toggle_dark_mode():
    global dark_mode
    if dark_mode:
        text.config(bg="white", fg="black", insertbackground="black")
        status_bar.config(bg="#f0f0f0", fg="black")
        dark_mode = False
    else:
        text.config(bg="#1e1e1e", fg="white", insertbackground="white")
        status_bar.config(bg="#333333", fg="white")
        dark_mode = True

def find_replace():
    find_text = simpledialog.askstring("Find", "Enter text to find:")
    if find_text:
        replace_text = simpledialog.askstring("Replace", "Enter replacement text (leave empty to skip):")
        content = text.get("1.0", tk.END)
        occurrences = content.count(find_text)
        if occurrences > 0:
            if replace_text is not None:
                content = content.replace(find_text, replace_text)
                text.delete("1.0", tk.END)
                text.insert(tk.END, content)
                messagebox.showinfo("Find & Replace", f"Replaced {occurrences} occurrence(s).")
            else:
                messagebox.showinfo("Find", f"Found {occurrences} occurrence(s) of '{find_text}'.")
        else:
            messagebox.showinfo("Find", f"No occurrences of '{find_text}' found.")

def auto_save():
    if current_file:
        save_file()
    root.after(auto_save_interval, auto_save)

# Text Area
text = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), undo=True)
text.pack(expand=True, fill=tk.BOTH)

scrollbar = tk.Scrollbar(text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=text.yview)
text.config(yscrollcommand=scrollbar.set)
text.bind("<KeyRelease>", update_status)

# Status Bar
status_bar = tk.Label(root, text="Words: 0 | Characters: 0 | Saved", anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=exit_app)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: text.event_generate("<<Undo>>"))
edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: text.event_generate("<<Redo>>"))
edit_menu.add_command(label="Find & Replace", accelerator="Ctrl+F", command=find_replace)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)

# Keyboard Shortcuts
root.bind("<Control-n>", new_file)
root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_as_file)
root.bind("<Control-q>", exit_app)
root.bind("<Control-f>", lambda e: find_replace())
root.bind("<Control-z>", lambda e: text.event_generate("<<Undo>>"))
root.bind("<Control-y>", lambda e: text.event_generate("<<Redo>>"))

# Start Auto-save
root.after(auto_save_interval, auto_save)

root.mainloop()
