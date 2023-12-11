from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name="home"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('signup/', views.UserSignupView.as_view(), name="signup"),
    path('login/', views.UserLoginView.as_view() , name="login"),
    path('logout/', views.user_logout_view, name="logout"),

    path('addpost/', views.AddPost.as_view(), name="addpost"),
    path('updatepost/<int:pk>/', views.UpdatePost.as_view(), name="updatepost"),
    path('deletepost/<int:pk>/', views.delete_post, name="deletepost"),
]
