from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

"""
made all primary keys explicet for clarity

UserAccount implement the django user model

category, hack and comment all store the user that created them rather than 
just the username, this will have to be aquired in either forms.py or views.py

need to add an optional image field to Hack at some point but need to
 mess about with the media root etc to do that 

"""


def getNoUsernameText():
    return "!!!No Username!!!"


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True, primary_key=True)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


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


class Hack(models.Model):
    hackID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    shortDescription = models.CharField(max_length=55)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(UserAccount, null=True, on_delete=models.SET_NULL)
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
    dateTimeCreated = models.DateTimeField(auto_now_add = True)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Hack, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.hackID)


class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    hackID = models.ForeignKey(Hack, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=255)
    dateTimeCreated = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.commentID)