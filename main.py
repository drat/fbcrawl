from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import json
import handleDB
import handleCrawl
import sqlite3
from datetime import date

# page = "/groups/1445720959014904"
data_page = []
data_account = []

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('home.html')

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        today = date.today().strftime("%Y-%m-%d")
        # create table DB
        with sqlite3.connect("database.db") as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS post(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page varchar(255),
                    post_id varchar(30),
                    date_crawl varchar(255),
                    data text
                );"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS comment(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id varchar(30),
                    data text
                );"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS page(
                    page_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page_name varchar(512),
                    page_link varchar(512),
                    page_method varchar(255),
                    page_class varchar(255),
                    page_number INTEGER
                );"""
            )
            conn.execute(
                """CREATE TABLE IF NOT EXISTS account(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_email varchar(512),
                    account_password varchar(512)
                );"""
            )
            conn.commit()
        # data = handleDB.readDB(table="post", id=page)
        # # print("{}".format(data[0][0]))
        # data_total = []
        # index = 0
        # while index < len(data):
        #     # find comment based on post_id
        #     post_id = data[index][1]
        #     comment = handleDB.readDB(table="comment", id=post_id)
        #     comment_json = {}
        #     if len(comment) > 0:
        #         comment_json = json.loads(comment[0][1]) 
        #     # print(json.loads(comment[0][1])[0])
        #     data_format = {
        #         "page": data[index][0],
        #         "post_id": post_id,
        #         "date_crawl": data[index][2],
        #         "data": json.loads(data[index][3]),
        #         "comment": comment_json
        #     }
        #     data_total.append(data_format)
        #     index += 1
        # return render_template('quynh.html', data_crawl=data_total)
        data_page = []
        data_crawl = []
        pages = handleDB.readDB(table="page")
        for index, page in enumerate(pages):
            data_format = {
                "id": index + 1,
                "page_id": page[0],
                "page_name": page[1],
                "page_link": page[2],
                "page_method": page[3],
                "page_class": page[4],
                "page_number": page[5]
            }
            data_page.append(data_format)

            datas = handleDB.readDB(table="post", id=page[2], time=today)
            for index, data in enumerate(datas):
                post_id = data[2]
                comment = handleDB.readDB(table="comment", id=post_id)
                comment_json = {}
                if len(comment) > 0:
                    comment_json = json.loads(comment[0][2]) 
                data_format = {
                    "id": index + 1,
                    "page": page[1],
                    "post_id": post_id,
                    "date_crawl": data[3],
                    "data": json.loads(data[4]),
                    "comment": comment_json
                }
                data_crawl.append(data_format)

        data_account = []
        accounts = handleDB.readDB(table="account")
        if len(accounts) > 0:
            data_format = {
                "id": accounts[0][0],
                "email": accounts[0][1],
                "password": accounts[0][2]
            }
            data_account.append(data_format)

        return render_template('quynh.html', data_page=data_page, data_account=data_account, data_crawl=data_crawl)

@app.route('/', methods=['POST'])
def savePage():
    print("save page")
    if 'savePage' in request.form:
        page_name = request.form['page_name']
        page_link = request.form['page_link']
        page_method = request.form['page_method']
        page_class = request.form['page_class']
        if page_name != '' and page_link != '' and page_method != '' and page_class != '':
            handleDB.storePage2DB(page_name, page_link, page_method, page_class, 1)
        return redirect(url_for('home'))

@app.route('/delete_page/<string:id>')
def delete_page(id):
    handleDB.deletePage(id)
    return redirect(url_for('home'))

@app.route('/get_page/<string:id>', methods=['POST'])
def get_page(id):
    page = handleDB.readDB(table='page', id=id)
    data_format = {
        "page_id": page[0][0],
        "page_name": page[0][1],
        "page_link": page[0][2],
        "page_method": page[0][3],
        "page_class": page[0][4],
        "page_number": page[0][5]
    }
    return json.dumps(data_format)

@app.route('/update_page/<string:id>', methods=['POST'])
def update_page(id):
    page_name = request.form['page_name']
    page_link = request.form['page_link']
    page_method = request.form['page_method']
    page_class = request.form['page_class']
    page_number = request.form['page_number']
    handleDB.updatePage(id, page_name, page_link, page_method, page_class, page_number)
    return json.dumps({'status':'OK'})

@app.route('/update_account', methods=['POST'])
def update_account():
    account_email = request.form['account_email']
    account_password = request.form['account_password']
    handleDB.updateAccount(account_email, account_password)
    return json.dumps({'status':'OK'})

@app.route('/crawl')
def crawl():
    accounts = handleDB.readDB(table="account")
    pages = handleDB.readDB(table="page")
    today = date.today().strftime("%Y-%m-%d")
    for page in pages:
        handleCrawl.crawl(accounts[0][1], accounts[0][2], page[2], today)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'POST':
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session['logged_in'] = True
        else:
            flash('wrong password!')
        return home()
    else:
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000, threaded=True)