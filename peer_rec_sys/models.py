from flask_login import UserMixin
from peer_rec_sys import db, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserTag(db.Model):
    __tablename__ = 'usertag'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    tag_type = db.Column(db.Boolean, unique=False, nullable=False)
    tag = db.relationship('Tag', back_populates='users')
    user = db.relationship('User', back_populates='tags')


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(160), unique=False, nullable=False, default="")
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    tags = db.relationship('UserTag', back_populates='user')
    rec_users = db.relationship('User',
                                secondary='rec_user',
                                primaryjoin='User.id==rec_user.c.user_id',
                                secondaryjoin='User.id==rec_user.c.rec_id',
                                backref='rec_to'
                                )
    # rec_user = association_proxy('is_a_rec', 'rec_user')
    # rec_to = association_proxy('is_the_user', 'rec_to')

rec_user = db.Table('rec_user',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('rec_id', db.Integer, db.ForeignKey('user.id'))
)

class Rec(db.Model):
    __tablename__ = 'rec'
    rec_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    rec_to = db.relationship('User',
                             primaryjoin=(User.id==rec_to_id),
                             backref='rec_list')

    in_rec_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    in_rec = db.relationship('User',
                    primaryjoin=(User.id==in_rec_id),
                    backref='rec_to_list')

    is_a_like = db.Column(db.Boolean, unique=False, nullable=False)

    def __init__(self, user, userToRec, is_like):
        self.rec_to = user
        self.in_rec = userToRec
        self.is_a_like = is_like

    # To add users to rec table
    # Rec(_user, _user2, True) if user likes user2
    # Rec(_user2, _user) if user2 ignores user

    # Access
    # someUser.rec_to
    # someUser.in_rec


class Friend(db.Model):
    __tablename__ = 'friend'
    friend_of_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    friend_of = db.relationship('User',
                             primaryjoin=(User.id==friend_of_id),
                             backref='friend_list')

    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    friend = db.relationship('User',
                    primaryjoin=(User.id==friend_id),
                    backref='friend_of_list')


    def __init__(self, user, friend):
        self.friend_of = user
        self.friend = friend

    # To add users to rec table
    # Rec(_user, _user2, True) if user likes user2
    # Rec(_user2, _user) if user2 ignores user

    # Access
    # someUser.friend_list
    # someUser.friend_of_list


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',
                                   primaryjoin=(User.id==sender_id),
                                   backref='message_sent')

    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient = db.relationship('User',
                             primaryjoin=(User.id == recipient_id),
                             backref='message_recieved')

    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, author, recipient, body):
        self.author = author
        self.recipient = recipient
        self.body = body

    def __repr__(self):
        return f"{self.body}"



class Tag(db.Model):
    __tablename = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(120), unique=True, nullable=False)
    users = db.relationship('UserTag', back_populates='tag')
