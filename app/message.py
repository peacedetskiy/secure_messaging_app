from db import get_db
from config import DB_SECRET


def send_message(sender, recipient, content):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO message (content, sender, recipient) VALUES (pgp_sym_encrypt(%s, %s), %s, %s)',
        (content, DB_SECRET, sender, recipient)
    )
    db.commit()
    return True


def get_messages(caller):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        'SELECT pgp_sym_decrypt(content::bytea, %s), sender, recipient, timestamp FROM message WHERE (sender = %s '
        'OR recipient = %s) ORDER BY timestamp DESC',
        (DB_SECRET, caller, caller)
    )
    messages = cursor.fetchall()
    if messages:
        return messages
    else:
        return None
