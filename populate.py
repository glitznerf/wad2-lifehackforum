import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad2Lifehackforum.settings')

import django

django.setup()
from django.core.files import File
from forum.models import UserAccount, Category, Hack, Comment
from datetime import datetime
from pytz import utc
from django.contrib.auth.models import User


def populate():
    userInfo = [     
         {'user': 'Amanda',
          'email': 'Amanda99@gmail.com',
          'password': 'AmandaPass1',
          'verified': False},
         {'user': 'Charlie',
         'email': 'Charlie66@gmail.com',
          'password': 'CharliePass2',
          'verified': True},
         {'user': 'lifehackfan',
         'email': 'lifehackfan@gmail.com',
          'password': 'testPass3',
          'verified': False},
         {'user': 'jasper999',
         'email': 'jasper999@gmail.com',
          'password': 'testPass4',
          'verified': True},
         {'user': 'davidf99',
         'email': 'davidf99@gmail.com',
          'password': 'testPass5',
          'verified': True}]
    userAccounts = []
    for info in userInfo:
        userAccounts.append(AddUserAccount(info['user'], info['email'], info['password'], info['verified']))
    
    
    categoryInfo = [{
           'categoryName': 'gaming ',
           'user': userAccounts[0],
           'description': 'Hacks related to gaming'},
          {'categoryName': 'Beauty and Fashion',
           'user': userAccounts[0],
           'description': 'Hacks related to beauty and fashion'},
          {'categoryName': 'Parenting',
           'user': userAccounts[3],
           'description': 'Hacks related to being a parent'},
          {'categoryName': 'Organising',
           'user': userAccounts[3],
           'description': 'Hacks related to Organising'},
          {'categoryName': 'Cooking',
           'user': userAccounts[4],
           'description': 'Hacks related to food and cooking.'}]
    for info in categoryInfo:
        category = AddCategory(info['categoryName'], info['user'], info['description'])
        hackInfo = [{
              'name': 'Fresh Bananas',
              'description': 'By covering the stems of your bananas with plastic wrap you can keep them fresher for longer',
              'shortDescription': 'Put plastic wrap over banana stems to keep them fresh',
              'likes': 35,
              'user': userAccounts[0],
              'category': category},
             {
              'name': 'Zip Hack',
              'description': 'Is your jeans zipper falling down? Use a keyring loop to fasten the zip to a button and keep them up!',
              'shortDescription': 'Use a metal loop to keep jeans from falling down',
              'likes': 12,
              'user': userAccounts[1],
              'category': category},
             {
              'name': 'Mosquito Net Hack',
              'description': "Put a bedsheet over your child's outdoor play area to prevent bugs from biting them",
              'shortDescription': 'Use a sheet to protect your child from bugs',
              'likes': 44,
              'user': userAccounts[2],
              'category': category},
             {
              'name': 'Bag Storage',
              'description': 'Store any plastic bags you have in an empty packet of wipes for easy storage and retrieval',
              'shortDescription': 'Use empty wipe packets to store carrier bags',
              'likes': 30,
              'user': userAccounts[3],
              'category': category},
             {
              'name': 'Foam Plate Hack',
              'description': 'Put foam plates in between dishes to avoid them getting chipped when storing them',
              'shortDescription': 'Use foam plates to protect dishes',
              'likes': 8,
              'user': userAccounts[4],
              'category': category}
              ]
        for info in hackInfo:
            hack = AddHack(info['name'], info['description'], info['shortDescription'], 
                        info['likes'], info['user'], info['category'])
            comments = [
                {'hack': hack,
                 'user': userAccounts[0],
                 'text': 'Wow, so helpful thanks!'},
                {'hack': hack,
                 'user': userAccounts[1],
                 'text': 'Great hack'},
                {'hack': hack,
                 'user': userAccounts[2],
                 'text': 'Cant wait to try this out.'},
                {'hack': hack,
                 'user': userAccounts[3],
                 'text': 'Great tip, thank you!'},
                {'hack': hack,
                 'user': userAccounts[4],
                 'text': 'Thats so cool!'}
                ]
            for comment in comments:
                AddComment(comment['hack'], comment['user'], comment['text'])
                    




def AddUserAccount(userName, email, pword, verified):
    user=User.objects.create_user(userName, email=email, password=pword)
    user.is_superuser=True
    user.is_staff=True
    user.save()
    u = UserAccount.objects.get_or_create(user=user, verified=verified)[0]
    u.user = user
    u.verified = verified
    u.save()
    return u


def AddCategory(categoryName, user, description):
    cat = Category.objects.get_or_create(categoryName=categoryName, user=user, description=description)[0]
    cat.categoryName = categoryName
    cat.user = user
    cat.description = description
    cat.save()
    return cat

def AddHack(name, description, shortDescription, likes, user, category):
    h = Hack.objects.get_or_create(name=name, description=description, shortDescription=shortDescription,
                                   likes=likes, user=user, categoryName=category)[0]
    h.name = name
    h.description = description
    h.shortDescription=shortDescription
    h.likes=likes
    h.user=user
    h.categoryName=category
    h.save()
    imageName = h.slug + '.jpg'
    h.image.save(imageName, File(open('C:/Users/angus/Documents/Uni/2ndYear/computing/OOSE/team project/wad2-lifehackforum/media/populateImages/'+'POULATE-FILE ' + imageName, 'rb')))
    return h

def AddComment(hack, user, text):
    com = Comment.objects.get_or_create(hackID=hack, user=user, text=text)[0]
    com.hackID = hack
    com.user = user
    com.text = text
    com.save()
    return com



if __name__ == '__main__':
    print('Starting population script...')
    populate()
