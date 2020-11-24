from flask import render_template, url_for, flash, redirect, request, Blueprint
from peer_rec_sys import db, bcrypt
from peer_rec_sys.models import User, Tag, UserTag, Message
from peer_rec_sys.users.utils import save_picture, insert_tags_to_current_user
from peer_rec_sys.users.forms import RegistationForm, LoginForm, UpdateProfileForm, Taglist, MessageForm

from flask_login import login_user, current_user, logout_user, login_required


users = Blueprint('users', __name__)


# The methods variable is a list of allowed methods passed to the route
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # if form validates the message gets flashed, flash is a one time message
        flash(f'Account created for {form.username.data}!')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # terniary conditional
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    # try:
    #     Rec.query.filter(Rec.rec_to_id == current_user.id).delete()
    #     db.session.query(Friend).delete()
    #     db.session.commit()
    # except:
    #     db.session.rollback()
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # return render_template('profile.html', title='Profile')
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)


@users.route('/tags', methods=['GET', 'POST'])
@login_required
def tags():
    form = Taglist()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    form.strength.choices = [(tag.id, tag.tagname) for tag in Tag.query.all()]
    form.weakness.choices = [(tag.id, tag.tagname) for tag in Tag.query.all()]
    if form.validate_on_submit():
        if not current_user.tags:
            insert_tags_to_current_user(form.strength.data, form.weakness.data)
        else:
            UserTag.query.filter(UserTag.user_id == current_user.id).delete()
            db.session.commit()
            insert_tags_to_current_user(form.strength.data, form.weakness.data)
    else:
        print(form.errors)
    return render_template('tags.html', title='Tags', image_file=image_file, form=form)

@users.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    friendlist = current_user.friend_list
    # if request.method == 'POST':
    #     if request.form:
    #         friend_id = int(request.form['button'])
    #         print(friend_id)
    #         redirect(url_for('send_message', recipient_id=friend_id))
    return render_template('friends.html', title='Friends', friendlist=friendlist)


@users.route('/send_message/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def send_message(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=recipient, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
    messages = []
    messages.extend(Message.query.filter(Message.author == current_user, Message.recipient == recipient).all())
    messages.extend(Message.query.filter(Message.author == recipient, Message.recipient == current_user).all())
    messages.sort(key=lambda r: r.timestamp)
    return render_template('message.html', title='Messages', messages=messages, form=form, recipient=recipient.username)



