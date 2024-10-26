from django.urls import path
from myblog import views 
from .views import PostCreateView
from .views import rate_site

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('detail/<int:post_id>/', views.post_detail, name='post_detail'),      
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'), 
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),  # تعديل هنا
    path('rate_site/', rate_site, name='rate_site'), 
    path('new_post/', PostCreateView.as_view(), name='new_post'),
    path('django/',views.django, name='django'),
    path('python/',views.python, name='python'),
    path('c++/',views.css, name='c++'),
    path('html/',views.html, name='html'),
    path('privacy-policy/', views.Privacy_Policy, name='privacy_policy'),
    path('Terms_ofUse/', views.TermsofUse, name='Terms_ofUse')
]
