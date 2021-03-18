import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django

django.setup()

from forum.models import UserAccount, Category, Hack, Comment
from datetime import datetime
from pytz import utc


def populate():
    #TBD


def AddUserAccount(username, password, email, verified):
    u = UserAccount.objects.get_or_create(userName=username, password=password, email=email, verified=verified)[0]
    u.userName = username
    u.password = password
    u.email = email
    u.verified = verified
    u.save()
    return u


def AddCategory(categoryName, userName, description):
    cat = Category.objects.get_or_create(categoryName=categoryName, userName=userName, description=description)[0]
    cat.categoryName = categoryName
    cat.userName = userName
    cat.description = description
    cat.save()
    return cat

def AddHack(hackID, name, description, shortDescription, likes, userName, categoryName, dateTimeCreated):
    h = Hack.objects.get_or_create(hackID=hackID, name=name, description=description, shortDescription=shortDescription,
                                   likes=likes, userName=userName, categoryName=categoryName, dateTimeCreated=dateTimeCreated)[0]
    h.hackID = hackID
    h.name = name
    h.description = description
    h.shortDescription=shortDescription
    h.likes=likes
    h.userName=userName
    h.categoryName=categoryName
    h.dateTimeCreated=dateTimeCreated
    h.save()
    return h

def AddComment(commentID, hackID, userName, text, dateTimeCreated):
    com = Comment.objects.get_or_create(commentID=commentID, hackID=hackID, text=text, dateTimeCreated=dateTimeCreated)[0]
    com.commentID = commentID
    com.hackID = hackID
    com.text = text
    com.dateTimeCreated=dateTimeCreated
    com.save()
    return com



if __name__ == '__main__':
    print('Starting population script...')
    populate()
