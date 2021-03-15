from django.contrib import admin
from forum.models import UserAccount, Category, Hack, Comment
admin.site.register(UserAccount)
admin.site.register(Category)
admin.site.register(Hack)
admin.site.register(Comment)