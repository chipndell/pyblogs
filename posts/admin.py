from django.contrib import admin
from .models import Blog_Post, User_Profile, User_Comments, Likes_Dislike, TechKW


admin.site.register(Blog_Post)
admin.site.register(User_Profile)
admin.site.register(User_Comments)
admin.site.register(Likes_Dislike)
admin.site.register(TechKW)


class Blog_Post_Admin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["content"]}
