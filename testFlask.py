import subprocess

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    """
    Run spider in another process and store items in file. Simply issue command:

    > scrapy crawl dmoz -o "output.json"

    wait for  this command to finish, and read output.json to client.
    """
    email = "dangviethieu.hntv@gmail.com"
    password = "Lp14061993"
    page = "/groups/1445720959014904"
    lang = "it"
    output = "test.json"
    subprocess.check_output(['scrapy', 'crawl', 'fb', '-a', 'email=', email, '-a', 'password=', password, '-a', 'page=', page, '-a', 'lang=', lang, '-o', output])
    with open("output.json") as items_file:
        return items_file.read()

if __name__ == '__main__':
    app.run(debug=True)