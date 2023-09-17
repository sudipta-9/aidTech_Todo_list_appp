# todo.py
# Store todo items in a SQL database

import sqlite3
import tkinter
import datetime

# Create a SQLite database connection
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Create the 'items' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node TEXT,
        creationtime DATE
    )
''')
conn.commit()

# Time management
date_time = datetime.datetime.now()
date = date_time.date()  # gives date

class Database:
    @staticmethod
    def drop_and_refresh():
        cursor.execute('DROP TABLE IF EXISTS items')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node TEXT,
                creationtime DATE
            )
        ''')
        conn.commit()

    @staticmethod
    def print_all_items():
        print("---------------------------")
        cursor.execute('SELECT * FROM items')
        for row in cursor.fetchall():
            print(row[0], row[1], sep='. ')

    @staticmethod
    def delete_all_items():
        cursor.execute('DELETE FROM items')
        conn.commit()

    @staticmethod
    def insert_new_item(item):
        curTime = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
        cursor.execute('INSERT INTO items (node, creationtime) VALUES (?, ?)', (item, curTime))
        conn.commit()

    @staticmethod
    def remove_item(identifier):
        cursor.execute('DELETE FROM items WHERE id = ?', (identifier,))
        conn.commit()

class TodoApp(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Todo")

        self.todoList = tkinter.Listbox()
        self.todoList.pack(fill=tkinter.BOTH, expand=0)

        # Entry box & button for new todo items
        self.entry = tkinter.Entry()
        self.entry.pack(fill=tkinter.BOTH, expand=0)

        entryButton = tkinter.Button(text="Enter", command=self.add_to_list)
        entryButton.pack(fill=tkinter.BOTH, expand=0)

        # Delete items box & button
        self.deleteOption = tkinter.Entry()
        self.deleteOption.pack(fill=tkinter.BOTH, expand=0)

        deleteButton = tkinter.Button(text="Delete", command=self.delete_from_list)
        deleteButton.pack(fill=tkinter.BOTH, expand=0)

        # Update the application on startup with items already in the database
        self.refresh_list()

    def refresh_list(self):
        self.todoList.delete(0, tkinter.END)
        cursor.execute('SELECT * FROM items')
        for row in cursor.fetchall():
            item = f"{row[0]}. {row[1]} - Created at {row[2]}"
            self.todoList.insert(tkinter.END, item)
            self.todoList.update_idletasks()

    def add_to_list(self):
        item_text = str(self.entry.get())
        if item_text.strip():
            Database.insert_new_item(item_text)
            self.entry.delete(0, 'end')
            self.refresh_list()
            Database.print_all_items()

    def delete_from_list(self):
        item_id = self.deleteOption.get()
        if item_id.isdigit():
            Database.remove_item(int(item_id))
            self.deleteOption.delete(0, 'end')
            self.refresh_list()
            Database.print_all_items()

if __name__ == "__main__":
    application = TodoApp()
    application.mainloop()
