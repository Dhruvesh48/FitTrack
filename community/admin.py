from django.contrib import admin
from .models import Category, Post, Comment, PostLike, CommentLike
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    summernote_fields = ('content',)

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)