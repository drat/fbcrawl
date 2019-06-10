import requests
from bs4 import BeautifulSoup
import sqlite3
import json

def login(session, email, password):
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)

    assert response.status_code == 302
    assert 'c_user' in response.cookies
    return response.cookies

def findUidWithoutLogin(PROTECTED_URL):
    try:
        response = requests.get(PROTECTED_URL)
        soup = BeautifulSoup(response.text, "lxml")
        url = soup.find("meta",  property="al:android:url")
        uid = url['content'][13:]
        profile_img = "https://graph.facebook.com/{}/picture?type=large".format(uid)
        return profile_img
    except Exception as e:
        print("error: {}".format(e))
        return ""

def findUidWitLogin(USERNAME, PASSWORD, PROTECTED_URL):
    try:
        session = requests.session()
        cookies = login(session, USERNAME, PASSWORD)
        response = session.get(PROTECTED_URL, cookies=cookies, allow_redirects=False)

        soup = BeautifulSoup(response.text, "lxml")
        url = soup.find("meta",  property="al:android:url")
        print(url)
        uid = url['content'][13:]
        profile_img = "https://graph.facebook.com/{}/picture?type=large".format(uid)
        return profile_img
    except Exception as e:
        print("error: {}".format(e))
        return ""

def findUid(USERNAME, PASSWORD, PROTECTED_URL):
    try:
        res = readProfileImg(PROTECTED_URL)
        if len(res) == 0:
            profile_img = findUidWithoutLogin(PROTECTED_URL)
            if profile_img == "":
                profile_img = findUidWitLogin(USERNAME, PASSWORD, PROTECTED_URL)
            updateProfileImg(PROTECTED_URL, profile_img)
            return profile_img
        else:
            return res[0][2]
    except Exception as e:
        print("error: {}".format(e))
        return ""

def readProfileImg(link):
    with sqlite3.connect("database.db") as conn:
        cur = conn.execute(
            """SELECT * FROM profile WHERE link=?;""",
            (link,)
        )
        res = cur.fetchall()
        conn.commit()
        return res

def updateProfileImg(link, profile_img):
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            INSERT INTO profile (link, profile_img) VALUES (?, ?);""",
            (link, profile_img)
        )
        conn.commit()