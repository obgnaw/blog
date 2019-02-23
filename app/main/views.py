from flask import render_template, redirect, url_for, abort, flash, request, jsonify 
from flask_login import login_required, current_user
from . import main
from ..models import Roles, Users, Posts
from .forms import PostForm
from ..md2html import md2html


@main.route('/article/<int:id>/')
def get_post(id):
    post = Posts.get(id=id)
    return render_template("base_article.html",
            blog_content=post.body,
            static_root="/static/",
            title=post.title,
            summary=post.summary,
            authors=post.author.username,
            toc=post.toc,
        )

@main.route("/")
def index():
    return render_template("articles.html")

@main.route("/api/index/article/")
def get_all_article():
    articles = {}
    for post in Posts.select():
        articles[post.id] = {
        "modify_time": post.timestamp,
        "title": post.title,
        "summary": post.summary,
        "authors": [post.author.username,],
        "publish_date": "2019-02-23",
        "tags": []
        }
    return jsonify(articles)

@main.route('/upload', methods=['GET', 'POST'])
def page_upload():
    if request.method == 'POST':
        f = request.files["md_file"]
        md = md2html()
        html, meta, toc = md.parse(f.read().decode("utf-8"))
        author = Users.get(Users.username == meta.get("authors") )
        post = Posts(
            author = author,
            body = html,
            title = meta.get("title"),
            summary=meta.get("summary", ""),
            toc = toc,
        )
        post.save()
        return redirect(url_for('main.page_upload'))
    return render_template("upload.html")    
