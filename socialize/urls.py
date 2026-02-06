
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from.views import index ,tweet_create,tweet_edit,tweet_delete,tweet_list,register,login,logout,like,add_comment

from. import views
urlpatterns = [ 
 path('',views.tweet_list,name='tweet_list'),
 path('create/',views.tweet_create,name='tweet_create'),
 path('<int:tweet_id>/tweet_delete/',views.tweet_delete,name='tweet_delete'),
 path('<int:tweet_id>/edit/',views.tweet_edit,name='tweet_edit'),
  path('register',views.register,name='register'),
  path('accounts/login/',views.User_login,name='login'),
   path('logged_out',views.User_logout,name='logout'),
   path('search/',views.search_result,name='search'),
   path('test/',views.test,name='test'),
   path('<int:tweet_id>/like/',views.like,name='like'),
   path('<int:tweet_id>/comment/',views.add_comment,name='comment'),
   path('<int:tweet_id>/share/',views.increment_share_count,name='share_tweet'),
   path('oauth/',include('social_django.urls',namespace='social')),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
