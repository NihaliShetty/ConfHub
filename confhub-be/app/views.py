import os
import csv
from datetime import datetime
from flask import jsonify, request

from app import app, db
from app.models import AuthToken, User, ConferenceItem, PendingEmails, UniversityProgram, ImpactConference
from app.utils import generate_token, get_conf_detail, logged_in, get_top_conf_detail, RSSFeed
from app.conf import DATASETS_PATH

import sqlite3
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)),"Final DB/db.sqlite3")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    print(data)
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"success": False, "reason": "email_already_exists"})
    user = User(email=data["email"], password=data["password"], name=data["name"], city=data["city"],
                dob=datetime.strptime(data["dob"], "%Y-%m-%d").date())
    token = generate_token()
    auth_token = AuthToken(email=data["email"], token=token)
    db.session.add(user)
    db.session.add(auth_token)
    db.session.commit()
    return jsonify({"success": True, "token": token})


@app.route("/validate-token", methods=["POST"])
def validate_token():
    data = request.get_json()
    print(data)
    if AuthToken.query.filter_by(email=data["email"], token=data["userToken"]).first():
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()
    auth_token = AuthToken.query.filter_by(email=data["email"], token=data["userToken"]).first()
    if auth_token:
        db.session.delete(auth_token)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"], password=data["password"]).first()
    if not user:
        return jsonify({"success": False, "reason": "invalid_credentials"})
    token = generate_token()
    auth_token = AuthToken(email=data["email"], token=token)
    db.session.add(auth_token)
    db.session.commit()
    return jsonify({"success": True, "token": token})


@app.route("/confs", methods=["POST"])
def conferences():
    today = datetime.utcnow().date()
    conferences = []
    rows = ConferenceItem.query.filter(ConferenceItem.date >= today).order_by("date").limit(100)
    for conf in rows:
        conferences.append(get_conf_detail(conf))
    return jsonify({"success": True, "conferences": conferences})


@app.route("/mail",methods=["POST"])
@logged_in
def mail(data, user):
    enddate = datetime.strptime(data["deadline"], "%Y-%m-%d").date()
    queued_email = PendingEmails.query.filter_by(email=data["email"], confname=data["confname"]).first()
    if queued_email:
        return jsonify({"success": True, "already_subscribed": True})
    conf = PendingEmails(
        email=data["email"],confname=data["confname"],deadline=enddate,location=data["location"],
        user=user
    )
    db.session.add(conf)
    db.session.commit()
    return jsonify({"success": True, "already_subscribed": False})


@app.route("/confs-by-single-filter", methods=["POST"])
def confs_by_single_filter():
    data = request.get_json()
    if data["filter"] == "date":
        date = datetime.strptime(data["value"], "%Y-%m-%d").date()
        confs = ConferenceItem.query.filter_by(date=date)
    elif data["filter"] == "category":
        confs = ConferenceItem.query.filter_by(category=data["value"])
    elif data["filter"] == "location":
        confs = ConferenceItem.query.filter_by(location=data["value"])
    conferences = []
    for conf in confs:
        conferences.append(get_conf_detail(conf))
    return jsonify({"success": True, "conferences": conferences})


@app.route("/confs-by-multiple-filters", methods=["POST"])
def confs_by_multiple_filters():
    data = request.get_json()
    filters = {}
    if "date" in data["filters"].keys():
        date = datetime.strptime(data["filters"]["date"], "%Y-%m-%d").date()
        filters["date"] = date
    if "category" in data["filters"].keys():
        filters["category"] = data["filters"]["category"]
    if "location" in data["filters"].keys():
        filters["location"] = data["filters"]["location"]

    today = datetime.utcnow().date()
    confs = ConferenceItem.query.filter_by(**filters).filter(ConferenceItem.date >= today).order_by("date")
    conferences = []
    for conf in confs:
        conferences.append(get_conf_detail(conf))
    return jsonify({"success": True, "conferences": conferences})


