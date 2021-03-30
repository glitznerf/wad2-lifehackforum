from django import forms
from forum.models import UserAccount, Category, Hack, Comment
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password',)
    
	
class UserAccountForm(forms.ModelForm):
    verified = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserAccount
        fields = ('verified',)


class CategoryForm(forms.ModelForm):
    categoryName = forms.CharField(max_length=20, help_text="Please enter the category name.")
    description = forms.CharField(max_length=55, help_text="Please enter a description.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    user = forms.ModelMultipleChoiceField(queryset=User.objects, widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Category
        fields = ('categoryName', 'description', 'slug', "user")
    def __init__(self, user, *args, **kwargs):
        print("try !!!!!!!!!!!!!!")
        self.user = user
        print("---")
        print(self.user)
        print("---")
        super(CategoryForm, self).__init__(*args, **kwargs)


class HackForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=500)
    shortDescription = forms.CharField(max_length=55)
    dateTimeCreated = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    slug = forms.SlugField(widget=forms.HiddenInput(), required=False)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Hack
        fields = ('name', 'description', 'shortDescription',
                  'slug', 'hackID', 'likes')
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(HackForm, self).__init__(*args, **kwargs)

class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=255)
    dateTimeCreated = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ('text', 'commentID')
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CommentForm, self).__init__(*args, **kwargs)
		
		
class VerificationForm(forms.ModelForm):
    verified = forms.BooleanField()
    class Meta:
        model = UserAccount
        fields = ('verified',)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(VerificationForm, self).__init__(*args, **kwargs)	



		