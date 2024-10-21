from django import template
from myblog.models import Post, Comment

register = template.Library()

@register.inclusion_tag('myblog/latest_blog.html')
def latest_blog():
    context = {
        'l_blog':Post.objects.all()[0:5]
    }
    return context
   

@register.inclusion_tag('myblog/latest_comments.html')
def latest_comments():
    context = {
        'l_comments':Comment.objects.filter(active=True)[0:5]
    }
    return context
   