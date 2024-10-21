from django.urls import path
from . import views
from .views import profile, PostDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),  # Added a comma here
    path('logout/', views.logout_user, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('post/<int:id>/', PostDetailView.as_view(), name='detail'),  # تأكد من أن هذا السطر موجود
    path('profile_update/',views.profile_update, name='profile_update'),
    path('accounts/login/', views.login_user, name='login'),  # هذا إذا كنت تستخدم view مخصص
    path('accounts/logout/', views.logout_user, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)