from django.db import models
"""
made all primary keys explicet for clarity

changes made from ER diagram in design specs doc:
all instances of UserID have been replaced with username as we decided to have userName be unique.

Users model no longer has NumVotes as this was origonally goint to be used to keep track of
the number of likes a user had to check for verrified status but now we are planning to just 
query the database for total likes when the user applies for verifyed status.

in the Hack model "CategoryID" has been changed to categoryName

"""
def getNoUsernameText():
	return "!!!No Username!!!"

	
	
class UserAccount(models.Model):
	userName = models.CharField(max_length=30, unique=True, primary_key=True)
	password = models.CharField(max_length=30)
	email = models.EmailField()
	verified = models.BooleanField(default=False)
	def __str__(self):
		return self.userName
		
class Category(models.Model):
	categoryName = models.CharField(max_length=20, unique=True, primary_key=True)
	userName = models.ForeignKey(UserAccount, on_delete=models.SET(getNoUsernameText))
	description = models.CharField(max_length=55)
	class Meta:
		verbose_name_plural = 'Categories'
	def __str__(self):
		return self.categoryName
		
class Hack(models.Model):
	hackID = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=500)
	shortDescription = models.CharField(max_length=55)
	likes = models.IntegerField(default=0)
	userName = models.ForeignKey(UserAccount, on_delete=models.SET(getNoUsernameText))
	categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
	dateTimeCreated = models.DateTimeField()
	def __str__(self):
		return self.hackID

class Comment(models.Model):
	commentID = models.AutoField(primary_key=True)
	hackID = models.ForeignKey(Hack, on_delete=models.CASCADE)
	userName = models.ForeignKey(UserAccount, on_delete=models.SET(getNoUsernameText))
	text = models.CharField(max_length=255)
	dateTimeCreated = models.DateTimeField()
	def __str__(self):
		return self.commentID