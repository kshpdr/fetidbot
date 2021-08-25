import psycopg2
import config

conn = psycopg2.connect(config.database_url, sslmode='require')
cur = conn.cursor()

# inserting chat_id in data base
def insert_user(chat_id, message):
    cur.execute("INSERT INTO users (chat_id) \
                VALUES (%d) \
                ON CONFLICT (chat_id) DO NOTHING" % message.chat.id)
    conn.commit()


# # inserting chat_id and photo_name in data base
# def insert_photo(chat_id, message, photo):
#     cur.execute("SELECT * FROM sent_photos")
#     # checking whether photo has been already sent
#     row = cur.fetchone()
#     while row is not None:
#         if row[1] == photo and row[0] == chat_id:
#             return False
#         row = cur.fetchone()
#
#     # if not, addr to database and update photos amount
#     cur.execute("INSERT INTO sent_photos (chat_id, photo_name)\
#                     VALUES (%d, '%s') \
#                 ON CONFLICT ON CONSTRAINT unique_photos DO NOTHING" % (chat_id, photo))
#     cur.execute("UPDATE users SET total_photos = total_photos + 1 WHERE chat_id = '%d'" % chat_id)
#     conn.commit()
#     return True

# inserting chat_id and photo_name in data base
def insert_photo(chat_id, message, photo_url):
    cur.execute("SELECT * FROM photos_sent")
    # checking whether photo has been already sent
    row = cur.fetchone()
    while row is not None:
        if row[1] == photo_url and row[0] == chat_id:
            return False
        row = cur.fetchone()

    # if not, add to database and update photos amount
    cur.execute("INSERT INTO photos_sent (chat_id, photo_link)\
                    VALUES (%d, '%s') \
                ON CONFLICT ON CONSTRAINT unique_photo DO NOTHING" % (chat_id, photo_url))
    cur.execute("UPDATE users SET total_photos = total_photos + 1 WHERE chat_id = '%d'" % chat_id)
    conn.commit()
    return True