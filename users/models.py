from django.db import models
from django.contrib.auth.models import User  # استخدم نموذج User المدمج

# لا تقم بإنشاء نموذج User جديد هنا
# class User(models.Model):
#     username = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # تأكد من أن كلمة المرور مشفرة
#     confirm_password = models.CharField(max_length=128)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # استخدام نموذج User المدمج
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # حقل الصورة

    def __str__(self):
        return f'{self.user.username} Profile'
