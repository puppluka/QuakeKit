import tkinter as tk
from tkinter import filedialog, messagebox
import re

class FileEditorApp:
    def __init__(self, root, input_filepath="files.dat"):
        self.root = root
        self.root.title("ASCII Data Editor")
        self.input_filepath = input_filepath
        self.files_data = {}
        self.current_file = None

        self.create_widgets()
        self.load_files_data()
        self.populate_file_list()

    def create_widgets(self):
        # PanedWindow for resizable sections
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left Frame for File List
        self.left_frame = tk.Frame(self.paned_window, bd=2, relief=tk.GROOVE)
        self.paned_window.add(self.left_frame, minsize=150)

        self.file_list_label = tk.Label(self.left_frame, text="Defined Files:")
        self.file_list_label.pack(pady=5)

        self.file_list = tk.Listbox(self.left_frame, selectmode=tk.SINGLE, exportselection=False)
        self.file_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.file_list.bind('<<ListboxSelect>>', self.on_file_select)

        # Right Frame for Text Editor
        self.right_frame = tk.Frame(self.paned_window, bd=2, relief=tk.GROOVE)
        self.paned_window.add(self.right_frame, minsize=300)

        self.text_editor = tk.Text(self.right_frame, wrap="word", undo=True)
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Menu Bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_changes)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_editor.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_editor.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.text_editor.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.text_editor.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.text_editor.event_generate("<<Paste>>"))

    def load_files_data(self):
        self.files_data = {}
        current_filename = None
        current_content = []

        try:
            with open(self.input_filepath, 'r') as f:
                for line in f:
                    if line.startswith('/*') and not line.startswith('*/'):
                        if current_filename:
                            self.files_data[current_filename] = "".join(current_content)
                        current_filename = line[2:].strip()
                        current_content = []
                    elif line.startswith('*/'):
                        if current_filename:
                            self.files_data[current_filename] = "".join(current_content)
                        current_filename = None
                        current_content = []
                    else:
                        if current_filename:
                            current_content.append(line)
                # Add the last file if the file ends without a '*/'
                if current_filename:
                    self.files_data[current_filename] = "".join(current_content)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Input file '{self.input_filepath}' not found.")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading: {e}")
            self.root.quit()

    def populate_file_list(self):
        self.file_list.delete(0, tk.END)
        for filename in self.files_data.keys():
            self.file_list.insert(tk.END, filename)

    def on_file_select(self, event):
        selected_index = self.file_list.curselection()
        if selected_index:
            self.current_file = self.file_list.get(selected_index[0])
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, self.files_data[self.current_file])

    def open_file(self):
        filepath = filedialog.askopenfilename(
            initialdir=".",
            title="Select files.dat",
            filetypes=(("Datalist file", "*.dat"), ("All files", "*.*"))
        )
        if filepath:
            self.input_filepath = filepath
            self.load_files_data()
            self.populate_file_list()
            self.text_editor.delete(1.0, tk.END) # Clear editor after loading new file
            self.current_file = None # Reset current file selection

    def save_changes(self):
        if self.current_file:
            self.files_data[self.current_file] = self.text_editor.get(1.0, tk.END)
        else:
            messagebox.showinfo("No File Selected", "Please select a file to save its changes.")
            return

        try:
            with open(self.input_filepath, 'w') as f:
                for filename, content in self.files_data.items():
                    f.write(f"/*{filename}\n")
                    f.write(content)
                    if not content.endswith('\n'): # Ensure content ends with a newline before closing comment
                        f.write('\n')
                    f.write("*/\n\n")
            messagebox.showinfo("Save Successful", "Changes saved to files.dat!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEditorApp(root)
    root.mainloop()