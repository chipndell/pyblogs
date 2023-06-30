from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# from posts.views import handle_404

urlpatterns = (
    [
        path("", include("posts.urls"), name="posts"),
        path("admin/", admin.site.urls),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)


handler400 = "posts.views.handle_400"
handler403 = "posts.views.handle_403"
handler404 = "posts.views.handle_404"
# handler404 = handle_404
handler500 = "posts.views.handle_500"
