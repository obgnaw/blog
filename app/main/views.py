from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from ..models import Roles, Users, Posts
from .forms import PostForm
from ..md2html import md2html


@main.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(body=form.body.data,
                    author=current_user._get_current_object())
        # db.session.commit()
        post.save()
        return redirect(url_for('.index'))
    # Posts.delete().execute()
    posts = Posts.select()
    return render_template('index.html', form=form, posts=posts)

@main.route('/blog/')
def blog():
    md = md2html()
    # print(md)
    post = Posts.get()
    # print(post.body)
    html, meta, toc = md.parse(post.body)
    return md.render(html, meta, toc)
    # form = PostForm()
    # return render_template('index.html', form=form)