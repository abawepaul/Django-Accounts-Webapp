from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('reg', views.reg, name="reg"),
    path('login', views.login, name="login"),
    path('userjobs/<num>', views.userjobs, name='userjobs'),
    path('accountedit/<num>', views.accountedit, name='accountedit'),
    path('accountupdate', views.accountupdate, name='accountupdate')
]