import os
import markdown
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializer import PostSerializer

from .forms import Blog_Post_Form, User_signup, UserProfileForm, LoginForm
from .models import Blog_Post, User_Profile, TechKW


def deploy(request):
    print("whoami", os.system("whoami"))
    os.system("cd ~/pyglogs")
    os.system("git pull -f origin master")
    os.system("touch /var/www/py2s_pythonanywhere_com_wsgi.py")
    print("Updated Deployment", request)


def md_to_html(data):
    return markdown.markdown(data)


class BlogPostListView(ListView):
    model = Blog_Post
    template_name_suffix = "_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "mypost" not in self.request.path:
            queryset = Blog_Post.objects.select_related("user").prefetch_related("kws")[
                ::-1
            ]
            context["object_list"] = queryset
            return context
        else:
            queryset = (
                Blog_Post.objects.select_related("user")
                .prefetch_related("kws")
                .filter(user_id=self.request.user.id)[::-1]
            )
            context["object_list"] = queryset
        return context


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Blog_Post
    form_class = Blog_Post_Form
    template_name_suffix = "_create"
    success_url = "/posts/explore"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog_Post
    template_name_suffix = "_delete"
    success_url = "/posts/explore"

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Blog_Post, slug=slug)
        if obj.user.id == self.request.user.id:
            return obj


class BlogPostDetailView(DetailView):
    model = Blog_Post
    template_name_suffix = "_detail"

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Blog_Post, slug=slug)
        return obj


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog_Post
    form_class = Blog_Post_Form
    template_name_suffix = "_update"
    success_url = "/posts/explore"


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User_Profile
    template_name_suffix = "_detail"

    def get_object(self):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(User_Profile, id=pk)
        return obj


class ProfileCreateView(CreateView):
    model = User_Profile
    form_class = UserProfileForm
    success_url = "/posts/explore"
    template_name_suffix = "_create"

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User_Profile
    form_class = UserProfileForm
    success_url = "/posts/explore/"
    template_name_suffix = "_update"


# class APIPostList(APIView):
#     def get(self, request):
#         posts = Blog_Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)


# class APIPostDetail(APIView):
#     def get_object(self, id):
#         try:
#             return Blog_Post.objects.get(id=id)
#         except Blog_Post.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, id):
#         post = self.get_object(id)
#         ser = PostSerializer(post)
#         return Response(ser.data)


class KWListView(ListView):
    model = TechKW
    template_name = "posts/blog_post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Blog_Post.objects.filter(kws__keyword=self.kwargs["keyword"])[::-1]
        if queryset:
            context["object_list"] = queryset
        return context


def login_view(request):
    context = {}
    form = LoginForm()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Successfully Loggedin to Account!!")
            return redirect("/posts/create")
        messages.warning(request, "Please check your credentials!!")
    context.update({"form": form})
    return render(request, "login.html", context=context)


def signup_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password1"]
        if password1 != password2:
            messages.warning(request, "Passwords do not match!")
            return redirect("signup")
        user = User_Profile.objects.create_user(
            username=username,
            password=password1,
        )
        g = Group.objects.get(name="EndUser")
        user.groups.add(g)
        messages.success(request, "Account creation is successful!")
        return redirect("/login/")
    form = User_signup()
    context.update({"form": form})
    return render(request, "signup.html", context=context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have successfully Logged out!!")
        return render(request, "logout.html")
    messages.warning(request, "Please check URL!!")
    return redirect("login")


def aboutme(request):
    return render(request, "aboutme.html")


def contactus(request):
    return render(request, "contactus.html")


def terms(request):
    return render(request, "termspage.html")


def handle_400(request, exception=400):
    return render(request, "400.html")


def handle_403(request, exception=403):
    return render(request, "403.html")


def handle_404(request, exception=404):
    return render(request, "404.html")


def handle_500(request, exception=500):
    return render(request, "500.html")
