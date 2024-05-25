import sqlite3

def setup_database():
    conn = sqlite3.connect('quotes.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT NOT NULL,
        book_title TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        date DATE DEFAULT CURRENT_DATE,
        notes TEXT
    ) 
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()