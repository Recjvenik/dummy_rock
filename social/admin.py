from django.contrib import admin
from .models import Discussion, DiscussionReply


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'user', 'upvotes', 'reply_count', 'is_resolved', 'is_pinned', 'created_at']
    list_filter = ['is_resolved', 'is_pinned', 'module']
    search_fields = ['title', 'body', 'user__email']
    list_editable = ['is_pinned']


@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ['discussion', 'user', 'upvotes', 'is_best_answer', 'created_at']
    list_filter = ['is_best_answer']
    search_fields = ['body', 'user__email']
