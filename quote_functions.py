import tkinter as tk
import sqlite3
from tkinter import messagebox

class QuoteManager:
    def __init__(self, app):
        self.app = app

    def add_quote(self):
        quote = self.app.quote_entry.get("1.0", "end-1c")
        book_title = self.app.book_entry.get()
        author = self.app.author_entry.get()
        tags = self.app.tags_entry.get()
        notes = self.app.notes_entry.get("1.0", "end-1c")

        if not quote or not book_title or not author:
            messagebox.showerror("Input Error", "Quote, Book Title, and Author are required")
            return

        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO quotes (quote, book_title, author, tags, notes)
        VALUES (?, ?, ?, ?, ?)
        ''', (quote, book_title, author, tags, notes))
        conn.commit()
        conn.close()

        self.clear_entries()
        self.load_quotes()

    def clear_entries(self):
        self.app.quote_entry.delete("1.0", "end")
        self.app.book_entry.delete(0, "end")
        self.app.author_entry.delete(0, "end")
        self.app.tags_entry.delete(0, "end")
        self.app.notes_entry.delete("1.0", "end")

    def load_quotes(self):
        for row in self.app.quotes_tree.get_children():
            self.app.quotes_tree.delete(row)

        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, quote, book_title, author, notes FROM quotes')
        for row in cursor.fetchall():
            # Insert only the desired columns
            self.app.quotes_tree.insert('', tk.END, values=row[1:], iid=row[0], tags=('font',))
        conn.close()

    def search_quotes(self):
        search_term = self.app.search_entry.get()

        for row in self.app.quotes_tree.get_children():
            self.app.quotes_tree.delete(row)

        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT id, quote, book_title, author, notes FROM quotes
        WHERE quote LIKE ? OR book_title LIKE ? OR author LIKE ? OR tags LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        for row in cursor.fetchall():
            self.app.quotes_tree.insert('', "end", values=row[1:], iid=row[0])
        conn.close()

    def delete_quote(self):
        selected_item = self.app.quotes_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a quote to delete")
            return

        # Retrieve the ID stored as iid
        quote_id = int(selected_item[0])

        conn = sqlite3.connect('quotes.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM quotes WHERE id=?', (quote_id,))
        conn.commit()
        conn.close()

        self.app.quotes_tree.delete(selected_item)
