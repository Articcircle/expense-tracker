from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from expenses import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('expenses/',include('expenses.urls')),

]
