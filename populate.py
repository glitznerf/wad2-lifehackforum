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
          'password': 'CharliePass2098',
          'verified': True},
         {'user': 'lifehackfan',
         'email': 'lifehackfan@gmail.com',
          'password': 'passThis69',
          'verified': False},
         {'user': 'jasper999',
         'email': 'jasper999@gmail.com',
          'password': 'weflknlkqcnkq',
          'verified': True},
         {'user': 'davidf99',
         'email': 'davidf99@gmail.com',
          'password': 'notMyPass420',
          'verified': True}]
    userAccounts = []
    for info in userInfo:
        userAccounts.append(AddUserAccount(info['user'], info['email'], info['password'], info['verified']))


    categoryInfo = [
          {'categoryName': 'Gaming',
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
    categories = []
    for info in categoryInfo:
        category = AddCategory(info['categoryName'], info['user'], info['description'])
        categories.append(category)
    
    hackInfo = [
    [     
         {
          'name': 'Clean your mouse',
          'description': 'the best performance you will get out of your mouse is when it is clean! the particles of dirt and dust will cloud the sensor and cause inefficiency',
          'shortDescription': 'clean your mouse for better performance',
          'likes': 35,
          'user': userAccounts[1],
          'category': categories[0]},
         {
          'name': 'Overclock CPU',
          'description': 'if you have an intell CPU thats part number ends in a K you can actually overclock your CPU to get more bang for your CPU buck',
          'shortDescription': 'Overclock your CPU for better gaming performance',
          'likes': 12,
          'user': userAccounts[1],
          'category': categories[0]},
         {
          'name': 'Wait for the sale!',
          'description': "if you play games on PC you should wait for the steam sales. Every season steam offers extensive and genorouse sale prices that will save you a load.",
          'shortDescription': 'Wait for the steam sale to buy your games',
          'likes': 44,
          'user': userAccounts[1],
          'category': categories[0]},
         {
          'name': '360 noscope',
          'description': 'if you turn your input sensitivety to the maximum you can hit those 360s easier than ever',
          'shortDescription': 'max sense equals easier 360s',
          'likes': 30,
          'user': userAccounts[3],
          'category': categories[0]},
         {
          'name': 'street fighter combo',
          'description': 'ive found a brand new street fighter combo! LLRLUDDDDLLRRU , this combo wins you the game instantly!',
          'shortDescription': 'ive found a brand new combo',
          'likes': 8,
          'user': userAccounts[4],
          'category': categories[0]}
    ],
          
    [
        {
          'name': 'invest in lipstick',
          'description': 'over the years i have bought a diverse range of lipstick and i have finally come to the conclusion that the most cost effective lipstick is actually the expensive stuff. I know it sounds counterentuitive but the cheap stuff just doesnt last.',
          'shortDescription': 'cheap lipstick doesnt last',
          'likes': 19,
          'user': userAccounts[0],
          'category': categories[1]},
         {
          'name': 'Tuck in your laces!',
          'description': 'shoe laces are SOOOOoooooo 2010 if you want to have some real style you have to tuck in your laces',
          'shortDescription': 'laces are sooooooooo 2010',
          'likes': 99,
          'user': userAccounts[0],
          'category': categories[1]},
         {
          'name': 'clashing colours are in',
          'description': "comlementary colours are out and clashing is in, clowns are just so COOOLLLL",
          'shortDescription': 'clowns are just so COOOLLLL',
          'likes': 14,
          'user': userAccounts[2],
          'category': categories[1]},
         {
          'name': 'hand-me-downs',
          'description': 'ask your relitives to have a look at thier closets and ask if they have any clothes that they would be happy to give you, some of that retro stuff is supper cool!',
          'shortDescription': 'free retro clothes are a great thing',
          'likes': 32,
          'user': userAccounts[4],
          'category': categories[1]},
         {
          'name': 'custom scarfs',
          'description': 'if you have old or ripped clothes you can cut them into stripps and turn them into a nice new scarf for you and all your friends',
          'shortDescription': 'free custom scarfs, great for gifts',
          'likes': 24,
          'user': userAccounts[0],
          'category': categories[1]}  
    ],
    
    [
        {
          'name': 'here comes the airplane',
          'description': 'if your baby dosnt want to eat its veggies then you can pretend that the spoon is an airplane, they go for it every time.',
          'shortDescription': 'pretend the spoon is an airplane',
          'likes': 5,
          'user': userAccounts[0],
          'category': categories[2]},
         {
          'name': 'charity baby clothes',
          'description': 'if you need baby clothes but are on a bit of a buget you can always hit up the charity shops, they do great prices and are just as good as new.',
          'shortDescription': 'baby on a buget',
          'likes': 20,
          'user': userAccounts[4],
          'category': categories[2]},
         {
          'name': 'clean your dummies',
          'description': "make sure you clean your dummies twice a day to make sure to cut down on bacteria",
          'shortDescription': 'dummies get dirty',
          'likes': 11,
          'user': userAccounts[4],
          'category': categories[2]},
         {
          'name': 'use a leash',
          'description': 'if your litle one is a runner then invest in a dog leash! it makes taking them out so much easier and cuts down on your axiety.',
          'shortDescription': 'use a leash to stop them running off',
          'likes': 1,
          'user': userAccounts[3],
          'category': categories[2]},
         {
          'name': 'repare-velcro shoes',
          'description': 'if your kids shoes have some old velcro that barely stick together you can buy strong velcro tape online and refresh the stickyness of those shoes.',
          'shortDescription': 'get some velcro tape online',
          'likes': 83,
          'user': userAccounts[3],
          'category': categories[2]}  
    ],
    [
         {
          'name': 'Sticky notes',
          'description': 'stick sticky notes everywhere! the more sticky notes you stick the more organised you are!',
          'shortDescription': 'sticky notes equal organisation',
          'likes': 36,
          'user': userAccounts[0],
          'category': categories[3]},
         {
          'name': 'pastel colour code',
          'description': 'normal colour codding is boring and garish, pastel colour codding is the new style',
          'shortDescription': 'pastel coulours are in',
          'likes': 9,
          'user': userAccounts[3],
          'category': categories[3]},
         {
          'name': 'paper diary',
          'description': "many younger people use electronic diaries but they dont relise all of the cool tricks you can do with a paper diary like folding pages, having bookmarks and making a custom binding",
          'shortDescription': 'joys of paper',
          'likes': 19,
          'user': userAccounts[3],
          'category': categories[3]},
         {
          'name': 'fix binder',
          'description': 'if your binder mechanism is beant you can use a pair of pliers to bend it back to good as new',
          'shortDescription': 'if mechanism is bent use pliars',
          'likes': 6,
          'user': userAccounts[1],
          'category': categories[3]},
         {
          'name': 'pin board pins',
          'description': 'you can get super cheap pinboard pins online if you go for sellers with a long delivery time',
          'shortDescription': 'get cheap pins online',
          'likes': 43,
          'user': userAccounts[1],
          'category': categories[3]} 
    ],
    [
         {
          'name': 'season wok',
          'description': 'when you buy a new wok you should use sesame oil to add a protective layer to the surface of the wok',
          'shortDescription': 'make you wok more non-stick',
          'likes': 56,
          'user': userAccounts[2],
          'category': categories[4]},
         {
          'name': 'sharpen those knives',
          'description': 'dont use those automattic knife sharpeners, they make your knife blunt, but a wetstone if you really want a sharp knife',
          'shortDescription': 'dont dull your knives',
          'likes': 13,
          'user': userAccounts[2],
          'category': categories[4]},
         {
          'name': 'substitute meat',
          'description': "if you are looking for a cheap and easy substitute for meat mushrooms are a great option, they have a very similar texture and taste great.",
          'shortDescription': 'tasty tasty mushrooms',
          'likes': 26,
          'user': userAccounts[3],
          'category': categories[4]},
         {
          'name': 'easy mash',
          'description': 'mashed potatoes can take alot of effort but to make them easier you can use a handheld blender, makes is supper fluffy!',
          'shortDescription': 'easy fluffy mash',
          'likes': 7,
          'user': userAccounts[3],
          'category': categories[4]},
         {
          'name': 'homemade hotsause',
          'description': 'if you like your sause spicy but are on a buget you can make your own! just make sure not to add too much vinigar or it will taste discusting',
          'shortDescription': 'cheap tasty hotsause',
          'likes': 9,
          'user': userAccounts[1],
          'category': categories[4]}     
    ]]
    for i in range(len(categories)):
        for info in hackInfo[i]:
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
    h.image.save(imageName, File(open('media/populateImages/'+'POPULATE-FILE ' + imageName, 'rb')))
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
