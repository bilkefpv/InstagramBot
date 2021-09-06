class Stats:

    def __init__(self):
        self.followed_actual = 0
        self.like = 0
        self.skip = 0
        self.inter = 0
        self.followed_actual = 0
        self.already_followed = 0

    def report(self, liked=False, skipped=False, interact=False, ret=False, followed=False, already_follow=False):
        self.like += liked
        self.skip += skipped
        self.inter += interact
        self.followed_actual += followed
        self.already_followed += already_follow
        if ret:
            print(
                f"Liked posts: {self.like} \nSkipped : {self.skip} \nInteracted:{self.inter}\nFollowed: {self.followed_actual}")

    def followed_on_session(self):
        return self.followed_actual