@app.route("/conferences-by-impact", methods=["POST"])
def conferences_by_impact():
    today = datetime.utcnow().date()
    conferences = []
    rows = ImpactConference.query.filter(ImpactConference.date >= today).order_by(
        ImpactConference.h_index.desc()).limit(100)
    for conf in rows:
        conferences.append(get_top_conf_detail(conf))
    return jsonify({"success": True, "conferences": conferences})


@app.route("/filter-impact-conferences", methods=["POST"])
def filter_impact_based_conferences():
    data = request.get_json()
    filters = {}
    if "date" in data["filters"].keys():
        date = datetime.strptime(data["filters"]["date"], "%Y-%m-%d").date()
        filters["date"] = date
    if "category" in data["filters"].keys():
        filters["category"] = data["filters"]["category"]
    if "location" in data["filters"].keys():
        filters["location"] = data["filters"]["location"]

    today = datetime.utcnow().date()
    confs = ImpactConference.query.filter_by(**filters).filter(
        ImpactConference.date >= today).order_by(ImpactConference.h_index.desc())
    conferences = []
    for conf in confs:
        conferences.append(get_top_conf_detail(conf))
    return jsonify({"success": True, "conferences": conferences})


@app.route("/list-training-programs", methods=["POST"])
def list_training_programs():
    data = request.get_json()
    if data["query"] == "list_universities":
        query = db.session.query(UniversityProgram.university.distinct().label("university"))
        universities = [row.university for row in query.all()]
        return jsonify({"success": True, "universities": universities})
    if data["query"] == "filter_courses":
        course = data["course"]
        courses = []
        rows = UniversityProgram.query.filter_by(program=course)
        for row in rows:
            courses.append({"university": row.university})
        return jsonify({"success": True, "universities": courses})
    return jsonify({"success": False, "reason": "Invalid Query"})


@app.route("/user-details", methods=["POST"])
@logged_in
def user_details(data, user):
    emails = user.pending_emails
    subscribed_events = [e.confname for e in emails]
    programs = [(p.university, p.program) for p in user.programs]
    return jsonify({"success": True, "events": subscribed_events, "programs": programs, "name": user.name,
                    "city": user.city, "dob": str(user.dob)})


@app.route("/rss-feed", methods=["POST"])
def rss_feed():
    feed = RSSFeed.get_instance()
    return jsonify({"success": True, "entries": feed.li})


