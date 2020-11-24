import os
import secrets
from PIL import Image
from peer_rec_sys import db
from flask import current_app
from peer_rec_sys.models import Tag, UserTag, Rec
from flask_login import current_user


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (300, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def insert_tags_to_current_user(strength_form_data, weakness_form_data):
    for tag in strength_form_data:
        with db.session.no_autoflush:
            current_user.tags.append(UserTag(tag_type=True, tag=Tag.query.get(tag)))
    for tag in weakness_form_data:
        with db.session.no_autoflush:
            current_user.tags.append(UserTag(tag_type=False, tag=Tag.query.get(tag)))
    Rec.query.filter(Rec.rec_to_id == current_user.id).delete()
    db.session.commit()

