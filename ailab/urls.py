from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_views.login_page, name='login'),
    path('register/', user_views.register_page, name='register'),
    path('logout/', user_views.logout_page, name='logout'),
    path('welcome/', include('landing.urls')),
    path('school/', include('school.urls')),
    path('api/auth/', include('users.urls')),
    path('api/modules/', include('modules.urls')),
    path('api/simulations/', include('simulations.urls')),
    path('api/ai/', include('ai_service.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/social/', include('social.urls')),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