@app.route("/admin/update-datasets", methods=["POST"])
def update_datasets():
    if not os.path.isfile(os.path.join(DATASETS_PATH, "WorldConferenceAlerts.csv")):
        return jsonify({"success": False, "reason": "conference_csv_does_not_exist"})
    with open(os.path.join(DATASETS_PATH, "WorldConferenceAlerts.csv"), "r", encoding="utf8") as f:
        print("Reading WorldConferenceAlerts.csv file..")
        reader = csv.reader(f, delimiter=",")
        new_changes = False
        row_count = -1
        print("Rows updated in AllConf (WorldConferenceAlerts): " + format(0, "05d"), end="")
        for row in reader:
            row_count += 1
            if row_count == 0:
                continue
            cells = list(row)
            if not ConferenceItem.query.filter_by(name=cells[2]).first():
                try:
                    date = datetime.strptime(cells[0], "%Y-%m-%d").date()
                except Exception as e:
                    continue
                deadline = datetime.strptime(cells[9], "%Y-%m-%d").date()
                conf = ConferenceItem(
                    date=date, link=cells[1], name=cells[2], organizer=cells[3],
                    category=cells[4], location=cells[5], country=cells[6],
                    website=cells[7], organizer_email=cells[8], deadline=deadline,
                    description=cells[10]
                )
                db.session.add(conf)
                new_changes = True
            print("\b" * 5 + format(row_count, "05d"), end="")
        print()

        if not os.path.isfile(os.path.join(DATASETS_PATH, "TopConf.csv")):
            return jsonify({"success": False, "reason": "TopConf_csv_does_not_exist"})
        with open(os.path.join(DATASETS_PATH, "TopConf.csv"), "r", encoding="utf8") as f:
            print("Reading TopConf.csv file..")
            reader = csv.reader(f, delimiter=",")
            row_count = -1
            print("Rows updated in TopConf: " + format(0, "05d"), end="")
            for row in reader:
                row_count += 1
                if row_count == 0:
                    continue
                cells = list(row)
                if not ImpactConference.query.filter_by(name=cells[2]).first():
                    date = datetime.strptime(cells[0], "%d-%m-%Y").date()
                    deadline = datetime.strptime(cells[7], "%d-%m-%Y").date()
                    conf = ImpactConference(
                        date=date, link=cells[1], name=cells[2], organizer=cells[3],
                        location=cells[4], country=cells[5],
                        website=cells[6], deadline=deadline, h_index=cells[8]
                    )
                    db.session.add(conf)
                    new_changes = True
                print("\b" * 5 + format(row_count, "05d"), end="")
            print()

        if not os.path.isfile(os.path.join(DATASETS_PATH, "UnivPgms.csv")):
            return jsonify({"success": False, "reason": "UnivPgms_csv_does_not_exist"})
        with open(os.path.join(DATASETS_PATH, "UnivPgms.csv"), "r", encoding="utf8") as f:
            print("Reading UnivPgms.csv file..")
            reader = csv.reader(f, delimiter=",")
            row_count = -1
            print("Universities updated in UnivPgms: " + format(0, "05d"), end="")
            for row in reader:
                row_count += 1
                if row_count == 0:
                    continue
                cells = list(row)
                university = cells[0]
                programs = cells[1].split(";;;")
                for program in programs:
                    if not UniversityProgram.query.filter_by(university=university, program=program).first():
                        _program = UniversityProgram(
                            university=university, program=program
                        )
                        db.session.add(_program)
                        new_changes = True
                print("\b" * 5 + format(row_count, "05d"), end="")
            print()

        if new_changes:
            db.session.commit()
        return jsonify({"success": True, "new_changes": new_changes})


@app.route("/interestssignup", methods=["POST","GET"])
def filter_category_signup():
    conferences = []
    data = request.get_json()
    categoryval = data["searchname"]
    # rows = ConferenceItem.query.filter_by(category)
    rows = ConferenceItem.query.filter(ConferenceItem.category.like('%'+categoryval+'%')).limit(10)
    for conf in rows:
        val = conf.category
        if val not in conferences:
            conferences.append(
                conf.category
            )
    return jsonify({"success": True, "conferences": conferences})
    

@app.route("/getsuperclasses", methods=["POST","GET"])
def getsuperclasses():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id,categoryName from categories where id in(SELECT Super from categoryMap);")
            rows = cur.fetchall()
            #print(rows)
            superclasses = []
            for i in range(len(rows)):
                p = dict()
                p["id"] = rows[i][0]
                p["categoryName"] = rows[i][1]
                superclasses.append(p)
            print(superclasses)
    except:
        conn.rollback()
    finally:
        conn.close()
        return jsonify({"success": True, "superclasses": superclasses})
        

@app.route("/getsubclasses", methods=["POST","GET"])
def getsubclasses():
    data = request.args['id']
    # print(data)
    # print(DATABASE)
    # return jsonify(1)
    try:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT Sub from categoryMap where Super=?",[data])
            rows = cur.fetchone()
            #print("hello")
            subclasses = rows[0].split(";")
            l = []
            for i in subclasses:
                cur.execute("SELECT id,categoryName,hasConf from categories where id=?",[i])
                print(rows)
                rows = cur.fetchone()
                p = dict()
                p["id"] = rows[0]
                p["categoryName"] = rows[1]
                p["leaf"] = rows[2]
                l.append(p)
            print(l)
    except:
        conn.rollback()
    finally:
        conn.close()
        #return jsonify(1)
        return jsonify({"success": True, "subclasses": l})