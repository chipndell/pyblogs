from django.urls import path
from .views import (
    BlogPostDetailView,
    BlogPostListView,
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostUpdateView,
    ProfileDetailView,
    ProfileCreateView,
    ProfileUpdateView,
    KWListView,
    # APIPostDetail,
    # APIPostList,
    login_view,
    signup_view,
    logout_view,
    aboutme,
    contactus,
    terms,
)

app_name = "posts"
urlpatterns = [
    path("keywards/<int:id>/", KWListView.as_view(), name="kwlist"),
    path("keywards/<slug:keyword>/", KWListView.as_view(), name="kwlist"),
    path("", BlogPostListView.as_view()),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("posts/explore/", BlogPostListView.as_view(), name="explore"),
    path("posts/myposts", BlogPostListView.as_view(), name="myposts"),
    path("posts/create/", BlogPostCreateView.as_view(), name="create"),
    path("posts/<slug:slug>/", BlogPostDetailView.as_view(), name="detail"),
    path("posts/<slug:slug>/delete/", BlogPostDeleteView.as_view(), name="delete"),
    path("posts/<slug:slug>/update/", BlogPostUpdateView.as_view(), name="update"),
    # path(
    #     "posts/api/<slug:slug>/detail/", APIPostDetail.as_view(), name="apipostsdetail"
    # ),
    # path("posts/api/list/", APIPostList.as_view(), name="apipostslist"),
    path("profile/<int:pk>/detail/", ProfileDetailView.as_view(), name="profiledetail"),
    path("profile/<int:pk>/create/", ProfileCreateView.as_view(), name="profilecreate"),
    path("profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="profileupdate"),
    path("aboutme/", aboutme, name="aboutme"),
    path("contactus/", contactus, name="contactus"),
    path("terms/", terms, name="terms"),
]
