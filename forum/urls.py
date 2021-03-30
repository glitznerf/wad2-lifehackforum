from django.urls import path
from forum import views
app_name = 'forum'
urlpatterns = [

#base pages
path('', views.home, name='home'),
path('about/', views.about, name = 'about'),

#account pages
path('create_account/' ,views.create_account, name = 'create_account'),
path('sign_in/' ,views.sign_in, name = 'sign_in'),
path('account_info/<slug:user_id_slug>/',views.account_info, name='account_info'),

#category pages
path('all_categories/<slug:category_categoryName_slug>/', views.category, name = 'category'),
path('all_categories/', views.all_categories, name = 'all_categories'),
path('all_categories/create_category', views.create_category, name = 'create_category'),

#hack pages
path('all_categories/<slug:category_categoryName_slug>/<slug:hack_hack_slug>/', views.hack , name = 'hack'),
path('all_categories/<slug:category_categoryName_slug>/add_hack/' ,views.add_hack, name = 'add_hack'),
path('hack/<slug:hack_hack_slug>/' ,views.just_hack, name = 'just_hack'),


#non template elements
path('sign_out/', views.sign_out, name='sign_out'),
path('add_comment/' , views.addComment, name='add_comment'),
]