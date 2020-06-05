import sqlite3
global db

class database_c(object):
    def __init__(self):
        print("ji")
        db = sqlite3.connect("review_db.db")

    def create_table(search_string=None):
        c_query = "create table " + search_string + "(name text,rating text,comment_head text,comment text)"
        db.execute(c_query)
        return

    def insert_rec( search_String=None, reviews=None):
        i_query = "insert into " + search_String + "(name,rating,comment_head,comment) values(?,?,?,?)"
        db.execute(i_query, (reviews[0], reviews[1], reviews[2], reviews[3]))

    def commit_(self):
        db.commit()

    def retrieve_rec(self,search_string=None):
        res_query="select * from "+search_string+"order by name"
        results=db.execute(res_query)
        return results

    def sql_fetch(self):
        cursorObj = db.cursor()
        print('HI')
        cursorObj.execute('SELECT name from sqlite_master WHERE type = "table"')
        return cursorObj.fetchall()