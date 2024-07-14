import tkinter as tk
from tkinter import filedialog, messagebox
import os
import struct
import zipfile
import io
from tkinterdnd2 import TkinterDnD, DND_FILES

class DataFrogApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zes-Frogger")
        self.resizable(False, False)  # Lock the window size

        # GUI elements
        self.label_name_game = tk.Label(self, text="Game Name:")
        self.label_name_game.grid(row=0, column=0, padx=10, pady=10)

        self.edit_name_game = tk.Entry(self)
        self.edit_name_game.grid(row=0, column=1, padx=10, pady=10)

        self.label_game_info = tk.Label(self, text="Drag & Drop")
        self.label_game_info.grid(row=3, column=2, padx=10, pady=10)

        self.label_path_nes = tk.Label(self, text="NES Path:")
        self.label_path_nes.grid(row=1, column=0, padx=10, pady=10)

        self.edit_path_nes = tk.Entry(self, state='readonly')  # Disable manual access
        self.edit_path_nes.grid(row=1, column=1, padx=10, pady=10)

        self.button_path_nes = tk.Button(self, text="Browse", command=self.browse_nes)
        self.button_path_nes.grid(row=1, column=2, padx=10, pady=10)

        self.label_path_png = tk.Label(self, text="PNG Path:")
        self.label_path_png.grid(row=2, column=0, padx=10, pady=10)

        self.edit_path_png = tk.Entry(self, state='readonly')  # Disable manual access
        self.edit_path_png.grid(row=2, column=1, padx=10, pady=10)

        self.button_path_png = tk.Button(self, text="Browse", command=self.browse_png)
        self.button_path_png.grid(row=2, column=2, padx=10, pady=10)

        # Placing the buttons in the same line
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.button_build_zes = tk.Button(self.button_frame, text="Build ZES", command=self.build_zes)
        self.button_build_zes.pack(side=tk.LEFT, padx=3)

        self.button_save_png = tk.Button(self.button_frame, text="Dump PNG", command=self.save_png_from_zes)
        self.button_save_png.pack(side=tk.LEFT, padx=3)

        self.button_reset_all = tk.Button(self.button_frame, text="Clear", command=self.reset_all)
        self.button_reset_all.pack(side=tk.LEFT, padx=3)

        self.label_link_home = tk.Label(self, text="Github", fg="blue", cursor="hand2")
        self.label_link_home.grid(row=0, column=2, columnspan=4, padx=3, pady=3)
        self.label_link_home.bind("<Button-1>", lambda e: self.open_url("https://github.com/exorei/Zes-Frogger"))

        # Enable drag and drop for files
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

    def browse_nes(self):
        nes_file = filedialog.askopenfilename(filetypes=[("NES files", "*.nes")])
        if nes_file:
            self.edit_path_nes.config(state='normal')
            self.edit_path_nes.delete(0, tk.END)
            self.edit_path_nes.insert(0, os.path.basename(nes_file))
            self.edit_path_nes.config(state='readonly')
            game_name = os.path.splitext(os.path.basename(nes_file))[0]
            self.edit_name_game.delete(0, tk.END)
            self.edit_name_game.insert(0, game_name)

    def browse_png(self):
        png_file = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if png_file:
            self.edit_path_png.config(state='normal')
            self.edit_path_png.delete(0, tk.END)
            self.edit_path_png.insert(0, os.path.basename(png_file))
            self.edit_path_png.config(state='readonly')

    def build_zes(self):
        nes_path = self.edit_path_nes.get()
        png_path = self.edit_path_png.get()
        game_name = self.edit_name_game.get()

        if not nes_path or not png_path or not game_name:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        zes_path = os.path.join(os.path.dirname(nes_path), f"{game_name}.zes")

        # Create the ZIP archive in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(nes_path, os.path.basename(nes_path))

        zip_data = zip_buffer.getvalue()

        # Read the PNG data
        with open(png_path, 'rb') as png_file:
            png_data = png_file.read()

        # Create the header
        header = bytearray(520)
        game_name_bytes = game_name.encode('ascii')
        header[:len(game_name_bytes)] = game_name_bytes
        header[512:516] = struct.pack('<I', len(png_data))
        header[516:520] = struct.pack('<I', len(zip_data))

        # Write the ZES file
        with open(zes_path, 'wb') as zes_file:
            zes_file.write(header)
            zes_file.write(png_data)
            zes_file.write(zip_data)

        messagebox.showinfo("Success", f"ZES file created successfully: {zes_path}")

    def save_png_from_zes(self):
        zes_path = filedialog.askopenfilename(filetypes=[("ZES files", "*.zes")])
        if not zes_path:
            return

        with open(zes_path, 'rb') as zes_file:
            zes_file.seek(512)
            png_size = struct.unpack('<I', zes_file.read(4))[0]
            zes_file.seek(520)
            png_data = zes_file.read(png_size)

        png_path = os.path.splitext(zes_path)[0] + ".png"
        with open(png_path, 'wb') as png_file:
            png_file.write(png_data)

        messagebox.showinfo("Success", f"Preview image extracted successfully: {png_path}")

    def reset_all(self):
        self.edit_name_game.delete(0, tk.END)
        self.edit_path_nes.config(state='normal')
        self.edit_path_nes.delete(0, tk.END)
        self.edit_path_nes.config(state='readonly')
        self.edit_path_png.config(state='normal')
        self.edit_path_png.delete(0, tk.END)
        self.edit_path_png.config(state='readonly')

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def on_drop(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            if os.path.isdir(file):
                self.process_folder(file)
            elif file.lower().endswith('.nes'):
                self.process_nes_file(file)
            elif file.lower().endswith('.png'):
                self.process_png_file(file)

    def process_folder(self, folder_path):
        nes_file = None
        png_file = None

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.nes'):
                    nes_file = os.path.join(root, file)
                elif file.lower().endswith('.png'):
                    png_file = os.path.join(root, file)

        if nes_file:
            self.process_nes_file(nes_file)
        if png_file:
            self.process_png_file(png_file)

    def process_nes_file(self, nes_file):
        self.edit_path_nes.config(state='normal')
        self.edit_path_nes.delete(0, tk.END)
        self.edit_path_nes.insert(0, nes_file)
        self.edit_path_nes.config(state='readonly')
        game_name = os.path.splitext(os.path.basename(nes_file))[0]
        self.edit_name_game.delete(0, tk.END)
        self.edit_name_game.insert(0, game_name)

    def process_png_file(self, png_file):
        self.edit_path_png.config(state='normal')
        self.edit_path_png.delete(0, tk.END)
        self.edit_path_png.insert(0, png_file)
        self.edit_path_png.config(state='readonly')

if __name__ == "__main__":
    try:
        app = DataFrogApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
