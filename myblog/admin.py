from django.contrib import admin
from .models import Post, Comment, SiteRating

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # Number of empty forms to display

class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

    def delete_model(self, request, obj):
        # Automatically delete all related comments when a post is deleted
        obj.comments.all().delete()
        super().delete_model(request, obj)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(SiteRating)
