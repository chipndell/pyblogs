from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import filetype
from .models import Blog_Post, User_Profile, TechKW


def clean_image(img):
    if img:
        mime = filetype.guess(img).mime
        if "image" not in mime:
            raise ValidationError("Not a valid image")
        if img.size / (1024 * 1024) > 2:
            raise ValidationError("Image size exceeds 2MB")


def clean_file(file):
    if file:
        mime = filetype.guess(file).mime
        if "pdf" not in mime and "zip" not in mime:
            raise ValidationError("Only `pdf`, `zip` and files are allowed.")
        if file.size / (1024 * 1024) > 2:
            raise ValidationError("File size exceeds 2MB")


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
        picture = self.files.get("picture", None)
        if picture:
            clean_image(picture)
        files = self.files.get("files", None)
        if files:
            clean_file(files)

    class Meta:
        model = Blog_Post
        fields = ["title", "description", "content", "picture", "files", "kws"]


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self._meta.fields:
            self.fields[key].widget.attrs.update({"class": "row-auto form-control"})

    cell_no = forms.IntegerField(
        max_value=9999999999, min_value=999999999, required=False
    )
    personal_web = forms.URLField()
    profile_pic = forms.ImageField(
        label=_("Profile Picture"),
        help_text="Select Image as your Profile Picture",
        required=False,
        widget=forms.ClearableFileInput,
    )
    nick_name = forms.CharField(
        label=_("Nick Name"),
        strip=True,
        help_text="Enter your Nick name here",
        min_length=1,
        max_length=16,
        required=False,
    )

    def clean(self):
        profile_pic = self.files["profile_pic"]
        clean_image(profile_pic)

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
        model = User_Profile
        fields = [
            "username",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User_Profile
        fields = [
            "username",
            "password",
        ]
