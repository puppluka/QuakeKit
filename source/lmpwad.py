import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct

class WAD2Editor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Quake WAD2 Lumper")
        self.geometry("450x350")

        self.lumps = {}
        self.wad_file_path = None

        self.create_widgets()

    def create_widgets(self):
        # Frame for file selection
        file_frame = tk.Frame(self)
        file_frame.pack(pady=10)

        # Button to add LMPs
        add_button = tk.Button(file_frame, text="Add .LMP files", command=self.add_lmp_files)
        add_button.pack(side=tk.LEFT, padx=5)

        # Button to remove selected LMP
        remove_button = tk.Button(file_frame, text="Remove Selected", command=self.remove_selected)
        remove_button.pack(side=tk.LEFT, padx=5)

        # Listbox to display LMPs
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, width=60, height=10)
        self.listbox.pack(pady=5)

        # Frame for WAD file operations
        wad_frame = tk.Frame(self)
        wad_frame.pack(pady=10)

        # Button to load existing WAD
        load_button = tk.Button(wad_frame, text="Load .WAD File", command=self.load_wad_file)
        load_button.pack(side=tk.LEFT, padx=5)

        # Button to create/save WAD
        save_button = tk.Button(wad_frame, text="Save .WAD File", command=self.save_wad_file)
        save_button.pack(side=tk.LEFT, padx=5)

    def add_lmp_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select .LMP Files",
            filetypes=[("LMP files", "*.lmp"), ("All files", "*.*")]
        )
        for file_path in file_paths:
            # Check if the lump already exists in the list
            base_name = os.path.basename(file_path).split('.')[0].upper()
            if base_name in self.lumps.values():
                messagebox.showwarning("Duplicate", f"Lump '{base_name}' already exists. Please rename the file or remove the existing lump.")
                continue

            file_name = base_name[:16]
            self.lumps[file_name] = {'path': file_path, 'type': 'new', 'data': None, 'size': 0}
            self.listbox.insert(tk.END, file_name)
    
    def remove_selected(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return

        lump_name = self.listbox.get(selected_index[0])
        if lump_name in self.lumps:
            del self.lumps[lump_name]
            self.listbox.delete(selected_index)

    def load_wad_file(self):
        file_path = filedialog.askopenfilename(
            title="Open an existing .WAD file",
            filetypes=[("WAD files", "*.wad"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.wad_file_path = file_path
        self.lumps = {}
        self.listbox.delete(0, tk.END)

        try:
            with open(file_path, 'rb') as f:
                # Read WAD header
                magic = f.read(4)
                if magic != b'WAD2':
                    raise ValueError("Not a valid WAD2 file.")

                num_entries, = struct.unpack('<I', f.read(4))
                dir_offset, = struct.unpack('<I', f.read(4))

                # Read WAD directory
                f.seek(dir_offset)
                for _ in range(num_entries):
                    entry_data = f.read(32)
                    offset, dsize, size, type_byte, _, _, name_bytes = struct.unpack('<IIIBB2s16s', entry_data)
                    name = name_bytes.decode('ascii').split('\x00')[0].upper()

                    # Store lump data as a tuple (offset, size) within the original WAD file
                    self.lumps[name] = {
                        'path': self.wad_file_path,
                        'type': 'existing',
                        'data_info': (offset, size),
                        'size': size
                    }
                    self.listbox.insert(tk.END, name)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load WAD file: {e}")
            self.lumps = {}
            self.listbox.delete(0, tk.END)

    def save_wad_file(self):
        if not self.lumps:
            messagebox.showerror("Error", "No lumps to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".wad",
            filetypes=[("WAD files", "*.wad"), ("All files", "*.*")],
            title="Save WAD File"
        )
        if not save_path:
            return

        try:
            with open(save_path, 'wb') as wad_file:
                # 1. Write a placeholder for the WAD header
                wad_file.write(b"WAD2")
                num_entries = len(self.lumps)
                wad_file.write(struct.pack('<I', num_entries))
                dir_offset_placeholder = wad_file.tell()
                wad_file.write(b"\x00\x00\x00\x00")

                wad_file_directory = []

                # 2. Write the lump data and record directory entries
                with open(self.wad_file_path, 'rb') if self.wad_file_path else open(os.devnull, 'rb') as source_wad:
                    for name, lump_info in self.lumps.items():
                        lump_offset = wad_file.tell()
                        
                        if lump_info['type'] == 'new':
                            with open(lump_info['path'], 'rb') as lmp_file:
                                lump_data = lmp_file.read()
                                wad_file.write(lump_data)
                                lump_size = len(lump_data)
                        else:  # Existing lump
                            source_wad.seek(lump_info['data_info'][0])
                            lump_data = source_wad.read(lump_info['data_info'][1])
                            wad_file.write(lump_data)
                            lump_size = len(lump_data)

                        entry = {
                            'offset': lump_offset,
                            'dsize': lump_size,
                            'size': lump_size,
                            'type': 0x45,  # Type for "console picture"
                            'cmprs': 0,
                            'dummy': 0,
                            'name': name
                        }
                        wad_file_directory.append(entry)

                # 3. Write the directory
                dir_offset = wad_file.tell()
                for entry in wad_file_directory:
                    wad_file.write(struct.pack('<III', entry['offset'], entry['dsize'], entry['size']))
                    wad_file.write(struct.pack('<B', entry['type']))
                    wad_file.write(struct.pack('<B', entry['cmprs']))
                    wad_file.write(struct.pack('<H', entry['dummy']))
                    wad_file.write(entry['name'].encode('ascii').ljust(16, b'\x00'))

                # 4. Update the WAD header with the directory offset
                wad_file.seek(dir_offset_placeholder)
                wad_file.write(struct.pack('<I', dir_offset))

            messagebox.showinfo("Success", f".WAD file created successfully at {save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save WAD file: {e}")

if __name__ == "__main__":
    app = WAD2Editor()
    app.mainloop()