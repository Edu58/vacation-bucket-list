from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Roles(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    user_id = db.relationship('Users', backref='role', lazy='dynamic')


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    pass_hashed = db.Column(db.String, nullable=False)
    profile_path = db.Column(db.String, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    vacations = db.relationship('Vacations', backref='user', lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')
    reactions = db.relationship('Reactions', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User -> {self.email}'

    @property
    def password(self):
        return AttributeError('Password cannot be red')

    @password.setter
    def password(self, password):
        self.pass_hashed = generate_password_hash(password, method='sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.pass_hashed, password)

    def get_id(self):
        return self.user_id


# @login_manager.user_loader
# def load_user(user_id):
#     try:
#         return Users.query.get(int(user_id))
#     except:
#         return None


class Vacations(db.Model):
    __tablename__ = 'vacations'

    vacation_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    pricing = db.Column(db.Integer, nullable=False)
    date_of_visit = db.Column(db.DateTime, nullable=False)
    destination_photo = db.Column(db.String, nullable=True)
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comments = db.relationship('Comments', backref='vacation', lazy='dynamic')
    reactions = db.relationship('Reactions', backref='vacation', lazy='dynamic')

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    def get_likes(self, vacation_id):
        all_likes = []

        vacation = Vacations.query.filter_by(vacation_id=vacation_id).first()
        for reaction in vacation.reactions:
            if reaction.reaction == 1:
                all_likes.append(reaction)

        return len(all_likes)

    def get_dislikes(self, vacation_id):
        all_dislikes = []

        vacation = Vacations.query.filter_by(vacation_id=vacation_id).first()
        for reaction in vacation.reactions:
            if reaction.reaction == 0:
                all_dislikes.append(reaction)

        return len(all_dislikes)


class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)
    vacation_id = db.Column(db.Integer, db.ForeignKey('vacations.vacation_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()


class Reactions(db.Model):
    __tablename__ = 'reactions'

    reaction_id = db.Column(db.Integer, primary_key=True)
    reaction = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    vacation_id = db.Column(db.Integer, db.ForeignKey('vacations.vacation_id'))

    def save_reaction(self):
        db.session.add(self)
        db.session.commit()
