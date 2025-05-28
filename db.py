import sqlite3

def init_db():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS channels (id TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()

def add_channel(channel_id):
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO channels (id) VALUES (?)', (channel_id,))
    conn.commit()
    conn.close()

def remove_channel(channel_id):
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('DELETE FROM channels WHERE id = ?', (channel_id,))
    conn.commit()
    conn.close()

def get_channels():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('SELECT id FROM channels')
    results = c.fetchall()
    conn.close()
    return [row[0] for row in results]
