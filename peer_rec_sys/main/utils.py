
from peer_rec_sys import db
from peer_rec_sys.models import User, Rec, Friend


class RecommendedList:
    def __init__(self, active_user):
        self.active_user = active_user

        self.sorted_list = list()

        if self.active_user.rec_list:
            self.user_list = self.get_user_list()


            # self.user_list = [user for user in User.query.all()
            #                   if Rec.query.get((self.active_user.id, user.id))
            #                   not in user.rec_to_list
            #                   and user.id != self.active_user.id]
        else:
            self.user_list = self.get_user_list()

    def get_user_list(self):
        user_list = []
        for user in User.query.all():
            if user.id != self.active_user.id:
                user_list.append(user)
                if Rec.query.get((self.active_user.id, user.id)) is not None:
                    user_list.remove(user)
                if Friend.query.get((self.active_user.id, user.id)) is not None:
                    if user in user_list:
                        user_list.remove(user)
        return user_list


    def append_to_rec_list(self, user_to_append, is_a_like):
        rec = Rec(self.active_user, user_to_append, is_a_like)
        db.session.add(rec)
        db.session.commit()

    def update_user_list(self):

        # returns the list of users which have not yet been recommended
        if self.active_user.rec_list:
            self.user_list = self.get_user_list()

        else:
            self.user_list = self.get_user_list()
        if not self.user_list:
            return False

    def add_friend(self, rec_peer):
        if Rec.query.get((self.active_user.id, rec_peer.id)) and Rec.query.get((rec_peer.id, self.active_user.id)):
            if Rec.query.get((self.active_user.id, rec_peer.id)).is_a_like and Rec.query.get(
                    (rec_peer.id, self.active_user.id)).is_a_like:
                db.session.add_all([Friend(self.active_user, rec_peer), Friend(rec_peer, self.active_user)])
                db.session.commit()

    def get_tags(self, user, tag_type):
        tags = list()
        # get strengths
        if tag_type:
            for assoc in user.tags:
                if assoc.tag_type:
                    tags.append(assoc.tag)
        # get weakness
        if not tag_type:
            for assoc in user.tags:
                if not assoc.tag_type:
                    tags.append(assoc.tag)
        # return selected tags
        return tags

    def sim_score(self):
        self.update_user_list()
        self.sorted_list = []

        if self.active_user.tags:
            active_strengths = self.get_tags(self.active_user, True)
            active_weakness = self.get_tags(self.active_user, False)

            for user in self.user_list:
                peer_strengths = list()
                peer_weakness = list()
                peer_score = 0
                if active_strengths:
                    peer_strengths = self.get_tags(user, True)
                    peer_score += self.calc_score(active_strengths, peer_strengths)
                    peer_score += self.calc_reprocity(active_strengths, peer_weakness)
                if active_weakness:
                    peer_weakness = self.get_tags(user, False)
                    peer_score += self.calc_score(active_weakness, peer_weakness)
                    peer_score += self.calc_reprocity(active_weakness, peer_strengths)

                self.sorted_list.append((user, peer_score))

            self.sorted_list = sorted(self.sorted_list, key=lambda peer: peer[1], reverse=True)
            print(self.sorted_list)
            self.user_list = []
            for item in self.sorted_list:
                self.user_list.append(item[0])
            print(self.user_list)

    def calc_score(self, active_tags, peer_tags):
        score = 0
        for tag in peer_tags:
            if tag in active_tags:
                score += 1

        return score / len(active_tags)

    def calc_reprocity(self, active_tags, peer_tags):
        score = 0
        for tag in peer_tags:
            if tag in active_tags:
                score += 1

        return score / len(active_tags)
