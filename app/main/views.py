from flask import render_template, session, redirect, url_for, current_app, \
        flash, abort
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm, \
        CommentForm
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import User, Role, Permissions, Post, Comment
from ..crawler import make_data_for_index, make_data_for_internation_geography
from manage import redis_conn

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permissions.WRITE_ARTICLE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = []
    try:
        posts = redis_conn.lrange('posts', 0, -1)
    except Exception as e:
        print 'Redis Server may not be running!'
    if len(posts) == 0:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
    pack_list = make_data_for_index()
    print pack_list[0]
    for k, v in pack_list[0].iteritems():
        print k, '-------->', v

    return render_template('index.html', form=form, posts=posts, pack_list=pack_list, category=1)

@main.route('/geography', methods=['GET', 'POST'])
def geography():
    form = PostForm()
    if current_user.can(Permissions.WRITE_ARTICLE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    pack_list = make_data_for_internation_geography()
    return render_template('index.html', form=form, posts=posts, pack_list=pack_list, category=2)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc())
    return render_template('user.html', user=user, posts=posts)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        flash('Your comment has been published!')
        db.session.add(comment)
        return redirect(url_for('.post', id=post.id))
    comments = Comment.query.order_by(Comment.timestamp.asc()).all()
    return render_template('post_single.html', post=post, form=form, comments=comments)

@main.route('/follow/<username>')
@login_required
@permission_required(Permissions.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permissions.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    follows = user.followers.all()
    return render_template('followers.html', user=user, follows=follows, er_or_ed=True)

@main.route('/followed/<username>')
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    follows = user.followed.all()
    return render_template('followers.html', user=user, follows=follows, er_or_ed=False)

@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    form = CommentForm()
    post = Post.query.get_or_404(id)
    current_user.user_like_post(post)
    #post.user_like_post(current_user._get_current_object())
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        flash('Your comment has been published!')
        db.session.add(comment)
        return redirect(url_for('.post', id=post.id))
    comments = Comment.query.order_by(Comment.timestamp.asc()).all()
    return render_template('post_single.html', post=post, form=form, comments=comments)


@main.route('/unlike/<int:id>', methods=['GET', 'POST'])
@login_required
def unlike(id):
    form = CommentForm()
    post = Post.query.get_or_404(id)
    current_user.user_not_like_post(post)
    #post.user_not_like_post(current_user._get_current_object())
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        flash('Your comment has been published!')
        db.session.add(comment)
        return redirect(url_for('.post', id=post.id))
    comments = Comment.query.order_by(Comment.timestamp.asc()).all()
    return render_template('post_single.html', post=post, form=form, comments=comments)

