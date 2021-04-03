from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


"""
UserAccount model has 2 fields: 
user which implements the django user interface and is pimary key and cascades on dellete
verified which is a boolean value used to keep track whether a suer is verified and has acces to certain features of the webapp
"""
class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True, primary_key=True)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

"""
Category model is used to store information on all of the categories, it has 4 fields:
categoryName is the name of the category and is primary key
user is a foriegn key referancing the user that created the category, if this user is deleted this field is set to null
description is a descrition of the content of the category
slug is the slugified category name used in URLS and is updated autimatically every time the model is saved
"""
class Category(models.Model):
    categoryName = models.CharField(max_length=20, unique=True, primary_key=True)
    user = models.ForeignKey(UserAccount, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=55)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.categoryName)
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.slug

"""
Hack is used to store information on each of the hack posts on the site, it has 10 fields:
hackID is an auto incremented primary key field 
name is the name of the hack 
description is a description of the hack
shortDescription is used for when displaying the hacks on the category page so that there isnt too much text on the page
likes is an integer to keep track of the number of likes the page has, this can then be used for quires to find the most popular hacks 
user is a foriegn key referancing the user that created the hack, if this user is deleted the hack is also delleted 
categoryName is a foriegn key referancing the category that the hack belongs in, if this category is deleted the hack is also delleted
dateTimeCreated is a dateTime field that is initialised to the time the hack is created, this can then be used in queries to get the most recent created hack
slug is the slugified name used in URLS and is updated autimatically every time the model is saved
image is a imageField that makes use of pillow, the image is set to a default image and the images are stored in hackImages folder inside the media root folder
"""
class Hack(models.Model):
    hackID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    shortDescription = models.CharField(max_length=55)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(UserAccount, null=True, on_delete=models.CASCADE)
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
    dateTimeCreated = models.DateTimeField(auto_now_add = True)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to='hackImages', default='default.jpg')
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Hack, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.hackID)

"""
Comment is used to store all of the data on each of the comments made by user on a given hack, it has 5 fields:
commentID is an auto incremented primary key field 
hackID is a foriegn key referancing the hack that the comment is on, if this hack is deleted the comment is also delleted
user is a foriegn key referancing the user that created the comment, if this user is deleted the comment is also delleted 
text is the main text content of the comment 
dateTimeCreated is a dateTime field that is initialised to the time the comment is created
"""
class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    hackID = models.ForeignKey(Hack, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    dateTimeCreated = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.commentID)