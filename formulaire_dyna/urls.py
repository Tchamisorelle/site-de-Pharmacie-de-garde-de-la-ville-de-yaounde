"""
URL configuration for formulaire_dyna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from formulaire.views import new_utilisateur, index, register, connect,user_login, reset_password_request,rmail,CustomPasswordResetConfirmView,reset_password_complete,reset_password_done, lister_plages_dates,user_logout,suggestion
from django.contrib.auth import views as auth_views

 #nb: le name qui est ici c'est ca qui est appeler dans la page html
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('connect/', connect, name='connect'),
    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    
    path('formulaire-inscription/', new_utilisateur, name='sign-up'),
    path('send_mail/', rmail, name='mail'),
    path('mail_reini/', reset_password_request, name='reinitial'),
    path('reset_password_done/', reset_password_done, name='reset_password_done'),
    # path("reset-password/", reset_password_request, name="reset_password"),
    path("rest_password/<str:token>/<str:uidb64>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', reset_password_complete, name='reset_password_complete'),
    path('lister-plages-dates/', lister_plages_dates, name='lister_plages_dates'),
    path('suggestion/', suggestion, name='suggestion'),

]
urlpatterns += staticfiles_urlpatterns()