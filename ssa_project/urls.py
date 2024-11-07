from django.contrib import admin
from django.urls import include, path
from chipin import views as chipin_views  # Import the home view from the chipin app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(("users.urls", "users"), namespace="users")),
    path('chipin/', include(("chipin.urls", "chipin"), namespace="chipin")),
    path('', chipin_views.home, name='home'),  # Add this line to route the root URL to chipin's home view
]
