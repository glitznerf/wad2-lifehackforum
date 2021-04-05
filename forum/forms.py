from django import forms
from forum.models import UserAccount, Category, Hack, Comment
from django.contrib.auth.models import User

#have to specify the password field is a PasswordInput so that the password appears hidden on the template
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password',)
    
#the user field is initialised in the views.py file, verified filed is just set to false
class UserAccountForm(forms.ModelForm):
    verified = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserAccount
        fields = ('verified',)

#the slug is initialised in the Category model in the save function
#the user field is initialised in the views.py file
class CategoryForm(forms.ModelForm):
    categoryName = forms.CharField(max_length=20, help_text="Please enter the category name.")
    description = forms.CharField(max_length=55, help_text="Please enter a description.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Category
        fields = ('categoryName', 'description', 'slug')

#the image file is optional and is set to a default in models.py if not provided 
#the user field is initialised in the views.py file
#the category field is initialised in the views.py file
#the datetime feild is initialised to the time at which the hack is created in models.py
#the slug is initialised in the Category model in the save function
class HackForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    shortDescription = forms.CharField(max_length=55)
    description = forms.CharField(max_length=500)
    image = forms.ImageField(required=False)
    dateTimeCreated = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Hack
        fields = ('name','shortDescription','description','image',
                  'slug', 'hackID', )

#the user field is initialised in the views.py file
#the hack field is initialised in the views.py file
class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=255)
    dateTimeCreated = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ('text', 'commentID')
			