from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('login', views.do_login, name='login'),
 path('logout', views.do_logout, name='logout'),
 path('login_error', views.login_error, name='login_error'),
 path('home', views.home, name='home'),
 path('user', views.info_user, name='user'),
 path('movie/<int:id>', views.movie, name='movie'),
 path('play/<int:id>', views.play, name='play'),
 path('search/<str:name>', views.search, name='search'),
 path('genre/<str:name>', views.genre, name='genre'),
 path('sol_operation/<int:num>', views.sol_operation, name='sol_operation'),
]