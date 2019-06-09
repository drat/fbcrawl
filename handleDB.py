# -*- coding: utf-8 -*-
import sqlite3
import json

def readDB(table, id=None, time=None):
    with sqlite3.connect("database.db") as conn:
        command = ""
        if table == "post":
            if id is not None and time is not None:
                command = "SELECT * FROM {} WHERE page=\"{}\" and date_crawl=\"{}\"".format(table, id, time)
            elif id is not None:
                command = "SELECT * FROM {} WHERE page=\"{}\"".format(table, id)
            else:
                command = "SELECT * FROM {}".format(table)
        elif table == "comment":
            if id is not None:
                command = "SELECT * FROM {} WHERE post_id=\"{}\"".format(table, id)
            else:
                command = "SELECT * FROM {}".format(table)
        elif table == 'page':
            if id is not None:
                command = "SELECT * FROM {} WHERE page_id=\"{}\"".format(table, id)
            else:
                command = "SELECT * FROM {}".format(table)
        elif table == 'account':
            command = "SELECT * FROM {}".format(table)
        cur = conn.execute(command)
        res = cur.fetchall()
        conn.commit()
        return res

def storePage2DB(page_name, page_link, page_method, page_class, page_number):
    with sqlite3.connect("database.db") as conn:
        cur = conn.execute(
            """SELECT * FROM page WHERE page_link=?;""",
            (page_link,)
        )
        res = cur.fetchall()
        if len(res) == 0:
            cur = conn.execute("""
                INSERT INTO page (page_name, page_link, page_method, page_class, page_number) VALUES (?, ?, ?, ?, ?);""",
                (page_name, page_link, page_method, page_class, page_number)
            )
            conn.commit()

def updatePage(id, page_name, page_link, page_method, page_class, page_number):
    with sqlite3.connect("database.db") as conn:
        cur = conn.execute(
            """SELECT * FROM page WHERE page_id=?;""",
            (id,)
        )
        print(conn)
        res = cur.fetchall()
        if len(res) > 0:
            cur = conn.execute("""
                UPDATE page SET page_name=?, page_link=?, page_method=?, page_class=?, page_number=? WHERE page_id=?;""",
                (page_name, page_link, page_method, page_class, page_number, id)
            )
            conn.commit()

def deletePage(id):
    with sqlite3.connect("database.db") as conn:
        cur = conn.execute(
            """SELECT * FROM page WHERE page_id=?;""",
            (id,)
        )
        res = cur.fetchall()
        if len(res) > 0:
            cur = conn.execute("""
                DELETE FROM page WHERE page_id=?;""",
                (id,)
            )
            conn.commit()

def updateAccount(account_email, account_password):
    with sqlite3.connect("database.db") as conn:
        cur = conn.execute(
            """SELECT * FROM account WHERE account_email=?;""",
            (account_email,)
        )
        res = cur.fetchall()
        if len(res) > 0:
            cur = conn.execute("""
                UPDATE account SET account_password=? WHERE account_email=?;""",
                (account_password, account_email)
            )
        else:
            cur = conn.execute("""DELETE FROM account;""")
            cur = conn.execute("""
                INSERT INTO account (account_email, account_password) VALUES (?, ?);""",
                (account_email, account_password)
            )
        conn.commit()

# updateAccount("dangviethieu.hntv", "122")

# page_link = "https://www.facebook.com/groups/1445720959014904/"
# page_name = "Lập trình Swift"
# page_name = page_name.decode('utf-8')
# storePage2DB(page_name, page_link, "model", "group", 1)
# page = readDB(table="page")
# print("{}".format(page[0][0].encode('utf-8')))