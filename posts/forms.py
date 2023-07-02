from django import forms
from .models import Blog_Post, User_Profile, TechKW
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import filetype


class Blog_Post_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self._meta.fields:
            self.fields[key].widget.attrs.update({"class": "row-auto form-control"})
        self.fields["content"].widget.attrs.update({"cols": 50, "rows": 25})

    title = forms.CharField(
        label=_("Title"),
        strip=True,
        required=True,
    )
    description = forms.CharField(
        label=_("Description"),
        strip=True,
        required=True,
    )
    content = forms.Textarea()
    picture = forms.ImageField(
        label=_("Blog Cover Image"),
        help_text="Select Cover Image for Blog",
        required=False,
    )
    files = forms.FileField(
        help_text="Select If you have any attachement that needs to be served with blog.",
        required=False,
    )
    kws = forms.MultipleChoiceField(
        widget=forms.SelectMultiple,
        choices=[(i.id, i.keyword) for i in TechKW.objects.all()],
    )

    def clean(self):
        content = self.cleaned_data["content"]
        title = self.cleaned_data["title"]
        description = self.cleaned_data["description"]
        if ("<" in (content, title, description)) or (
            ">" in (content, title, description)
        ):
            raise ValidationError("Replace `<` with `&lt;` and `>` with `&gt;`")
        picture = self.cleaned_data["picture"]
        if picture:
            if "image" not in filetype.guess(picture).mime:
                raise ValidationError("Replace `<` with `&lt;` and `>` with `&gt;`")
            if picture.size / (1024 * 1024) > 2:
                raise ValidationError("Image size exceeds 2MB")
        files = self.cleaned_data["files"]
        if files:
            mime = filetype.guess(files).mime
            if "pdf" not in mime and "zip" not in mime:
                raise ValidationError("Only `pdf`, `zip` and files are allowed.")
            if files.size / (1024 * 1024) > 2:
                raise ValidationError("File size exceeds 2MB")

    class Meta:
        model = Blog_Post
        fields = ["title", "description", "content", "picture", "files", "kws"]


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self._meta.fields:
            self.fields[key].widget.attrs.update({"class": "row-auto form-control"})

    cell_no = forms.IntegerField(max_value=9999999999, min_value=999999999)
    personal_web = forms.URLField()
    profile_pic = forms.ImageField(
        label=_("Profile Picture"),
        help_text="Select Image as your Profile Picture",
    )
    nick_name = forms.CharField(
        label=_("Nick Name"),
        strip=True,
        help_text="Enter your Nick name here",
        min_length=1,
        max_length=16,
        required=False,
    )

    class Meta:
        model = User_Profile
        fields = [
            "cell_no",
            "personal_web",
            "profile_pic",
            "nick_name",
        ]


class User_signup(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self._meta.fields:
            self.fields[key].widget.attrs.update({"class": "row-auto form-control"})

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
        ]
