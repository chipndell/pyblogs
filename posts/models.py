from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.text import slugify

lk_dk = [("no", "None"), ("lk", "Like"), ("dk", "Dislike")]


class TechKW(models.Model):
    keyword = models.CharField(max_length=16, blank=False, null=False)

    def __str__(self):
        return self.keyword


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cell_no = models.IntegerField(
        null=True, blank=True, validators=[RegexValidator(code="[0-9]")]
    )
    personal_web = models.CharField(max_length=128, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="images/dp", null=True, blank=True)
    nick_name = models.CharField(max_length=64, null=True, blank=True)


class Blog_Post(models.Model):
    slug = models.SlugField(max_length=50, blank=False, null=False, unique=True)
    published_date_time = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    content = models.TextField()
    picture = models.ImageField(upload_to="images", blank=True, null=True)
    files = models.FileField(upload_to="files", blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    in_review = models.BooleanField(default=True)
    kws = models.ManyToManyField(TechKW)

    def get_absolute_url(self):
        return f"/posts/{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:64]
        return super(Blog_Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class User_Comments(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    blog_id = models.ForeignKey(
        Blog_Post, on_delete=models.CASCADE, null=False, blank=False
    )
    comment = models.TextField()


class Likes_Dislike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    blog_id = models.ForeignKey(
        Blog_Post, on_delete=models.CASCADE, null=False, blank=False
    )
    like_dislike = models.CharField(max_length=8, choices=lk_dk)
