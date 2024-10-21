from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from myblog.models import Post
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import Profile  # تأكد من استيراد نموذج Profile
from django.core.paginator import  Paginator,PageNotAnInteger,EmptyPage
from django.db import models
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_admin = request.POST.get('is_admin')  # حقل للتحقق إذا كان المستخدم إداريًا

        # التحقق من تطابق كلمات المرور
        if password != confirm_password:
            messages.error(request, "كلمات المرور لا تتطابق.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل.')
            return redirect('register')

        # إنشاء مستخدم جديد
        user = User(
            username=username,
            email=email,
            password=make_password(password)  # تشفير كلمة المرور
        )
        
        # تعيين أذونات المستخدم
        if is_admin == 'on':  # تحقق مما إذا كان المستخدم إداريًا
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()  # حفظ المستخدم
        
        # تحقق مما إذا كان الملف الشخصي موجودًا بالفعل
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user)  # إنشاء كائن Profile فقط إذا لم يكن موجودًا

        messages.success(request, "تم تسجيلك بنجاح.")
        return redirect('login')  # إعادة توجيه المستخدم إلى صفحة تسجيل الدخول

    return render(request, 'users/register.html', {'title': 'تسجيل'})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')  # توجيه المستخدم للصفحة الرئيسية
            else:
                error_message = "البينات ليست متطابقة"
                return render(request, 'users/login.html', {'error': error_message})
        else:
            error_message = "يرجى إدخال اسم المستخدم وكلمة المرور"
            return render(request, 'users/login.html', {'error': error_message})

    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')  # توجيه المستخدم لصفحة تسجيل الدخول بعد الخروج

@login_required(login_url='login')
def profile(request):
    # استخدم user بدلاً من author
    posts = Post.objects.filter(user=request.user)  # تعديل هنا
    paginator = Paginator(posts, 10)  # تحديد عدد المشاركات لكل صفحة
    page = request.GET.get('page')  # الحصول على رقم الصفحة من الطلب
    try:
        post_list = paginator.page(page)  # الحصول على المشاركات للصفحة المحددة
    except PageNotAnInteger:
        post_list = paginator.page(1)  # إذا لم يكن الرقم صحيحًا، ابدأ من الصفحة 1
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # إذا كانت الصفحة فارغة، اذهب إلى آخر صفحة

    return render(request, 'users/profile.html', {
        'title': 'الملف الشخصي',
        'posts': posts,
        'page': page,
        'post_list': post_list
    })

class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'  # تأكد من أن لديك هذا القالب
    context_object_name = 'post'  # اسم الكائن الذي سيكون متاحاً في القالب


@login_required
def profile_update(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        user = request.user

        # تحقق من صحة البيانات
        if not username:
            messages.error(request, "اسم المستخدم مطلوب.")
        elif not email:
            messages.error(request, "البريد الإلكتروني مطلوب.")
        elif password and password != confirm_password:
            messages.error(request, "كلمات المرور غير متطابقة.")
        else:
            # تحديث بيانات المستخدم
            user.username = username
            user.email = email
            
            if password:  # تحديث كلمة المرور إذا تم إدخالها
                user.set_password(password)
            
            if image:  # تحقق مما إذا كانت الصورة موجودة
                user.profile.image = image  # تحديث صورة الملف الشخصي
                user.profile.save()  # حفظ الملف الشخصي

            user.save()
            messages.success(request, "تم تحديث الملف الشخصي بنجاح.")
            return redirect('profile')  # تعديل هذا حسب اسم رابط ملف التعريف

    context = {
        'title': 'تعديل الملف الشخصي',
        'user': request.user,  # أضف المستخدم إلى السياق لإعادة ملء النموذج
    }
    return render(request, 'users/profile_update.html', context)