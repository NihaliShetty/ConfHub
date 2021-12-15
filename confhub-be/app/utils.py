from uuid import uuid4
from datetime import datetime, timedelta
from flask import request, jsonify
import feedparser

from .models import AuthToken, User


def generate_token():
    token = str(uuid4()) + str(uuid4())
    return token


def get_conf_detail(conf):
    return {
        "id": conf.id,
        "name": conf.name,
        "date": str(conf.date),
        "link": conf.link,
        "location": conf.location,
        "organizer": conf.organizer,
        "category": conf.category,
        "country": conf.country,
        "website": conf.website,
        "email": conf.organizer_email,
        "deadline": str(conf.deadline),
        "description": conf.description,
    }


def get_top_conf_detail(conf):
    return {
        "id": conf.id,
        "name": conf.name,
        "date": str(conf.date),
        "link": conf.link,
        "location": conf.location,
        "organizer": conf.organizer,
        "country": conf.country,
        "website": conf.website,
        "deadline": str(conf.deadline),
        "h_index": conf.h_index
    }


def logged_in(fn):
    def wrapped_fn(*args, **kwargs):
        data = request.get_json()
        if not AuthToken.query.filter_by(email=data["email"], token=data["userToken"]).first():
            return jsonify({"success": False, "reason": "Invalid User Credentials"})
        user = User.query.filter_by(email=data["email"]).first()
        return fn(data, user, *args, **kwargs)
    wrapped_fn.__name__ = fn.__name__
    return wrapped_fn


class RSSFeed:
    instance = None

    def __init__(self):
        self.li = []
        self.created_on = datetime.utcnow()
        d = feedparser.parse('https://www.techmeme.com/feed.xml')
        for post in d.entries:
            self.li.append(post.title)

    @staticmethod
    def get_instance():
        if RSSFeed.instance and RSSFeed.instance.created_on > datetime.utcnow() - timedelta(seconds=30):
            return RSSFeed.instance
        print("Refreshing feed..")
        RSSFeed.instance = RSSFeed()
        return RSSFeed.instance
