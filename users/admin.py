from django.contrib import admin
from django.apps import AppConfig
from .models import Profile

# تسجيل نموذج Profile في لوحة إدارة Django
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')  # الحقول التي سيتم عرضها في عرض القائمة
    search_fields = ('user__username',)  # يتيح البحث بواسطة اسم المستخدم
    list_filter = ('user',)  # يمكّن من تصفية النماذج حسب المستخدم في واجهة الإدارة

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'



