import os
import sqlite3
import json

lang = "it"
output = "data.json"
outputComment = "comment.json"

def crawl(email, password, page, date_crawl):
    # check if page, date_crawl is in DB, don't crawl
    with sqlite3.connect("database.db") as conn:
        cur = conn.execute(
            "SELECT * FROM post WHERE page=? and date_crawl=?", (page, date_crawl)
        )
        res = cur.fetchall()
        if len(res) > 0:
            conn.commit()
            return
    # crawl post
    cmd = "scrapy crawl fb -a email=\"{}\" -a password=\"{}\" -a page=\"{}\" -a lang=\"{}\" -o {}".format(email, password, page, lang, output)
    os.system(cmd)

    datastore = {}
    comment = {}

    with open (output, 'r') as jsonFile:
        datastore = json.load(jsonFile)

    index = 0
    while index < len(datastore):
        url = datastore[index]['url']
        post_id = datastore[index]['post_id']
        # read comment from url
        cmd = "scrapy crawl comments -a email=\"{}\" -a password=\"{}\" -a post=\"{}\" -a lang=\"{}\" -o {}".format(email, password, url, lang, outputComment)
        os.system(cmd)
        # put comment to DB
        if os.path.exists(outputComment):
            if os.stat(outputComment).st_size > 0:
                with open(outputComment, 'r') as commentFile:
                    comment = json.load(commentFile)
                    with sqlite3.connect("database.db") as conn:
                        cur = conn.execute(
                            "SELECT * FROM comment WHERE post_id=?", (post_id,)
                        )
                        res = cur.fetchall()
                        if len(res) == 0:
                            data = json.dumps(comment)
                            conn.execute(
                                "INSERT INTO comment (post_id, data) values (?, ?)",
                                (post_id, data)
                            )
                            conn.commit()
                    # delete comment json file
                os.system("rm -r {}".format(outputComment))
        index +=1

    # put post to DB
    with sqlite3.connect("database.db") as conn:
        index = 0
        while index < len(datastore):
            post_id = datastore[index]['post_id']
            data = json.dumps(datastore[index])
            conn.execute(
                "INSERT INTO post (page, post_id, date_crawl, data) values (?, ?, ?, ?)",
                (page, post_id, date_crawl, data)
            )
            index += 1
            conn.commit()

    os.system("rm -r {}".format(output))