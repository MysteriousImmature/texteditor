import tkinter as tk
from tkinter import filedialog, ttk, messagebox, Scrollbar

# This is just basic text editor that look like DOS Operating System
class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.tabs = []  # To store instances of Text widgets in each tab
        self.current_tab = None  # To keep track of the currently active tab
        self.file_names = []  # To store the names of files in each tab

        self.add_tab()

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_command(label="New Tab", command=self.add_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        theme_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme("light"))
        theme_menu.add_command(label="Dark Theme", command=lambda: self.change_theme("dark"))

        toolbar = tk.Frame(self.root)
        toolbar.pack(side="top", fill="x")

        open_button = tk.Button(toolbar, text="Open", command=self.open_file)
        open_button.pack(side="left", padx=2)

        save_button = tk.Button(toolbar, text="Save", command=self.save_file)
        save_button.pack(side="left", padx=2)

        save_as_button = tk.Button(toolbar, text="Save As", command=self.save_file_as)
        save_as_button.pack(side="left", padx=2)

        new_tab_button = tk.Button(toolbar, text="New Tab", command=self.add_tab)
        new_tab_button.pack(side="left", padx=2)

        theme_button = tk.Button(toolbar, text="Toggle Theme", command=self.toggle_theme)
        theme_button.pack(side="left", padx=2)

        self.theme = "dark"
        self.change_theme(self.theme)

    def add_tab(self):
        new_tab = tk.Frame(self.notebook)
        text_widget = tk.Text(new_tab, wrap="word", undo=True)
        text_widget.pack(expand=True, fill="both")

        scroll_y = Scrollbar(new_tab, command=text_widget.yview)
        scroll_y.pack(side="right", fill="y")
        text_widget['yscrollcommand'] = scroll_y.set

        self.tabs.append(text_widget)
        self.file_names.append(None)
        self.notebook.add(new_tab, text=f"Untitled Document {len(self.tabs)}")
        self.notebook.select(len(self.tabs) - 1)  # Switch to the newly added tab
        self.current_tab = len(self.tabs) - 1
        self.update_tab_title()

        text_widget.bind("<KeyRelease>", self.update_status_bar)

        # Close button on each tab
        close_button = tk.Button(new_tab, text="✖", command=lambda: self.close_tab(len(self.tabs) - 1))
        close_button.pack(side="left", padx=2)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.tabs[self.current_tab].delete(1.0, "end")
                self.tabs[self.current_tab].insert("insert", file_content)

            self.file_names[self.current_tab] = file_path
            self.update_tab_title()

    def save_file(self):
        if self.file_names[self.current_tab]:
            with open(self.file_names[self.current_tab], "w") as file:
                text_content = self.tabs[self.current_tab].get(1.0, "end-1c")
                file.write(text_content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                text_content = self.tabs[self.current_tab].get(1.0, "end-1c")
                file.write(text_content)

            self.file_names[self.current_tab] = file_path
            self.update_tab_title()

    def close_tab(self, index):
        if len(self.tabs) > 1:
            self.notebook.forget(index)
            self.tabs.pop(index)
            self.file_names.pop(index)
            self.update_tab_title()
            if index < self.current_tab:
                self.current_tab -= 1

    def change_theme(self, theme):
        self.theme = theme
        for tab in self.tabs:
            tab.config(bg="black", fg="white") if theme == "dark" else tab.config(bg="white", fg="black")

    def toggle_theme(self):
        if self.theme == "light":
            self.change_theme("dark")
        else:
            self.change_theme("light")

    def update_tab_title(self):
        for i, tab in enumerate(self.tabs):
            if self.file_names[i]:
                tab_title = f"{self.file_names[i].split('/')[-1]}"
            else:
                tab_title = f"Untitled Document {i + 1}"

            self.notebook.tab(i, text=tab_title)

    def update_status_bar(self, event):
        line, column = map(str, self.tabs[self.current_tab].index(tk.INSERT).split("."))
        self.root.status_var.set(f"Line: {line}, Column: {column}")

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.status_var = tk.StringVar()
    status_bar = tk.Label(root, textvariable=root.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side="bottom", fill="x")
    root.mainloop()
