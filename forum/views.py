from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from forum.models import UserAccount, Category, Hack, Comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from forum.forms import CategoryForm, HackForm, UserForm, UserAccountForm, CategoryForm


def home(request):
	#for top 3 of week - returns list of length 3 in order
	hackList = Hack.objects.order_by('-likes')[:3]
	context_dict = {}
	
	context_dict['hacks'] = hackList
	response = render(request, 'forum/home.html', context=context_dict)
	return response
	
	
def about(request):
	#???????????????????#
	context_dict = {}
	return render(request, 'forum/about.html', context=context_dict)

@login_required
def create_category(request):
	form = CategoryForm(request.user)
	userID =request.user.get_username()
	users = User.objects.filter(username=userID)
	verified = UserAccount.objects.filter(user__in=users, verified=True)
	
	if(verified):
		if request.method == 'POST':
			form = CategoryForm(request.user, request.POST)
			if form.is_valid():
				form.save(commit=True)
				return redirect('/forum/')
			else:
				print(form.errors)
		return render(request, 'forum/create_category.html', {'form': form})
	
	return HttpResponse("This page is exclusively for verified users \n If you believe you are verified please use the check verification button on your account info page \n backspace to return to home page")
	
	
def category(request, category_categoryName_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_categoryName_slug)
		hacks = Hack.objects.filter(categoryName=category)
		context_dict['hacks'] = hacks
		context_dict['category'] = category
		
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	return render(request, 'forum/category.html', context=context_dict)	

def hack(request, category_categoryName_slug, hack_hack_slug):
	
	context_dict = {}
	try:
		hack = Hack.objects.get(slug = hack_hack_slug)
		comment_list = Comment.objects.filter(hackID = hack)
		context_dict['hack'] = hack
		context_dict['comments'] = comment_list
		
	except Hack.DoesNotExist:
		context_dict['hack'] = None
	return render(request, 'forum/hack.html', context=context_dict)
	
	
	
@login_required
def add_hack(request, category_categoryName_slug):
	form = HackForm(request.user)
	if request.method == 'POST':
		form = HackForm(request.POST, request.user)
		if form.is_valid():
			form.save(commit=True)
			#perhaps redirect to category not home?
			return redirect('/forum/')
		else:
			print(form.errors)
	context_dict = {}		
	return render(request, 'forum/add_hack.html', {'form': form})
	
def all_categories(request):
	userID =request.user.get_username()
	users = User.objects.filter(username=userID)
	verified = UserAccount.objects.filter(user__in=users, verified=True)
	
	#search bar not included
	context_dict = {}
	category_list = Category.objects.order_by('-categoryName')
	context_dict['categories'] = category_list
	context_dict['verified'] = verified
	response = render(request, 'forum/all_categories.html', context=context_dict)
	return response


@login_required
def account_info(request, user_id_slug):
	context_dict = {}
	user_id =request.user.get_username()
	users = User.objects.filter(username=user_id)
	
	hack_list = Hack.objects.filter(name = user_id)
	context_dict['user'] = user_id
	context_dict['hacks'] = hack_list
	
	response = render(request, 'forum/account_info.html', context=context_dict)
	return response


def create_account(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserAccountForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserAccountForm()
	return render(request,'forum/create_account.html', context={'user_form': user_form,
				'profile_form': profile_form, 'registered': registered})

def sign_in(request):
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Get username & password from the login form.
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user: #test user returned
			if user.is_active: #test not disabled
				login(request, user) #send login
				return redirect(reverse('forum:home')) #return home
			else:
				#inactive account!
				return HttpResponse("Your Hacks R Us has been disabled")
		else:
			# Bad login details
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("invalid username and/or password")
	else:
		# No context variables to pass to the template system
		return render(request, 'forum/sign_in.html')


@login_required
def sign_out(request):
	logout(request)
	#user back to the home.
	return redirect(reverse('forum:home'))

	
#add verified functionality
	#-button on categories page
	#-cannot access the add category page regardless#
#add comment list to hack
#urls need fixes uh ohs
#add context dicts to forms
#test add comment
#search bar api needs implemented
#sort redirects
	#-back in breadcrumb proably
#http responses to an error page?? - requires template
#about form needs a plan
#testing generally, could be done by anyone if needed
#testing

@login_required
def addComment(request):
	form = CommentForm(request.user)
	if request.method == 'POST':
		form = CommentForm(request.POST, request.user)
		if form.is_valid():
			form.save(commit=True)
			return redirect('/forum/')
		else:
			print(form.errors)
			
			
#verified = UserAccount.objects.values_list('verified', flat = True).get(user=users)[0]

#verified = UserAccount.objects.only('verified').get(user=users).verified
	
#verified = UserAccount.objects.values('verified').get(user=users)['verified']			
	

