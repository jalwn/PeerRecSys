from flask import Blueprint, render_template, url_for
from peer_rec_sys import db
from peer_rec_sys.models import Tag
from peer_rec_sys.main.forms import LikeForm, Taglist2
from peer_rec_sys.main.utils import RecommendedList
from flask_login import current_user




main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        # clear = RecClear()
        # if clear.validate_on_submit():
        #     Rec.querrrry.filter(Rec.rec_to_id == current_user.id).delete()
        #     db.session.commit()
        rec_list = RecommendedList(current_user)
        rec_list.sim_score()
        print(rec_list.user_list)
        form = LikeForm()

        if form.validate_on_submit():
            if rec_list.user_list:
                rec_peer = rec_list.user_list[0]
                rec_list.append_to_rec_list(rec_peer, form.like.data)
                rec_list.sim_score()
                rec_list.add_friend(rec_peer)
                print(rec_list.user_list)
                print(current_user.rec_list)
        if rec_list.user_list:
            rec_peer = rec_list.user_list[0]
            image_file = url_for('static', filename='profile_pics/' + rec_peer.image_file)
            return render_template('home.html', rec_peer=rec_peer, form=form, list_empty=False, image_file=image_file)
        else:
            return render_template('home.html', list_empty=True)
    else:
        return render_template('home-ua.html')

@main.route('/hello', methods=['GET', 'POST'])
def hello_world():
    form = Taglist2()
    form.tags.choices = [(tag.id, tag.tagname) for tag in Tag.query.all()]
    if form.validate_on_submit():
        form.tags.choices = [(tag.id, tag.tagname) for tag in Tag.query.all()]
        if form.tags.data:
            for tag in form.tags.data:
                Tag.query.filter_by(id=tag).delete()
            db.session.commit()
        if form.enterTag.data == '':
            print(False)
        else:
            tag = Tag(tagname=form.enterTag.data)
            db.session.add(tag)
            db.session.commit()
    else:
        print(form.errors)
    return render_template('example.html', form=form)

