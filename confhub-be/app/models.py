from app import db

user_program = db.Table("user_program",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("program_id", db.Integer, db.ForeignKey("university_program.id")))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(90), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(30))
    city = db.Column(db.String(30))
    dob = db.Column(db.Date)
    interests = db.Column(db.Text)
    programs = db.relationship("UniversityProgram", secondary=user_program)

    def __repr__(self):
        return "<User %r>" % self.email


class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(90), nullable=False)
    token = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<AuthToken %r>" % self.email + ": " + self.token


class ConferenceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    link = db.Column(db.String(300))
    name = db.Column(db.String(150), unique=True)
    organizer = db.Column(db.String(150))
    category = db.Column(db.String(100))
    location = db.Column(db.String(80))
    country = db.Column(db.String(50))
    website = db.Column(db.String(200))
    organizer_email = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    description = db.Column(db.Text)

    def __repr__(self):
        return "<ConferenceItem %r>" % self.name

class PendingEmails(db.Model):
    email=db.Column(db.String(300),nullable=False,primary_key=True)
    confname=db.Column(db.String(150),nullable=False,primary_key=True,unique=True)
    deadline=db.Column(db.Date,nullable=False)
    location=db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(User, lazy=True, backref="pending_emails")

    def __repr__(self):
        return "<PendingEmails %r>" % self.confname


class UniversityProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<UniversityProgram %r>" % self.university


class ImpactConference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    link = db.Column(db.String(300))
    name = db.Column(db.String(150), unique=True)
    h_index = db.Column(db.Integer)
    organizer = db.Column(db.String(150))
    location = db.Column(db.String(80))
    country = db.Column(db.String(50))
    website = db.Column(db.String(200))
    deadline = db.Column(db.Date)

    def __repr__(self):
        return "<ConferenceItem %r>" % self.name
