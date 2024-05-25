import tkinter as tk
from tkinter import ttk, font, messagebox
from quote_functions import QuoteManager

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.manager = QuoteManager(self)

        # Define fonts for high-DPI screens and buttons
        self.large_font = font.Font(family="Courier 10 Pitch", size=14)
        self.medium_font = font.Font(family="Courier 10 Pitch", size=11)
        self.small_font = font.Font(family="Courier 10 Pitch", size=10)
        self.quote_font = font.Font(family="Courier 10 Pitch", size=11, slant="italic")

        self.setup_ui()
        self.manager.load_quotes()

    def setup_ui(self):
        self.root.title("Quote Manager")

        # Adjust scaling factor for high-DPI screens
        scaling_factor = 2.5  # Increase as needed for better visibility on a 4k screen
        self.root.tk.call('tk', 'scaling', scaling_factor)

        # Set the initial size of the window
        self.root.geometry('1920x1280')  # Width x Height

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Apply styles to Treeview headings
        style = ttk.Style()
        style.configure("Treeview.Heading", font=self.small_font)

        # Apply styles to Treeview rows
        style.configure("Treeview", rowheight=25, font=self.medium_font)

        # Input frame
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.grid(row=0, column=0, sticky=tk.W + tk.E)

        # Configure column 1 (where the input fields are) to be expandable
        input_frame.columnconfigure(1, weight=1)

        tk.Label(input_frame, text="Quote:", font=self.large_font).grid(row=0, column=0, sticky=tk.W)
        self.quote_entry = tk.Text(input_frame, width=100, height=4, font=self.quote_font)
        self.quote_entry.grid(row=0, column=1, sticky=tk.W + tk.E)

        tk.Label(input_frame, text="Book Title:", font=self.large_font).grid(row=1, column=0, sticky=tk.W)
        self.book_entry = tk.Entry(input_frame, width=100, font=self.medium_font)
        self.book_entry.grid(row=1, column=1, sticky=tk.W + tk.E)

        tk.Label(input_frame, text="Author:", font=self.large_font).grid(row=2, column=0, sticky=tk.W)
        self.author_entry = tk.Entry(input_frame, width=100, font=self.medium_font)
        self.author_entry.grid(row=2, column=1, sticky=tk.W + tk.E)

        tk.Label(input_frame, text="Tags:", font=self.large_font).grid(row=3, column=0, sticky=tk.W)
        self.tags_entry = tk.Entry(input_frame, width=100, font=self.medium_font)
        self.tags_entry.grid(row=3, column=1, sticky=tk.W + tk.E)

        tk.Label(input_frame, text="Notes:", font=self.large_font).grid(row=4, column=0, sticky=tk.W)
        self.notes_entry = tk.Text(input_frame, width=100, height=2, font=self.medium_font)
        self.notes_entry.grid(row=4, column=1, sticky=tk.W + tk.E)

        # Add search input and button to the input frame
        tk.Label(input_frame, text="Search:", font=self.large_font).grid(row=6, column=0, sticky=tk.W)
        self.search_entry = tk.Entry(input_frame, width=100, font=self.medium_font)
        self.search_entry.grid(row=6, column=1, sticky=tk.W + tk.E)

        add_button = tk.Button(input_frame, text="Add Quote", command=self.manager.add_quote, font=self.small_font)
        add_button.grid(row=5, column=1, sticky=tk.E, padx=10, pady=5, ipadx=5, ipady=5)

        search_button = tk.Button(input_frame, text="Search", command=self.manager.search_quotes, font=self.small_font)
        search_button.grid(row=7, column=1, sticky=tk.E, padx=10, pady=5, ipadx=5, ipady=5)

        delete_button = tk.Button(input_frame, text="Delete Quote", command=self.manager.delete_quote, font=self.small_font)
        delete_button.grid(row=8, column=1, sticky=tk.E, padx=10, pady=5, ipadx=5, ipady=5)

        # Quotes frame
        quotes_frame = tk.Frame(self.root, padx=10, pady=10)
        quotes_frame.grid(row=1, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        # Use ttk.Treeview for displaying quotes
        self.quotes_tree = ttk.Treeview(quotes_frame, columns=('Quote', 'Book Title', 'Author', 'Notes'), show='headings', height=20)
        self.quotes_tree.heading('Quote', text='Quote')
        self.quotes_tree.heading('Book Title', text='Book Title')
        self.quotes_tree.heading('Author', text='Author')
        self.quotes_tree.heading('Notes', text='Notes')

        self.quotes_tree.column('Quote', width=450, stretch=tk.YES)
        self.quotes_tree.column('Book Title', width=150, stretch=tk.YES)
        self.quotes_tree.column('Author', width=150, stretch=tk.YES)
        self.quotes_tree.column('Notes', width=250, stretch=tk.YES)

        self.quotes_tree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        # Make the columns stretch with the window
        quotes_frame.columnconfigure(0, weight=1)
        quotes_frame.rowconfigure(0, weight=1)

        # Bind the Treeview selection event for double-click
        self.quotes_tree.bind("<Double-1>", self.on_tree_double_click)

    def on_tree_double_click(self, event):
        selected_item = self.quotes_tree.selection()
        if selected_item:
            item = self.quotes_tree.item(selected_item)
            full_quote = item['values'][0]
            book_title = item['values'][1]
            author = item['values'][2]
            notes = item['values'][3]

            # Create a new Toplevel window
            top = tk.Toplevel(self.root)
            top.title("Quote Details")
            top.geometry("800x600")

            # Add a Text widget to display the full quote
            text = tk.Text(top, wrap=tk.WORD, padx=10, pady=10)
            text.insert(tk.END, full_quote + "\n\n", ("italic",))
            text.insert(tk.END, f"Book Title: {book_title}\n\n", ("default",))
            text.insert(tk.END, f"Author: {author}\n\n", ("default",))
            text.insert(tk.END, f"Notes: {notes}", ("default",))

            text.tag_configure("default", font=self.medium_font)
            text.tag_configure("italic", font=self.quote_font)
            text.config(state=tk.DISABLED)  # Make the Text widget read-only
            text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            # Add a button to close the Toplevel window
            close_button = tk.Button(top, text="Close", command=top.destroy, font=self.small_font, padx=10, pady=5)
            close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
