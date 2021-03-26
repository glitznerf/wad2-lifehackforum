import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django

django.setup()

from forum.models import UserAccount, Category, Hack, Comment
from datetime import datetime
from pytz import utc


def populate():
    user_accounts = [{'username': 'adamr55',
                      'password': 'chick3ns',
                      'email': 'adam1233@gmail.com',
                      'verified': True},
                     {'username': 'sarahp3',
                      'password': 'glasgow321',
                      'email': 'sarahp3@hotmail.com',
                      'verified': False},
                     {'username': 'lifehackfan',
                      'password': 'Wx4tt6a1',
                      'email': 'nicola22@gmail.com',
                      'verified': False},
                     {'username': 'jasper999',
                      'password': 'kitten11',
                      'email': 'jasper999@live.co.uk',
                      'verified': True},
                     {'username': 'davidf99',
                      'password': 'london128',
                      'email': 'davidf@outlook.com',
                      'verified': True}]

    categories = [{'categoryName': 'Cleaning',
                   'userName': 'adamr55',
                   'description': 'Hacks related to cleaning'},
                  {'categoryName': 'Beauty and Fashion',
                   'userName': 'jasper999',
                   'description': 'Hacks related to beauty and fashion'},
                  {'categoryName': 'Parenting',
                   'userName': 'sarahp3',
                   'description': 'Hacks related to being a parent'},
                  {'categoryName': 'Organising',
                   'userName': 'davidf99',
                   'description': 'Hacks related to organising'},
                  {'categoryName': 'Cooking',
                   'userName': 'lifehackfan',
                   'description': 'Hacks related to food and cooking.'}]

    hacks = [{'hackID': 1,
              'name': 'Fresh Bananas',
              'description': 'By covering the stems of your bananas with plastic wrap you can keep them fresher for longer',
              'shortDescription': 'Put plastic wrap over banana stems to keep them fresh',
              'likes': 35,
              'userName': 'lifehackfan',
              'categoryName': 'Cooking',
              'dateTimeCreated': None},
             {'hackID': 2,
              'name': 'Zip Hack',
              'description': 'Is your jeans zipper falling down? Use a keyring loop to fasten the zip to a button and keep them up!',
              'shortDescription': 'Use a metal loop to keep jeans from falling down',
              'likes': 12,
              'userName': 'jasper999',
              'categoryName': 'Fashion',
              'dateTimeCreated': None},
             {'hackID': 3,
              'name': 'Mosquito Net Hack',
              'description': "Put a bedsheet over your child's outdoor play area to prevent bugs from biting them",
              'shortDescription': 'Use a sheet to protect your child from bugs',
              'likes': 44,
              'userName': 'sarahp3',
              'categoryName': 'Parenting',
              'dateTimeCreated': None},
             {'hackID': 4,
              'name': 'Bag Storage',
              'description': 'Store any plastic bags you have in an empty packet of wipes for easy storage and retrieval',
              'shortDescription': 'Use empty wipe packets to store carrier bags',
              'likes': 30,
              'userName': 'davidf99',
              'categoryName': 'Organising',
              'dateTimeCreated': None},
             {'hackID': 5,
              'name': 'Foam Plate Hack',
              'description': 'Put foam plates in between dishes to avoid them getting chipped when storing them',
              'shortDescription': 'Use foam plates to protect dishes',
              'likes': 8,
              'userName': 'lifehackfan',
              'categoryName': 'Cooking',
              'dateTimeCreated': None}
             ]

    comments = [{'commentID': 1,
                 'hackID': 1,
                 'userName': 'lifehackfan',
                 'text': 'Wow, so helpful thanks!',
                 'dateTimeCreated': None},
                {'commentID': 2,
                 'hackID': 2,
                 'userName': 'jasper999',
                 'text': 'Great hack, saved my favorite jeans',
                 'dateTimeCreated': None},
                {'commentID': 3,
                 'hackID': 3,
                 'userName': 'sarahp3',
                 'text': 'Cant wait to try this when the sun comes out.',
                 'dateTimeCreated': None},
                {'commentID': 4,
                 'hackID': 4,
                 'userName': 'davidf99',
                 'text': 'Great tip for reducing plastic waste, thank you!',
                 'dateTimeCreated': None},
                {'commentID': 5,
                 'hackID': 5,
                 'userName': 'adamr55',
                 'text': 'No more chipped plates!',
                 'dateTimeCreated': None}
                ]

    for user_account in user_accounts:
        AddUserAccount(user_account['username'], user_account['password'],
                           user_account['email'], user_account['verified'])

    for category in categories:
        AddCategory(category['categoryName'], category['username'], category['description'])

    for hack in hacks:
        AddHack(hack['hackID'], hack['name'], hack['description'], hack['shortDescription'], hack['likes'],
                hack['userName'], hack['categoryName'], hack['dateTimeCreated'])

    for comment in comments:
        AddComment(comment['commentID'], comment['hackID'], hack['userName'], hack['text'], hack['dateTimeCreated'])




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
