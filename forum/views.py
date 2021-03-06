from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from forum.models import UserAccount, Category, Hack, Comment
from django.db.models import Sum, F
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from forum.forms import CategoryForm, HackForm, UserForm, UserAccountForm, CommentForm

########################################## Base ###############################################
def home(request):
	#for top 3 of week - returns list of length 3 in order

	hackList = Hack.objects.order_by('-likes')[:3]
	context_dict = {}

	context_dict['hacks'] = hackList
	response = render(request, 'forum/home.html', context=context_dict)
	return response


def about(request):
	#information page
	context_dict = {}
	return render(request, 'forum/about.html', context=context_dict)

########################################## Category ###############################################

def create_category(request):
	#If the request is a HTTP POST, try to pull out the relevant information.
    form = CategoryForm()
	#get user ID
    userID = request.user.get_username()
	#get user object
    users = User.objects.filter(username=userID)
	#get if user is verified
    verified = UserAccount.objects.filter(user__in=users, verified=True)
    if (verified):
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                newCat = form.save(commit=False)
				#add user details to category
                newCat.user = UserAccount.objects.get(pk=request.user)
				#save details
                newCat.save()
                return redirect('/forum/all_categories')
        else:
            print(form.errors)

        return render(request, 'forum/create_category.html', {'form': form})

    return HttpResponse("This page is exclusively for verified users \n If you believe you are verified please use the check verification button on your account info page \n backspace to return to home page")


def category(request, category_categoryName_slug):
	context_dict = {}
	try:
		#pass category object and list of hacks in that category order most recent
		category = Category.objects.get(slug=category_categoryName_slug)
		hacks = Hack.objects.filter(categoryName=category).order_by('-dateTimeCreated')
		context_dict['hacks'] = hacks
		context_dict['category'] = category
		#handle faulty category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['hacks'] = None
	return render(request, 'forum/category.html', context=context_dict)

def all_categories(request):
	userID =request.user.get_username()
	users = User.objects.filter(username=userID)
	#pass verified to see if add category button is accessible
	verified = UserAccount.objects.filter(user__in=users, verified=True)

	context_dict = {}
	#pass all catgegories ordered alphabetically
	category_list = Category.objects.order_by('categoryName')
	context_dict['categories'] = category_list
	context_dict['verified'] = verified
	response = render(request, 'forum/all_categories.html', context=context_dict)
	return response



########################################## Hack ###############################################
def hack(request,  hack_hack_slug, category_categoryName_slug = None):
	context_dict = {}
	try:
		#get and pass hack object
		hack = Hack.objects.get(hackID = hack_hack_slug)
		#get and pass comments for that hack order most recent
		comment_list = Comment.objects.filter(hackID = hack).order_by('-dateTimeCreated')

		#pass if image is default to see if should be displayed
		if hack.image.url == "/media/default.jpg":
			context_dict['not_default']=False
		else:
			context_dict['not_default']=True

		context_dict['hack'] = hack
		context_dict['comments'] = comment_list

	except Hack.DoesNotExist:
		context_dict['hack'] = None
		context_dict['comments'] = None
	return render(request, 'forum/hack.html', context=context_dict)

@login_required
def add_hack(request, category_categoryName_slug):
    context_dict = {}
	#get and pass category object that hack will belong to
    category = Category.objects.get(slug = category_categoryName_slug)
    context_dict['category'] = category
    form = HackForm()
    if request.method == 'POST':
        form = HackForm(request.POST, request.FILES)
        if form.is_valid():
            newHack = form.save(commit=False)
			# add user and category detials to hack
            newHack.user = UserAccount.objects.get(user=request.user)
            newHack.categoryName = Category.objects.get(slug = category_categoryName_slug)
			#initailise likes to 0
            newHack.likes = 0
            newHack.save()
            return redirect('/forum/all_categories/'+category_categoryName_slug+'/')
        else:
            print(form.errors)

    return render(request, 'forum/add_hack.html', {'form': form, 'context' : context_dict})

########################################## Account ###############################################

@login_required
def account_info(request, user_id_slug):
	context_dict = {}

	#get and pass all hacks created by that user order by most recent
	hack_list = Hack.objects.filter(user__user = request.user).order_by('-dateTimeCreated')
	context_dict['hacks'] = hack_list

	#get total number of likes of user
	likes = Hack.objects.filter(user__user = request.user).aggregate(Sum('likes'))['likes__sum']
	if type(likes) != int:
		likes = 0
	context_dict['likes'] = likes

	if likes>=200:
		context_dict['enoughlikes'] = True
	else:
		context_dict['enoughlikes'] = False

	userID =request.user.get_username()
	users = User.objects.filter(username=user_id_slug)
	#pass verified to see if already verified
	verified = UserAccount.objects.filter(user__in=users, verified=True)
	context_dict['verified'] = verified

	response = render(request, 'forum/account_info.html', context=context_dict)
	return response

def create_account(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserAccountForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			#add details to useraccount and profile
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
	message = None
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
				message = "Your Hacks R Us has been disabled"
		else:
			# Bad login details
			message = "Invalid login details"
			return render(request, 'forum/sign_in.html', {'error': message})
	else:
		# No context variables to pass to the template system
		return render(request, 'forum/sign_in.html', {'error': message})

########################################## Non Template Elements ############################################

@login_required
def delete_account(request, user_id_slug):
    userID = request.user.get_username()
    users = User.objects.filter(username=userID)
    verified = UserAccount.objects.filter(user__in=users).delete()
    users.delete()
    return redirect(reverse('forum:home'))

def add_like(request, hack_hack_slug):
	#update hack objects like by 1
	Hack.objects.filter(hackID= hack_hack_slug).update(likes=F('likes')+1)
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def sign_out(request):
	logout(request)
	#user back to the home.
	return redirect(reverse('forum:home'))


@login_required
def add_comment(request, hack_hack_slug):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
			#add details to new comment
            newComm = form.save(commit=False)
            newComm.user = UserAccount.objects.get(pk=request.user)
            newComm.hackID = Hack.objects.get(pk = hack_hack_slug)
            newComm.save()
			#redirect back to pervious page
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            print(form.errors)

@login_required
def request_verification(request):
	sum = Hack.objects.filter(user__user = request.user).aggregate(Sum('likes'))['likes__sum']
	#test if user has reached enough levels of likes on hacks
	if (type(sum) == int and sum >= 200):
		userID = request.user.get_username()
		users = User.objects.filter(username=userID)
		verified = UserAccount.objects.filter(user__in=users, verified=True)
		UserAccount.objects.filter(user__in = users).update(verified=True)
		#redirect back to pervious page
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
