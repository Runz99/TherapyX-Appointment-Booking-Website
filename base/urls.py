from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('bookasession/', views.bookingPage, name='booking'),
    path('contactpage/', views.contactPage, name='contact'),
    path('account/', views.account, name='account'),
    path('bookingSubmit/', views.bookingSubmit, name='bookingSubmit'),
    path('bookadmin/', views.bookAdmin, name='bookAdmin'),
    path('bookingAdminSubmit/', views.bookingAdminSubmit, name='bookingAdminSubmit'),
    #path('room/', views.room, name="room")
]