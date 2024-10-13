from django.urls import path
from myblog import views 
urlpatterns=[
    path('',views.home,name='home')
]