import sqlite3


def init_db():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def add_channel(channel_id, custom_message="gmgm"):
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO channels (id, custom_message) VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET custom_message=excluded.custom_message
    ''', (channel_id, custom_message))
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
    c.execute('SELECT id, custom_message FROM channels')
    results = c.fetchall()
    conn.close()
    # Retorna lista de tuplas (id, custom_message)
    return results
