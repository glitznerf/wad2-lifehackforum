from django.contrib import admin
from forum.models import UserAccount, Category, Hack, Comment

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('categoryName',)}
    
class HackAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

admin.site.register(UserAccount)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Hack)
admin.site.register(Comment)