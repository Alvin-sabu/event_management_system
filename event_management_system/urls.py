from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from events import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL should be included only once
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),  # Homepage
    path('events/', include('events.urls')),  # Include the events app URLs
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
