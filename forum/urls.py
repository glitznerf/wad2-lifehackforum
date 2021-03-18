from django.urls import path
from forum import views
app_name = 'forum'
urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name = 'about'),
path('create_account/' ,views.create_account, name = 'create_account'),
path('sign_in/' ,views.sign_in, name = 'sign_in'),
path('all_categories/', views.all_categories, name = 'all_categories'),
path('sign_in/<slug:user_id_slug>/',views.account_info, name='account_info'),
path('all_categories/create_category', views.create_category, name = 'create_category'),
path('all_categories/<slug:category_id_slug>/<slug:hack_ID_slug>/', views.hack , name = 'hack'),
path('all_categories/<slug:category_id_slug>/add_hack/' ,views.add_hack, name = 'add_hack'),
path('all_categories/<slug:category_id_slug>/', views.category, name = 'category'),
]