from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This empty string means it looks at the root of the site
    path('', include('checkout_logic.urls')),
]