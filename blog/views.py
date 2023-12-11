from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, LoginForm, AddPostForm
from .models import Post


# Create your views here.

def homeview(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts, 'home_active': 'active'})


def about_view(request):
    return render(request, 'blog/about.html', {'about_active': 'active'})


def contact_view(request):
    return render(request, 'blog/contact.html', {'contact_active': 'active'})


def dashboard_view(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        posts = Post.objects.all()
        return render(request, 'blog/dashboard.html', 
                      {'posts': posts, 'full_name': full_name, 'groups': gps, 'dashboard_active': 'active'})
    else:
        return HttpResponseRedirect('/login/',)


class UserSignupView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = SignupForm(label_suffix=' ')
            return render(request, 'blog/signup.html', {'form': form, 'signup_active': 'active'})
        else:
            return HttpResponseRedirect('/dashboard/')
    
    def post(self, request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name= 'Author')
                user.groups.add(group)
                messages.success(request, 'Congratulations!! Account created successfully.')
                form = SignupForm(label_suffix= ' ')
        return render(request, 'blog/signup.html', {'form': form, 'signup_active': 'active'})

               
class UserLoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm(label_suffix=' ')
            return render(request, 'blog/login.html', {'form': form, 'login_active': 'active'})
        else:
            return HttpResponseRedirect('/dashboard/')
    
    def post(self, request):
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data.get('username')
                upass = form.cleaned_data.get('password')
                user = authenticate(username = uname, password = upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm(label_suffix= ' ')
        return render(request, 'blog/login.html', {'form': form, 'login_active': 'active'})


def user_logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


class UpdatePost(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            post = Post.objects.get(id=pk)
            form = AddPostForm(instance= post)
            return render(request, 'blog/updatepost.html', {'form': form})
        
        return HttpResponseRedirect('/login/')
        
    def post(self, request, pk):
        if request.method == 'POST':
            post = Post.objects.get(id=pk)
            form = AddPostForm(request.POST, instance= post)
            if form.is_valid():
                form.save()
                messages.success(request, "Post updated successfully!!")
                return HttpResponseRedirect('/dashboard/')
            
        return render(request, 'blog/updatepost.html', {'form': form})


class AddPost(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = AddPostForm(label_suffix= ' ')
            return render(request, 'blog/addpost.html', {'form': form})
        else:
            return HttpResponseRedirect('/login/')
        
    def post(self, request):
        if request.method == 'POST':
            form = AddPostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                desc = form.cleaned_data.get('desc')
                post = Post(title= title, desc= desc)
                post.save()
                messages.success(request, "Post added successfully!!")
                form = AddPostForm(label_suffix= ' ')
        return render(request, 'blog/addpost.html', {'form': form})
    

def delete_post(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post.objects.get(id=pk)
            post.delete()
            messages.success(request, "Post deleted successfully!!")
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
    