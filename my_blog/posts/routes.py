from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required

from my_blog import db
from my_blog.models import Post
from my_blog.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route("/all_posts")
@login_required
def all_posts():
    """
    Все посты пользователя
    :return: возвращает шаблон all_posts.html с переменной posts
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('all_posts.html', posts=posts)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Форма создания поста
    :return: возвращает шаблон create_post.html с переменной form
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан!', 'success')
        return redirect(url_for('posts.all_posts'))
    return render_template('create_post.html',
                           title='Новый пост', form=form, legend='Новый пост')


@posts.route("/post/<int:post_id>")
def post(post_id):
    """
    Просмотр поста
    :param post_id: id поста
    :return: возвращает шаблон post.html с переменной post
    """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    Изменение поста
    :param post_id: id поста
    :return: возвращает шаблон create_post.html с переменной form
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост изменён!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Изменение поста', form=form, legend='Изменение поста')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Удаление поста
    :param post_id: id поста
    :return: возвращает шаблон all_posts.html с переменной posts
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('posts.all_posts'))