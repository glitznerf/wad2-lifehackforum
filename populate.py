import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad2Lifehackforum.settings')

import django

django.setup()

from forum.models import UserAccount, Category, Hack, Comment
from datetime import datetime
from pytz import utc


def populate():
    user_accounts = [{'user': 'adamr55',
                      'verified': True},
                     {'user': 'sarahp3',
                      'verified': False},
                     {'user': 'lifehackfan',
                      'verified': False},
                     {'user': 'jasper999',
                      'verified': True},
                     {'user': 'davidf99',
                      'verified': True}]

    categories = [{'categoryName': 'Cleaning',
                   'user': 'adamr55',
                   'description': 'Hacks related to cleaning',
                    'slug': 'cleaning'},
                  {'categoryName': 'Beauty and Fashion',
                   'user': 'jasper999',
                   'description': 'Hacks related to beauty and fashion',
                    'slug': 'beauty-and-fashion'},
                  {'categoryName': 'Parenting',
                   'user': 'sarahp3',
                   'description': 'Hacks related to being a parent',
                    'slug': 'parenting'},
                  {'categoryName': 'Organising',
                   'user': 'davidf99',
                   'description': 'Hacks related to organising',
                    'slug': 'organising'},
                  {'categoryName': 'Cooking',
                   'user': 'lifehackfan',
                   'description': 'Hacks related to food and cooking.',
                    'slug': 'cooking'}]

    hacks = [{'hackID': 1,
              'name': 'Fresh Bananas',
              'description': 'By covering the stems of your bananas with plastic wrap you can keep them fresher for longer',
              'shortDescription': 'Put plastic wrap over banana stems to keep them fresh',
              'likes': 35,
              'user': 'lifehackfan',
              'categoryName': 'Cooking',
              'dateTimeCreated': None,
              'slug': 'fresh-bananas'},
             {'hackID': 2,
              'name': 'Zip Hack',
              'description': 'Is your jeans zipper falling down? Use a keyring loop to fasten the zip to a button and keep them up!',
              'shortDescription': 'Use a metal loop to keep jeans from falling down',
              'likes': 12,
              'user': 'jasper999',
              'categoryName': 'Fashion',
              'dateTimeCreated': None,
              'slug': 'zip-hack'},
             {'hackID': 3,
              'name': 'Mosquito Net Hack',
              'description': "Put a bedsheet over your child's outdoor play area to prevent bugs from biting them",
              'shortDescription': 'Use a sheet to protect your child from bugs',
              'likes': 44,
              'user': 'sarahp3',
              'categoryName': 'Parenting',
              'dateTimeCreated': None,
              'slug': 'mosquito-net-hack'},
             {'hackID': 4,
              'name': 'Bag Storage',
              'description': 'Store any plastic bags you have in an empty packet of wipes for easy storage and retrieval',
              'shortDescription': 'Use empty wipe packets to store carrier bags',
              'likes': 30,
              'user': 'davidf99',
              'categoryName': 'Organising',
              'dateTimeCreated': None,
              'slug': 'bag-storage'},
             {'hackID': 5,
              'name': 'Foam Plate Hack',
              'description': 'Put foam plates in between dishes to avoid them getting chipped when storing them',
              'shortDescription': 'Use foam plates to protect dishes',
              'likes': 8,
              'user': 'lifehackfan',
              'categoryName': 'Cooking',
              'dateTimeCreated': None,
              'slug': 'foam-plate-hack'}
             ]

    comments = [{'commentID': 1,
                 'hackID': 1,
                 'user': 'lifehackfan',
                 'text': 'Wow, so helpful thanks!',
                 'dateTimeCreated': None},
                {'commentID': 2,
                 'hackID': 2,
                 'user': 'jasper999',
                 'text': 'Great hack, saved my favorite jeans',
                 'dateTimeCreated': None},
                {'commentID': 3,
                 'hackID': 3,
                 'user': 'sarahp3',
                 'text': 'Cant wait to try this when the sun comes out.',
                 'dateTimeCreated': None},
                {'commentID': 4,
                 'hackID': 4,
                 'user': 'davidf99',
                 'text': 'Great tip for reducing plastic waste, thank you!',
                 'dateTimeCreated': None},
                {'commentID': 5,
                 'hackID': 5,
                 'user': 'adamr55',
                 'text': 'No more chipped plates!',
                 'dateTimeCreated': None}
                ]

    for user_account in user_accounts:
        AddUserAccount(user_account['user'], user_account['verified'])

    for category in categories:
        AddCategory(category['categoryName'], category['user'], category['description'], category['slug'])

    for hack in hacks:
        AddHack(hack['hackID'], hack['name'], hack['description'], hack['shortDescription'], hack['likes'],
                hack['user'], hack['categoryName'], hack['dateTimeCreated'], hack['slug'])

    for comment in comments:
        AddComment(comment['commentID'], comment['hackID'], hack['user'], hack['text'], hack['dateTimeCreated'])




def AddUserAccount(user, verified):
    u = UserAccount.objects.get_or_create(user=user, verified=verified)[0]
    u.user = user
    u.verified = verified
    u.save()
    return u


def AddCategory(categoryName, user, description, slug):
    cat = Category.objects.get_or_create(categoryName=categoryName, user=user, description=description, slug=slug)[0]
    cat.categoryName = categoryName
    cat.user = user
    cat.description = description
    cat.slug = slug
    cat.save()
    return cat

def AddHack(hackID, name, description, shortDescription, likes, userName, categoryName, dateTimeCreated):
    h = Hack.objects.get_or_create(hackID=hackID, name=name, description=description, shortDescription=shortDescription,
                                   likes=likes, user=user, categoryName=categoryName, dateTimeCreated=dateTimeCreated, slug=slug)[0]
    h.hackID = hackID
    h.name = name
    h.description = description
    h.shortDescription=shortDescription
    h.likes=likes
    h.user=user
    h.categoryName=categoryName
    h.dateTimeCreated=dateTimeCreated
    h.slug=slug
    h.save()
    return h

def AddComment(commentID, hackID, userName, text, dateTimeCreated):
    com = Comment.objects.get_or_create(commentID=commentID, hackID=hackID,, user=user text=text, dateTimeCreated=dateTimeCreated)[0]
    com.commentID = commentID
    com.hackID = hackID
    com.user = user
    com.text = text
    com.dateTimeCreated=dateTimeCreated
    com.save()
    return com



if __name__ == '__main__':
    print('Starting population script...')
    populate()
