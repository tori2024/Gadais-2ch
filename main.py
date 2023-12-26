import hashlib
from flask import Flask, render_template, request, redirect, url_for
import random
import glob
import os
from datetime import datetime
import pytz


def get_japantime():
  japan_tz = pytz.timezone('Asia/Tokyo')
  return datetime.now(japan_tz)


app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route("/bbs/<bbs>")
def bbspage(bbs):
  hoge = ""
  for i in glob.glob(f"bbs/{bbs}/*/"):
    url = i.replace(f"bbs/{bbs}/", "").replace(f"/", "")
    threadtitle = open(f"{i}title.txt", "r").read()
    hoge += f"<a href=\"/bbs/{bbs}/{url}/\">{threadtitle}</a><br>\n"
  return render_template(
      "bbs.html",
      bbsname=open(f"bbs/{bbs}/title.txt", "r").read(),
      bbsdesc=open(f"bbs/{bbs}/description.txt", "r").read(),
      bbsid=bbs,
  ).replace("<!-- bbsthread -->", hoge)


@app.route('/bbs/<bbs>/<thread>/')
def page(bbs, thread):
  return render_template(
      'bbs_thread.html',
      threadtitle=open(f"bbs/{bbs}/{thread}/title.txt", "r").read(),
      bbs=bbs,
      thread=thread,
  ).replace(
      "<!-- messages -->",
      open(f"bbs/{bbs}/{thread}/dat.txt", "r").read().replace("\n", "<br>\n"))


@app.route('/post/<bbs>/<thread>/', methods=['POST'])
def post_message(bbs, thread):
  username = request.form['username'].replace("<", "＜").replace(">", "＞")
  ids = "".join(
      list(hashlib.md5(request.form["ids"].encode()).hexdigest())[0:12])
  if username == "":
    username = "名無しさん"

  username.replace("★", "☆")

  message = request.form['message'].replace("<", "＜").replace(">",
                                                              "＞").replace(
                                                                  "\n", "\n　　")
  open(f"bbs/{bbs}/{thread}/dat.txt", "a").write(
      f"""名前: <b><font color='green'>{username}</font></b> {get_japantime()} ID:{ids}
　　{message}\n\n""")
  return redirect(url_for('page', bbs=bbs, thread=thread))


@app.route('/post_register/<bbs>/', methods=['POST'])
def post2_message(bbs):
  thread = "".join([
      random.choice(
          "1234567890aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ")
      for i in range(32)
  ])
  os.mkdir(f"bbs/{bbs}/{thread}/")
  username = request.form['username'].replace("<", "＜").replace(">", "＞")
  ids = "".join(
      list(hashlib.md5(request.form["ids"].encode()).hexdigest())[0:12])
  if username == "":
    username = "名無しさん"

  username.replace("★", "☆")
  title = request.form['title'].replace("<",
                                        "＜").replace(">",
                                                     "＞").replace("\n", "")

  message = request.form['message'].replace("<", "＜").replace(">",
                                                              "＞").replace(
                                                                  "\n", "\n　　")
  open(f"bbs/{bbs}/{thread}/dat.txt", "a").write(
      f"""名前: <b><font color='green'>{username}</font></b> {get_japantime()} ID:{ids}
　　{message}\n\n""")
  open(f"bbs/{bbs}/{thread}/title.txt", "w").write(title)
  return redirect(url_for('page', bbs=bbs, thread=thread))


@app.route("/bbslist.htm")
def bbslist():
  r = ""
  for i in glob.glob("bbs/*"):
    url = i.replace("bbs/", "")
    r += f"<a href=\"bbs/{url}\">{i}</a><br>\n"
  return render_template("bbslist.html").replace("<!-- r -->", r)


if __name__ == '__main__':
  app.run("0.0.0.0", port=8000, debug=True)
