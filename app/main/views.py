from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from ..models import Role, User, Post
from .forms import PostForm


@main.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    form = PostForm()
    if form.validate_on_submit():
        # post = Post(body=form.body.data,
        #             author=current_user._get_current_object())
        # db.session.add(post)
        # db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)
