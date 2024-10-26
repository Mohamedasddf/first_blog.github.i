from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import  Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Post, Comment
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
from django.contrib.auth.decorators import login_required
from .models import SiteRating
from .forms import SiteRatingForm
from django.db import models

# إعداد سجل الأخطاء
logger = logging.getLogger(__name__)
# Create your views here.

def home(request):
    posts = Post.objects.all()  # الحصول على جميع المشاركات
    paginator = Paginator(posts, 4)  # تحديد عدد المشاركات لكل صفحة
    page = request.GET.get('page')  # الحصول على رقم الصفحة من الطلب
    
    try:
        posts = paginator.page(page)  # الحصول على المشاركات للصفحة المحددة
    except PageNotAnInteger:
        posts = paginator.page(1)  # إذا لم يكن الرقم صحيحًا، ابدأ من الصفحة 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # إذا كانت الصفحة فارغة، اذهب إلى آخر صفحة

    context = {
        'title': 'الصفحه الرئيسيه',
        'posts': posts,
        'page':page,
    }
    return render(request, 'myblog/home.html', context)

def about(request):
    return render(request, 'myblog/about.html', {"title": "من أنا"})

def post_detail(request, post_id):
    # الحصول على المنشور بناءً على المعرف
    post = get_object_or_404(Post, pk=post_id)
    # الحصول على التعليقات الرئيسية المتعلقة بالمنشور
    comments = post.comments.filter(active=True,)
    if request.method == 'POST':
        name = request.POST.get('name')  # الحصول على اسم المعلق
        body = request.POST.get('body')  # الحصول على نص التعليق

        # تحقق مما إذا كانت جميع البيانات موجودة
        if name and body:
            new_comment = Comment(
                name=name,
                body=body,
                post=post,
            )
            new_comment.save()  # حفظ التعليق الجديد
            messages.success(request, "تم نشر التعليق بنجاح.")
            return redirect('post_detail', post_id=post.id)  # إعادة توجيه بعد الحفظ
        else:
            messages.error(request, "يرجى ملء جميع الحقول.")

    # إعداد السياق لتمريره إلى القالب
    context = {
        'title': post.title,
        'post': post,
        'comments': comments,
    }
    
    return render(request, 'myblog/detail.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  # لا حاجة لحق المؤلف هنا
    template_name = 'myblog/new_post.html'
    success_url = reverse_lazy('home')  # تأكد من ضبط هذا على عنوان URL الصحيح

    def form_valid(self, form):
        # تعيين المؤلف كالمستخدم الحالي
        form.instance.user = self.request.user

        # تحقق من المدخلات
        title = form.cleaned_data.get('title')
        content = form.cleaned_data.get('content')

        # تحقق مما إذا كان الحقل العنوان فارغًا
        if not title:
            form.add_error('title', 'عنوان التدوينة مطلوب.')

        # تحقق مما إذا كان المحتوى يحتوي على عدد كافٍ من الأحرف
        if not content:
            form.add_error('content', 'محتوى التدوينة مطلوب.')
        elif len(content) < 10:
            form.add_error('content', 'يجب أن يحتوي محتوى التدوينة على 10 أحرف على الأقل.')

        # إذا كانت هناك أخطاء، لن يتم حفظ النموذج
        if form.errors:
            return self.form_invalid(form)

        # حفظ النموذج إذا كانت جميع المدخلات صحيحة
        return super().form_valid(form)

    def form_invalid(self, form):
        # تسجيل الأخطاء
        logger.error("نموذج التدوينة غير صالح: %s", form.errors)
        return super().form_invalid(form)

@login_required  # يضمن أن المستخدم يجب أن يكون مسجلاً للدخول
def post_edit(request, post_id):  # تأكد من أن المعلمة هنا هي 'post_id'
    post = get_object_or_404(Post, id=post_id)  # استرجاع التدوينة حسب id

    # تحقق مما إذا كان المستخدم هو مؤلف التدوينة
    if post.user != request.user:
        messages.error(request, "لا يحق لك تعديل هذه المدونة. انشئ تدوينات ليكون لك الحق في التحكم فيها")  # إضافة رسالة للمستخدم
        return redirect('post_detail', post_id=post.id)  # إعادة التوجيه إلى تفاصيل التدوينة

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # تحقق من ملء جميع الحقول
        if title and content:
            post.title = title
            post.content = content
            post.save()  # حفظ التغييرات
            return redirect('post_detail', post_id=post.id)  # التأكد من استخدام 'post_id' هنا
        else:
            error_message = "يجب ملء جميع الحقول."
    else:
        error_message = ""

    return render(request, 'myblog/post_edit.html', {
        'post': post, 
        'error_message': error_message,
    })

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # تحقق مما إذا كان المستخدم هو مؤلف التدوينة
    if post.user != request.user:
        messages.error(request, " لا يحق لك حذف هذه التدوينه انشئ تدوينات ليكون لك الحق في التحكم فيها")  # إضافة رسالة للمستخدم
        return redirect('post_detail', post_id=post.id)  # العودة إلى تفاصيل التدوينة
   
    if request.method == 'POST':
        # حذف التعليقات المرتبطة (إذا كان لديك نموذج تعليقات)
        post.comments.all().delete()  # تأكد من استخدام الاسم الصحيح لعلاقة التعليقات
        post.delete()  # حذف التدوينة
        messages.success(request, "تم حذف التدوينة بنجاح.")
        return redirect('home')

    return render(request, 'myblog/post_confirm_delit.html', {'post': post})

def rate_site(request):    
    if request.method == 'POST':
        form = SiteRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            if request.user.is_authenticated:
                rating.user = request.user
            rating.save()
            return redirect('rate_site')  # أو أي صفحة أخرى تريدها
    else:
        form = SiteRatingForm()

    ratings = SiteRating.objects.all()  # الحصول على جميع التقييمات
    average_rating = SiteRating.objects.aggregate(models.Avg('rating'))['rating__avg']  # حساب متوسط التقييمات

    return render(request, 'myblog/rate_site.html', {'form': form, 'ratings': ratings, 'average_rating': average_rating,'title':'تقيم الموقع'})

def django(request):
    return render(request, 'myblog/django.html', {"title": "دوره جانجو"})

def python(request):
    return render(request, 'myblog/python.html', {"title": "دوره بايثون"})

def css(request):
    return render(request, 'myblog/c++.html', {"title": "دوره c++"})

def html(request):
    return render(request, 'myblog/html.html', {"title": "دوره html"})

def Privacy_Policy(request):
    return render(request,'myblog/PrivacyPolicy.html',{'title':' سياسه الخصوصيه }'})

def TermsofUse(request):
    return render(request,'myblog/TermsofUse.html',{'title':' شروط لاستخدام  }'})