import pymysql


class uploadBookSql(object):
    def __init__(self):
        self.conn = pymysql.connect(host="192.168.1.3", port=3306, user="root", password="root", db="sos", charset='utf8')
        self.cur = self.conn.cursor()


    def selectBookName(self, book_name, bookAuthor):
        self.conn.ping(reconnect=True)
        self.cur.execute("SELECT source_url, fenbiao_id, url FROM maintable_book where book_name='{}' AND author='{}'".format(book_name, bookAuthor))
        self.conn.commit()
        self.conn.close()
        return self.cur.fetchall()

    def insert_update_chapter(self, book_id, chapter_name, chapterIndex, chapterPath, iszhubiao, isspider, chapterUrl, web_site, create_time, bookId):
        self.conn.ping(reconnect=True)
        self.cur.execute("INSERT INTO new_chapter_update(book_id, part_title, `number`, `path`, iszhubiao, isspider, url, source_url, create_time, formal_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (str(book_id), chapter_name, chapterIndex, chapterPath, iszhubiao, isspider, chapterUrl, web_site, create_time, bookId))
        self.conn.commit()
        self.conn.close()

    def select_biquInfo_book(self, bookName, bookAuthor):
        self.conn.ping(reconnect=True)
        self.cur.execute("SELECT source_url, book_name, author, url FROM maintable_book_biqu2 WHERE book_name='{}' AND author='{}'".format(bookName, bookAuthor))
        self.conn.commit()
        self.conn.close()
        return self.cur.fetchall()